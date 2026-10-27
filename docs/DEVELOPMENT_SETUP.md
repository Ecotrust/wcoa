# WCOA Development Environment Setup

This is a guide to running a local WCOA portal. The local stack builds the shared Madrona base and WCOA portal overlay. mp-\* and madrona-\* repos are bind-mounts for development.

## Prerequisites

- Docker Desktop or Docker Engine with the Compose v2 plugin
- [go-task](https://taskfile.dev/installation/) (`brew install go-task` on macOS)
- Access to the WCOA development WAR artifacts (`geoportal.war` and `harvester.war`) and, optionally, a local media archive.

## Clone the workspace

Keep `madrona-portal` and `madrona-apps` as siblings. Taskfile and Compose files depend on relative paths.

### Suggested structure

Make a portals directory to contain both `madrona-portal` and `madrona-apps`. Clone `madrona-portal` and make the `madrona-apps` dir:

```bash
mkdir -p portals
cd portals
mkdir -p madrona-apps
git clone https://github.com/Ecotrust/madrona-portal.git
```

Inside `madrona-apps`, clone the WCOA repository and every shared app mounted by the local stack or copied into the base image:

```bash
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

The result should include `madrona-portal/` and `madrona-apps/wcoa/`, with the shared apps alongside WCOA under `madrona-apps/`.

To update the checkouts later, pull the platform and the repositories used by this stack:

```bash
git -C ../madrona-portal pull --ff-only
for repo in wcoa django_url_shortener madrona-analysistools madrona-features madrona-manipulators madrona-scenarios mp-accounts mp-data-manager mp-drawing mp-explore mp-layers mp-map-groups mp-proxy mp-survey mp-visualize p97-nursery; do
  git -C "$repo" pull --ff-only
done
```

## Add WCOA artifacts

Run from `madrona-apps/wcoa`:

```bash
mkdir -p docker/wars docker/static docker/media docker/backups/sql docker/backups/elasticsearch
```

Place the two WAR files at the paths expected by the development environment:

```text
docker/wars/geoportal.war
docker/wars/harvester.war
```

Obtain these private artifacts from the team's 1Password vault (ask a portal maintainer for the item if you do not have access). Copy a development media archive into `docker/media/`.

## Configure local services

Create the local environment file:

```bash
cp docker/.env.example docker/.env
```

Set local-only values for `SECRET_KEY`, `DB_PASSWORD`, `REDIS_PASSWORD`, `ELASTIC_PASSWORD`, and `DJANGO_SUPERUSER_PASSWORD` in `docker/.env`. Generate random values with:

```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

Do not reuse production credentials or commit `docker/.env`. The template enables Django development settings. The app is available on port `8000`, Geoportal on `8080`, and Elasticsearch on `9200`.

*Please Note*:
* The template uses Django development settings and reCAPTCHA test keys. 
* WCOA is available on port `8000` (http://localhost:8000)
* Database host port defaults to `5433`.
* Geoportal is available on `8080`
* Elasticsearch is available on `9200`
  
## Build and start

From the WCOA repository root, build the shared base image and WCOA development image, then initialize a new database:

```bash
task build-base
task build-portal
```
### Do you have a database to import?

<details>
<summary><strong>Yes</strong>, I have a database to import</summary>

```bash
task up
```

This might take a minute, but after `task up` the dev stack should be running and you can detatch or open a new terminal and run:

```bash
scripts/db-restore.sh /path/to/mida-dump.sql
task manage -- migrate
task manage -- compress
task manage -- collectstatic
```

The `db-restore.sh` script imports a SQL file into the Docker `db` service.  

</details>

<details>
<summary><strong>No</strong>, I do not have a database to import</summary>

```bash
task init
```

`task init` runs the application entrypoint with `DB_INIT=1`; use it only for a fresh development database. Once initialized, start the stack with `task up`. These tasks run Compose attached to the terminal; use `task down` to stop and remove the containers while preserving named database volumes.

</details>

---  

Open <http://localhost:8001/>


## Taskfile commands

Run tasks from the WCOA repository root. `task --list` shows the current descriptions:

| Command | Purpose |
| --- | --- |
| `task build-base` | Builds a madrona-portal image – *Run initially and when shared dependencies change* |
| `task build-portal` | Build the WCOA dev image – *Run initially and when dependencies change* |
| `task up` | Starts the stack (Docker up) |
| `task down` | Stops the stack (Docker down) |
| `task logs` | Follow app container logs (Docker logs) |
| `task manage -- migrate` | Run a Django management command in the app container |
| `task shell` | Open the Django shell in the app container |
| `task init` | Initialize a fresh database and start the stack |

## Troubleshooting and tips

- If the app port is occupied, change `APP_PORT` in `docker/.env`
- After changing a Python dependency in `docker/requirements.txt`, run `task build-portal` again
- After shared dependency changes, run `task build-base` followed by `task build-portal`