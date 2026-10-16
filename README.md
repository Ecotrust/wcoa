# West Coast Ocean Data Portal

The West Coast Ocean Data Portal is the Regional Data Sharing Portal serving West Coast data users and the West Coast Ocean Alliance. The portal aims to increase the discovery and connectivity of ocean and coastal data and people to better inform regional resource management, policy development, and ocean planning.

## Docker architecture

WCODP has two Docker workflows:

- **Local development:** builds the wcoa portal overlay image on top of the shared `madrona-portal` base image and mounts the sibling application repositories for live development.
- **Production:** runs a self-contained image from GHCR with PostGIS, Redis, Geoportal, and Elastic. Host nginx provides static/media serving and TLS. 

## Local development

For a new workstation, including the full shared-repository clones, WAR files, local configuration, and database import, follow [Development Environment Setup](docs/DEVELOPMENT_SETUP.md).

Quick start from the repository root:

```bash
cp docker/.env.example docker/.env
# Set local SECRET_KEY, DB_PASSWORD, REDIS_PASSWORD, and DJANGO_SUPERUSER_PASSWORD.
task build-base
task build-portal
task up
```

The app is available at <http://localhost:8000/>
Geoportal at <http://localhost:8080/>
Elasticsearch at <http://localhost:9200/>

For more task commands see [Taskfile.yml](Taskfile.yml)  

## Production deployments

Production uses `docker/compose.prod.yml` and a pinned image:

```text
ghcr.io/ecotrust/wcoa:<short-commit-sha>
```

The production Compose file contains `app`, `db`, `tasks`, `geoportal`, and `elastic`. Gunicorn listens on container port `8008`; `APP_PORT` is the host port nginx proxies to, normally `8000`. PostGIS and Redis are bound to host loopback and are not exposed directly to the network.

Use [docs/AWS_DEPLOY_WCOA.md](docs/AWS_DEPLOY_WCOA.md) for deployment instructions, production `.env` values, initialization versus restore, nginx/TLS, systemd, backups, release, and rollback.
 
Use [docs/PRODUCTION_CUTOVER.md](docs/PRODUCTION_CUTOVER.md) only to migrate the existing deployment.

## Docker structure in this repo

- `docker/Dockerfile` builds the WCOA overlay from `ghcr.io/ecotrust/madrona-portal`
- `docker/compose.prod.yml` defines the production Compose stack
- `docker/compose.yml` defines WCOA app plus `geoportal` and `elastic`
- `docker/config.wcoa.docker.ini` holds local-development portal config
- `docker/config.wcoa.prod.ini` holds production-focused portal config
- `docker/.env` holds local secrets and environment-specific values
- `scripts/db_dump.sh` is a production database dump helper
- `scripts/db-restore.sh` imports a database dump
- `wcoa/` contains the WCOA Django application code
