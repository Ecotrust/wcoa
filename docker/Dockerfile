ARG BASE_IMAGE=ghcr.io/ecotrust/madrona-portal
ARG BASE_TAG=latest
FROM ${BASE_IMAGE}:${BASE_TAG}

# Build context is the wcoa repository root.
COPY --chown=madrona_user:madrona_user . ./apps/wcoa

RUN pip install --no-deps -e ./apps/wcoa && \
	if [ -s ./apps/wcoa/docker/requirements.txt ]; then \
		pip install -r ./apps/wcoa/docker/requirements.txt; \
	fi

ENV MP_PROJECT_CONFIG=/usr/local/apps/madrona-portal/apps/wcoa/docker/config.wcoa.docker.ini