# WCOA Production Cutover

This document covers migration of the currently running production WCOA stack from the old coupled deployment to the decoupled WCOA stack.

Use this document for production cutover planning and execution. For baseline host setup and greenfield deployment, use:

- Core host guide: madrona-portal – docs/AWS_DEPLOY.md
- WCOA deploy runbook: ./AWS_DEPLOY_WCOA.md

## Preconditions

Begin when all of these are true:

- Core base image and WCOA overlay image are published and pinned by tag.
- The target WCOA image tag was validated in staging.
- A full database restore test from the latest production dump has succeeded in staging.
- Latest media backup has been verified readable.
- Maintenance window is approved and communicated.
- Rollback owner and decision authority are explicitly assigned.

## Capture current production state

Before changing anything, capture all current state artifacts and copy them off-instance.

Capture checklist:

- Running app image tag and digest.
- Current docker environment file values.
- Current nginx site config.
- Current cron configuration.
- Fresh PostgreSQL dump.
- Fresh Elasticsearch snapshot.
- Media tarball backup.

Example commands:

```bash
# Record running image references
docker ps --format '{{.Names}} {{.Image}}' > /tmp/cutover-running-images.txt

# Save current crontab and nginx
crontab -l > /tmp/cutover-crontab.txt
sudo cp /etc/nginx/sites-available/default /tmp/cutover-nginx-default.conf

# DB dump and ES snapshot from existing workflow paths (adjust if needed)
cd /home/ubuntu/portals/madrona-apps/wcoa
./scripts/db_dump.sh -c ./docker/compose.prod.yml -e ./docker/.env -d ./docker/backups/sql
./scripts/create_elastic_snapshot.sh -r gp_es_snap

# Media backup
cd /home/ubuntu/portals/madrona-apps/wcoa
tar -czf /tmp/cutover-media-$(date +%F_%H-%M-%S).tgz docker/media
```

Copy all /tmp/cutover-* artifacts and backup files to durable external storage.

## Choose cutover strategy

### Strategy A: In-place cutover

Use the same instance, stop old services, deploy decoupled stack in-place.

- Pros: fastest, no DNS/EIP move.
- Cons: highest blast radius.
- Rollback model: restart old stack with prior configs and image tags.

### Strategy B: Side-by-side cutover

Provision a new instance, restore data, verify with staging hostname, then move Elastic IP or DNS.

- Pros: safest, clean rollback by switching traffic back.
- Cons: requires temporary duplicate infrastructure.
- Rollback model: move Elastic IP/DNS back to old instance.

## 3. Data continuity warning

Docker named volumes are namespaced by compose project name.

If compose project names differ between old and new stacks, the new stack will not see old volumes automatically.

Best practice:

- perform explicit DB restore and media restore into the new stack.
- validate Elasticsearch snapshot repository and restore path explicitly.
- assume volume reuse as a migration method.

## Cutover steps

### Prepare target stack

On the target host:

- Clone and configure WCOA repo.
- Place WAR files and media.
- Prepare docker env and production config.
- Pull and boot decoupled stack.

```bash
cd /home/ubuntu/portals/madrona-apps/wcoa
docker compose -f docker/compose.prod.yml --env-file docker/.env pull
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

### Restore data and validate services

```bash
# Restore DB from a known-good dump
scripts/db_restore.sh -c ./docker/compose.prod.yml -e ./docker/.env -d ./docker/backups/sql/<dump-file>.sql

# Run migrations
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app python marco/manage.py migrate
```

If needed for legacy path alignment:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env exec app python marco/manage.py migration_to_layers
```

### Traffic move

For side-by-side:

- Move Elastic IP to new instance or switch DNS A record.
- Verify nginx and certbot on new host.
- Confirm security group does not expose internal ports.

For in-place:

- Stop old stack.
- Start decoupled stack.
- Validate ingress and app health immediately.

## Verification checklist

Complete all checks before declaring success.

Application:

- Homepage loads.
- Admin login works.
- Representative map/layer pages load.
- Static and media assets load.

Data/catalog:

- Elasticsearch responds and metadata search works.
- Geoportal and harvester routes respond.
- Geospatial-related routes required by WCOA respond.

Background jobs:

- Celery task execution round-trip works.
- Cron entries are installed and dry-run successfully.

Operational:

- systemd unit status is healthy.
- No recurring critical errors in app/db/elastic/geoportal logs.

## Rollback triggers and commands

Rollback if any of these are true after remediation attempts during the window:

- Core page flows remain unavailable for more than 10 minutes.
- Data integrity checks fail (missing critical records, broken catalog indices).
- Login/admin workflows remain broken.
- Unexpected high error rate persists in app logs.

### Strategy A rollback (in-place)

Use previously captured old-stack compose/config files and prior image tags.

```bash
# Stop decoupled stack
cd /home/ubuntu/portals/madrona-apps/wcoa/docker
docker compose -f compose.prod.yml --env-file .env down

# Start prior stack using its original compose/env paths
cd /home/ubuntu/portals/<old-stack-path>
docker compose -f <old-compose-file> --env-file <old-env-file> up -d
```

### Strategy B rollback (side-by-side)

```bash
# Move traffic back to old instance
# Option 1: re-associate Elastic IP to old instance
# Option 2: revert DNS A/ALIAS to old instance endpoint
```

Then verify old stack health and keep the failed new stack online but isolated for diagnosis.

## Decommission and retention

After stable operation:

- Capture final post-cutover DB dump.
- Capture final Elasticsearch snapshot.
- Archive old instance logs and configs.
- Remove old instance.
