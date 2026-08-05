# WCOA production rollout: Docker decoupling

This runbook covers the production rollout for the WCOA Docker decoupling work. It assumes the application is deployed from the WCOA repo using the image-based compose file in [docker/compose.prod.yml](../docker/compose.prod.yml).

## Goal

Ship the decoupled WCOA deployment so the portal runs from its own image and config while still using the shared Madrona base image.

## Recommended rollout order

1. Confirm the shared base image is ready.
2. Build and publish the WCOA overlay image.
3. Deploy the new image to production.
4. Verify the app, DB, and supporting services.
5. Roll back quickly if anything fails.

---

## 1. Prepare the release

### Confirm the base image

The WCOA overlay image depends on the shared Madrona base image published from the core repo.

Before rollout:

- Confirm the core image build completed successfully.
- Note the base image tag you want to use, preferably a pinned SHA or release tag rather than `latest`.
- Confirm the WCOA image build will use that base tag in the Docker build arguments.

### Confirm release content

Verify the following are ready:

- The WCOA repo branch or PR is merged or otherwise approved for production.
- The image workflow completed successfully.
- The production environment has the required secrets in its `.env` file.
- Any required WAR files and media assets are present in the deployment host.

---

## 2. Build and publish the WCOA image

The WCOA workflow publishes images to GHCR from [/.github/workflows/build-and-publish-image.yml](../.github/workflows/build-and-publish-image.yml).

### What to expect

The workflow publishes:

- `ghcr.io/ecotrust/wcoa:<short-sha>`
- `ghcr.io/ecotrust/wcoa:latest`

### Production recommendation

For production, prefer deploying a pinned SHA rather than `latest`.

Example:

```bash
# Example only: use the SHA from the successful workflow run
export IMAGE_TAG=<short-sha>
```

---

## 3. Prepare the production host

On the deployment host, make sure the production environment is ready.

### Required files

Ensure the host has:

- The production `.env` file with secrets and runtime settings
- The compose file at [docker/compose.prod.yml](../docker/compose.prod.yml)
- The production WCOA config file at `docker/config.wcoa.prod.ini` mounted by the container
- Static and media directories with correct permissions

Before first startup, create the Elasticsearch snapshot path expected by compose:

```bash
mkdir -p docker/backups/elasticsearch
chown -R "$(id -u)":"$(id -g)" docker/backups/elasticsearch
```

### Minimum environment values

At minimum confirm these values are present in the host `.env`:

```env
SECRET_KEY=...
DB_PASSWORD=...
REDIS_PASSWORD=...
DB_NAME=wcoa_docker_db
IMAGE_TAG=<short-sha>
DJANGO_SUPERUSER_PASSWORD=...
```

If this is the first production deployment after the decoupled rollout, set `DB_INIT=1` once for initial boot and data setup. After that, switch it back to `0`.

---

## 4. Deploy the new image

From the WCOA deployment directory, pull and recreate the stack.

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env pull
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

If this is the first boot or the database needs initialization:

```bash
DB_INIT=1 docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

After initialization, set `DB_INIT=0` in the environment and restart the app service if needed.

---

## 5. Verify the deployment

### Container health

```bash
docker compose -f docker/compose.prod.yml --env-file docker/.env ps
docker compose -f docker/compose.prod.yml --env-file docker/.env logs -f app
```

### Functional checks

Verify:

- The app responds on the expected host port.
- The portal loads without obvious errors.
- The database connection is healthy.
- Static and media files are served correctly.
- Geoportal and Elasticsearch are healthy if those services are part of the deployment.

If you have a smoke-test endpoint or a browser-based check, use it at this stage.

---

## 6. Roll back if needed

If the deployment shows problems, revert to the previous known-good image tag.

```bash
export IMAGE_TAG=<previous-good-sha>
docker compose -f docker/compose.prod.yml --env-file docker/.env pull
docker compose -f docker/compose.prod.yml --env-file docker/.env up -d
```

Keep the previous image tag recorded so rollback is fast.

---

## 7. Post-deploy notes

After the rollout is confirmed:

- Record the deployed image tag in the deployment notes.
- Capture the date, release SHA, and any config changes.
- Keep the previous image tag available for rollback until the next deployment is stable.
- If the rollout included a new database migration or fixture load, verify the data shape before removing the temporary initialization step.

---

## Quick checklist

- [ ] Core base image build succeeded
- [ ] WCOA image workflow succeeded
- [ ] Production `.env` is ready
- [ ] Image tag is pinned for production
- [ ] Containers pulled and recreated
- [ ] App, DB, and supporting services are healthy
- [ ] Rollback target is recorded
