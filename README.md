West Coast Ocean Alliance (WCOA) Data Portal
=====

Django web application and Wagtail CMS for the West Coast Ocean Data Portal.

This repository is the WCOA portal application for the [Madrona Portal](https://github.com/Ecotrust/madrona-portal) platform.

## Prerequisites

- Docker Desktop or Docker Engine with Compose v2
- [go-task](https://taskfile.dev) (`brew install go-task`)
- Workspace with side-by-side [madrona-portal](https://github.com/Ecotrust/madrona-portal) repo and madrona-apps folder containing this repo and other portal repos:

```text
madrona/
├── madrona-portal/
└── madrona-apps/
    └── wcoa/
    └── django_url_shortener/
    └── madrona-analysistools/
    └── etc.
```

```bash
mkdir madrona
cd madrona
git clone https://github.com/Ecotrust/madrona-portal.git
mkdir madrona-apps
cd madrona-apps
git clone https://github.com/Ecotrust/wcoa.git
git clone https://github.com/Ecotrust/django_url_shortener.git
git clone https://github.com/Ecotrust/madrona-analysistools.git
git clone https://github.com/Ecotrust/madrona-features.git
git clone https://github.com/Ecotrust/madrona-manipulators.git
git clone https://github.com/Ecotrust/madrona-scenarios.git
git clone https://github.com/Ecotrust/mp-accounts.git
git clone https://github.com/Ecotrust/mp-data-manager.git
git clone https://github.com/Ecotrust/mp-drawing.git
git clone https://github.com/Ecotrust/mp-explore.git
git clone https://github.com/Ecotrust/mp-layers.git
git clone https://github.com/Ecotrust/mp-map-groups.git
git clone https://github.com/Ecotrust/mp-proxy.git
git clone https://github.com/Ecotrust/mp-survey.git
git clone https://github.com/Ecotrust/mp-visualize.git
git clone https://github.com/Ecotrust/p97-nursery.git
```

## Quickstart (local development)

Run all commands from this repository root (`madrona-apps/wcoa`).

```bash
cd wcoa
```

Create your local environment file:

```bash
cp docker/.env.example docker/.env
```

Edit `docker/.env` and set at minimum:
- `SECRET_KEY`
- `DB_PASSWORD`
- `REDIS_PASSWORD`
- `DJANGO_SUPERUSER_PASSWORD` (recommended for first init)

*A full `.env` example can be found in 1Password.*

Add directory named wars:

```bash
mkdir wars
```

Find the WAR files for Geoportal and Harvester in 1Password and then copy them into the `wars` directory:

```text
└── wcoa/
    └── wars/
        └── geoportal.war
        └── harvester.war
```

Copy media files into `docker/` from a backup:
*backup is available in 1Password*

```text
└── wcoa/
    └── docker/
        └── media/
            └── documents/
            └── group_images/
            └── images/
            └── original_images/
```

Build the core base image (first time or after core dependency changes):

```bash
task base
```

Build the WCOA overlay image:

```bash
task build
```

First boot with migrations, fixtures, and optional superuser creation:

```bash
task init
```

Open the portal:
- App: http://localhost:8000
- Geoportal: http://localhost:8080
- Elasticsearch: http://localhost:9200

*After the first boot, use:*

```bash
task up
```

Import database into the portal from a dump file:
*dump file is available in 1Password*

```bash
./scripts/db-restore.sh <dump_file.sql>
```

---  

## Day-to-day commands

```bash
task up          # Start stack
task down        # Stop stack
task logs        # Tail app logs
task shell       # Django shell
task manage -- migrate
task manage -- createsuperuser
```

## Docker structure in this repo

- `docker/Dockerfile` builds the WCOA overlay from `ghcr.io/ecotrust/madrona-portal`
- `docker/compose.yml` defines WCOA app plus `geoportal` and `elastic`
- `docker/config.wcoa.docker.ini` holds portal-level non-secret config
- `docker/.env` holds local secrets and environment-specific values

The app service uses:
- WCOA compose overlay (`docker/compose.yml`)
- Core compose base from `madrona-portal/docker/compose.base.yml`

The `Taskfile.yml` intentionally composes with the WCOA file first and core base second.
Keep that order to avoid path-resolution issues with bind mounts.

## Configuration notes

- `MP_PROJECT_CONFIG` points to `docker/config.wcoa.docker.ini` in-container
- Secrets should come from environment variables in `docker/.env`
- `docker/.env` is gitignored
- `DB_INIT=1` should be used only when intentionally initializing data

## Running the production-oriented compose file locally

This repo also includes `docker/compose.prod.yml` for image-based runs.
Published image tags include both `linux/amd64` and `linux/arm64`, so Docker will
pull the correct architecture automatically on Intel and Apple Silicon hosts.

Example:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

Optional dev profile services in that file:

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env --profile dev up -d
```

TODO: Add instructions for running production compose file in a cloud environment.
TODO: Media files dir might permissions changes.


## Troubleshooting

- If app startup fails, inspect logs:

```bash
task logs
```

- If Django commands fail due to schema state, re-run init once:

```bash
task down
task init
```

- If you changed only WCOA code/templates, `task up` is usually enough.
- If you changed Python dependencies in `docker/requirements.txt`, run `task build` again.
- If you changed shared core dependencies, rebuild base with `task base` and then `task build`.

## Legacy notes

Older Vagrant and manual server setup steps have been removed from this README.
Use Docker-based workflows described above and onboarding references for current development.