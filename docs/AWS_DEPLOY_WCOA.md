# AWS Deployment Runbook - WCOA Portal

This runbook is for deploying WCOA on a host that is already prepared using the core platform guide in [madrona-portal/docs/AWS_DEPLOY.md](../../../madrona-portal/docs/AWS_DEPLOY.md).

Use this document for greenfield WCOA deployment and repeatable release operations.

## 1. What WCOA adds

Compared to the platform baseline, WCOA adds:

- Geoportal and Harvester on Tomcat.
- Elasticsearch for metadata indexing/search.
- Geoportal WAR artifacts.
- WCOA-specific proxy routes and cron jobs.

Sizing guidance:

- Start at t3.large minimum for production.
- Use at least 60 GB root volume.
- Monitor memory and disk pressure during indexing jobs.

## 2. Prerequisites to collect

From secure credential storage, collect:

- WCOA deployment host SSH key.
- GHCR read token for image pulls.
- WCOA production environment values for docker/.env.
- Geoportal WAR files:
  - geoportal.war
  - harvester.war
- Current database dump for initial load.
- Media backup archive.

## 3. Clone repository and place artifacts

On the host:

```bash
mkdir -p /home/ubuntu/portals
cd /home/ubuntu/portals
git clone https://github.com/Ecotrust/wcoa.git
cd wcoa
```

Create required directories and place artifacts:

```bash
mkdir -p docker/wars
mkdir -p docker/media
mkdir -p docker/backups/elasticsearch
mkdir -p docker/backups/sql
```

Copy WAR files into docker/wars and restore media into docker/media.

Set directory ownership for Elasticsearch snapshots:

```bash
chown -R "$(id -u)":"$(id -g)" docker/backups/elasticsearch
```

## 4. Configure WCOA

### 4.1 Create docker environment file

```bash
cp docker/.env.example docker/.env
```

Required production settings in docker/.env:

```env
COMPOSE_PROJECT_NAME=wcoa
IMAGE_TAG=<pinned-short-sha>
BASE_TAG=<base-tag-used-for-this-overlay>

APP_PORT=8000
DB_PORT=5432

SECRET_KEY=<required>
DEBUG=False
ALLOWED_HOSTS=portal.westcoastoceans.org,www.westcoastoceans.org

DB_NAME=wcoa_docker_db
DB_USER=postgres
DB_PASSWORD=<required>
REDIS_PASSWORD=<required>

DB_INIT=0
DJANGO_ENV=production
GUNICORN_WORKERS=3

gpt_catalog_war=./wars/geoportal.war
gpt_harvester_war=./wars/harvester.war

ELASTIC_PASSWORD=<required>
CLUSTER_NAME=elasticsearch
ES_REINDEX_REMOTE_WHITELIST=elastic.prod.wcoa.ecotrust.org:80
```

Notes:

- In production compose, APP_PORT controls host mapping only. Gunicorn binds container port 8008.

### 4.2 Confirm production ini selection

WCOA production compose mounts and uses:

- docker/config.wcoa.prod.ini

No change is required unless you need environment-specific non-secret overrides.

## 5. Authenticate and first boot

Log in to GHCR on host:

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin
```

Pull and start services:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env pull
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

If this is first boot and you need Django init tasks:

```bash
DB_INIT=1 docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

After init, ensure DB_INIT is set back to 0 in docker/.env.

## 6. Load data

Restore database dump with production compose:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env exec -T \
  -e PGPASSWORD="$DB_PASSWORD" db psql -U "$DB_USER" -d "$DB_NAME" \
  < /path/to/dump.sql
```

Apply migrations:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app python marco/manage.py migrate
```

If required for legacy layers migration:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app python marco/manage.py migration_to_layers
```

Rebuild static assets if needed:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app python marco/manage.py collectstatic --noinput
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app python marco/manage.py compress --force
```

## 7. Nginx routes for WCOA

