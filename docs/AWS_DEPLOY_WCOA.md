# AWS Deployment Runbook - West Coast Ocean Data Portal

This runbook deploys the self-contained WCOA Docker stack on one EC2 host. Complete the shared host preparation in the [Madrona Portal AWS guide](https://github.com/Ecotrust/madrona-portal/blob/main/docs/AWS_DEPLOY.md) first. This runbook covers WCOA specific image, configuration, data, and service setup.

Use this document when starting from scratch with WCOA deployment and repeatable release operations.

This stack contains wcoa app, Geoportal and Harvester on Tomcat, Elasticsearch for metadata indexing/search, Geoportal WAR artifacts, WCOA-specific proxy routes and cron jobs.

## Sizing and prerequisites

Start with:  

- Start at t3.large minimum for production
- Use at least 60 GB root volume
- Security-group access for SSH and HTTP/HTTPS only
- Docker Engine and the Compose plugin
- A GHCR read token for `ghcr.io`
- The current production database dump and media archive
- WCOA deployment host SSH key
- WCOA production environment values for docker/.env
- Geoportal WAR files:
  - geoportal.war
  - harvester.war

## Clone repository and place artifacts

```bash
sudo mkdir -p /home/ubuntu/portals/madrona-apps
sudo chown ubuntu:ubuntu /home/ubuntu/portals /home/ubuntu/portals/madrona-apps
cd /home/ubuntu/portals/madrona-apps
git clone https://github.com/Ecotrust/wcoa.git
cd wcoa
```

Production uses the self-contained WCOA image; the host does not need a checkout of `madrona-portal` or the shared application repositories.

Create required directories and place artifacts:

```bash
mkdir -p docker/wars
mkdir -p docker/media
mkdir -p docker/static
mkdir -p docker/backups/elasticsearch
mkdir -p docker/backups/sql
```

Copy WAR files into docker/wars and restore media into docker/media.

For example, from the workstation holding the approved artifacts:

```bash
scp /secure/path/geoportal.war ubuntu@<host>:/home/ubuntu/portals/madrona-apps/wcoa/docker/wars/
scp /secure/path/harvester.war ubuntu@<host>:/home/ubuntu/portals/madrona-apps/wcoa/docker/wars/
scp -r /secure/path/media/. ubuntu@<host>:/home/ubuntu/portals/madrona-apps/wcoa/docker/media/
```

Set directory ownership for Elasticsearch snapshots:

```bash
chown -R "$(id -u)":"$(id -g)" docker/backups/elasticsearch
```

Allow nginx to traverse the home directory if required by the host's default permissions:

```bash
sudo chmod o+x /home/ubuntu
```

## Configure WCOA

### Create docker environment file

```bash
cp docker/.env.example docker/.env
chmod 600 docker/.env
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
gpt_frame_options=DENY
gpt_allowed_origin=<verified-production-origins>
gpt_admin_username=<from-secure-credential-store>
gpt_admin_password=<from-secure-credential-store>
gpt_publisher_username=<from-secure-credential-store>
gpt_publisher_password=<from-secure-credential-store>
gpt_user_username=<from-secure-credential-store>
gpt_user_password=<from-secure-credential-store>
gpt_esri_username=<from-secure-credential-store>
gpt_esri_password=<from-secure-credential-store>

ELASTIC_PASSWORD=<required>
CLUSTER_NAME=elasticsearch
ES_REINDEX_REMOTE_WHITELIST=elastic.prod.wcoa.ecotrust.org:80
```

Notes:

- `IMAGE_TAG` is required and must be a pinned WCOA image tag
- In production compose, `APP_PORT` controls the host-side loopback mapping only. Gunicorn binds container port 8008.
- App, database, Redis, Geoportal, and Elasticsearch host ports bind to `127.0.0.1`; host nginx is the public ingress.

Confirm that `docker/config.wcoa.prod.ini` contains the verified production values. It is mounted and selected through `MP_PROJECT_CONFIG`.

## Authenticate and start the stack

Log in to GHCR on host:

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin
```

Validate and pull the pinned image:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env config >/dev/null
docker compose -f docker/compose.prod.yml --env-file docker/.env pull
```

In most cases you will have an existing production database to import. In this case start the stack without running fixtures:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

If for some reason you do not have an existing production database to import, then use initial fixtures by setting `DB_INIT=1` in `docker/.env` for the first start:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

After initialization, set `DB_INIT=0` in `docker/.env` and recreate the app:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d --force-recreate app
```

## Restore/Import production data

Import the production database to restore the dump after the database is healthy:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env stop app
./scripts/db-restore.sh --drop /path/to/mida-production.sql
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d app
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

## Host nginx and TLS

Install nginx and Certbot following the core host guide. Create a server block for the WCOA hostnames using these locations, then run Certbot to add TLS and HTTP-to-HTTPS redirection:

```nginx
server {
  listen 80;
  listen [::]:80;
  server_name portal.westcoastoceans.org www.westcoastoceans.org;

  client_max_body_size 100M;

  location /static/ {
    alias /home/ubuntu/portals/madrona-apps/wcoa/docker/static/;
  }

  location /media/ {
    alias /home/ubuntu/portals/madrona-apps/wcoa/docker/media/;
  }

  location ~ ^(/_search/|/_doc/|/metadata).*$ {
    proxy_pass http://127.0.0.1:9200;
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location ~ ^/(manager|host-manager|semantix|solr|gc|geoportal|harvester).*$ {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300;
  }

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300;
  }
}
```

After DNS points to the instance, request the certificate and validate nginx:

```bash
sudo certbot --nginx -d portal.westcoastoceans.org -d www.westcoastoceans.org
sudo nginx -t
sudo systemctl reload nginx
```

## Elasticsearch and Geoportal checks

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

## systemd service for WCOA

Before enabling the WCOA unit, disable any legacy portal units that can restart the old stack:

```bash
# Staging
sudo systemctl disable --now staging.madrona-portal.service || true
# Production
sudo systemctl disable --now madrona-portal.service || true
```

Create unit file such as /etc/systemd/system/wcoa.service:

```bash
sudo nano /etc/systemd/system/wcoa.service
```

```ini
[Unit]
Description=WCOA Docker Stack
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/portals/madrona-apps/wcoa/docker
ExecStart=/usr/bin/docker compose -f /home/ubuntu/portals/madrona-apps/wcoa/docker/compose.prod.yml --env-file /home/ubuntu/portals/madrona-apps/wcoa/docker/.env up -d
ExecStop=/usr/bin/docker compose -f /home/ubuntu/portals/madrona-apps/wcoa/docker/compose.prod.yml --env-file /home/ubuntu/portals/madrona-apps/wcoa/docker/.env down
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

Confirm only the intended unit is enabled and that the app container image is WCOA:

```bash
systemctl list-unit-files | grep -E 'wcoa|madrona'
systemctl status wcoa.service --no-pager
docker ps --format '{{.Names}} {{.Image}}' | grep -E 'wcoa|madrona-portal'
```

## Cron jobs for WCOA

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

## Restart Nginx after cutover

```bash
sudo service nginx restart
```

## Release and rollback

### Deploy a new release

1. Set IMAGE_TAG to a pinned new SHA in docker/.env.
2. Pull and recreate:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env pull
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

3. Verify app, db, elastic, and geoportal health.
4. Verify the running app image matches the intended WCOA tag:

```bash
docker ps --format '{{.Names}} {{.Image}}' | grep app
```

The app image should be `ghcr.io/ecotrust/wcoa:<pinned-tag>`, not `ghcr.io/ecotrust/madrona-portal:<tag>`.

### Rollback

1. Set IMAGE_TAG back to prior known-good SHA.
2. Pull and recreate using same commands.
3. Re-verify health and core routes.

## Services and ports reference

Container services:

- app (Gunicorn inside container on 8008)
- db (PostGIS on 5432)
- tasks (Redis on 6379)
- geoportal (Tomcat on 8080)
- elastic (Elasticsearch on 9200/9300)
- kibana (dev profile only)
- nginx (dev profile only)

Host-facing defaults (all bound to loopback for host nginx or maintenance access):

- APP_PORT default 8000 mapped to container 8008
- DB_PORT default 5432 mapped to container 5432
- Redis default 6379, Geoportal 8080, and Elasticsearch 9200/9300

## Troubleshooting and tips

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
docker compose -f docker/compose.prod.yml --env-file docker/.env exec db \
  sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

If APP_PORT changes, confirm Nginx proxy_pass target is updated to match host-side port.

Confirm the production configuration and catalog are active:

```bash
curl -sf http://127.0.0.1:8000/ >/dev/null
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app \
  python marco/manage.py shell -c \
  'from django.conf import settings; assert settings.DEBUG is False; assert settings.DATA_CATALOG_ENABLED; print(settings.CATALOG_SOURCE, settings.CATALOG_QUERY_ENDPOINT)'
```