Use core Nginx/TLS setup pattern, then add WCOA upstream routes.

Core app route should proxy to host loopback APP_PORT.

Example WCOA-specific upstreams:

- /geoportal and /harvester -> 127.0.0.1:8080
- /_search, /_doc, /metadata -> 127.0.0.1:9200
- /geospatial -> filesystem path expected by Geoportal
- /nativeland -> app route as configured

Do not proxy internal services via public IP. Use loopback targets.

## 8. Elasticsearch and Geoportal checks

Verify service health:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env ps
docker compose -f docker/compose.prod.yml --env-file docker/.env logs -f elastic
docker compose -f docker/compose.prod.yml --env-file docker/.env logs -f geoportal
```

Register snapshot repository if not yet configured:

```bash
curl -X PUT "http://127.0.0.1:9200/_snapshot/gp_es_snap" \
  -H 'Content-Type: application/json' \
  -d '{"type":"fs","settings":{"location":"/usr/share/elasticsearch/backups"}}'
```

Create a test snapshot:

```bash
./scripts/create_elastic_snapshot.sh -r gp_es_snap
```

## 9. systemd service for WCOA

Create unit file such as /etc/systemd/system/wcoa.service:

```ini
[Unit]
Description=WCOA Docker Stack
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/portals/madrona-apps/wcoa/docker
ExecStart=/usr/bin/docker compose -f compose.prod.yml --env-file .env up -d
ExecStop=/usr/bin/docker compose -f compose.prod.yml --env-file .env down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable wcoa.service
sudo systemctl start wcoa.service
```

## 10. Cron jobs for WCOA

Install cron entries for DB dump, ES snapshots, and nativeland refresh.

Recommended entries:

```cron
# DB dump retention
15 2 * * * cd /home/ubuntu/portals/madrona-apps/wcoa && /bin/bash -lc './scripts/db_dump.sh -c ./docker/compose.prod.yml -e ./docker/.env -d ./docker/backups/sql && find ./docker/backups/sql -type f -name "*.sql" -mtime +10 -delete' >> /home/ubuntu/portals/madrona-apps/wcoa/docker/backups/db_dump.log 2>&1

# Elasticsearch snapshot
15 3 * * * /usr/bin/bash /home/ubuntu/portals/madrona-apps/wcoa/scripts/create_elastic_snapshot.sh -r gp_es_snap

# NativeLand refresh
31 5 * * * cd /home/ubuntu/portals/madrona-apps/wcoa/docker && docker compose -f compose.prod.yml --env-file .env exec app python marco/manage.py import_nativeland
```

## 11. Release and rollback

### 11.1 Deploy a new release

1. Set IMAGE_TAG to a pinned new SHA in docker/.env.
2. Pull and recreate:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env pull
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

3. Verify app, db, elastic, and geoportal health.

### 11.2 Rollback

1. Set IMAGE_TAG back to prior known-good SHA.
2. Pull and recreate using same commands.
3. Re-verify health and core routes.

## 12. Services and ports reference

Container services:

- app (Gunicorn inside container on 8008)
- db (PostGIS on 5432)
- tasks (Redis on 6379)
- geoportal (Tomcat on 8080)
- elastic (Elasticsearch on 9200/9300)
- kibana (dev profile only)
- nginx (dev profile only)

Host-facing defaults:

- APP_PORT default 8000 mapped to container 8008
- DB_PORT default 5432 mapped to container 5432
- Geoportal and Elasticsearch are mapped directly in compose and should remain security-group restricted

## 13. Troubleshooting

Useful checks:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env ps
docker compose -f docker/compose.prod.yml --env-file docker/.env logs -f app
```

Run a Django command:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app python marco/manage.py <command>
```

Database connectivity smoke test:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env exec db pg_isready -U "$DB_USER" -d "$DB_NAME"
```

If APP_PORT changes, confirm Nginx proxy_pass target is updated to match host-side port.
