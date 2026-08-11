#!/usr/bin/env bash

set -euo pipefail

REPOSITORY=""
ELASTIC_URL="${ELASTIC_URL:-http://localhost:9200}"

usage() {
	cat <<EOF
Usage: $(basename "$0") -r <repository> [-u <elastic_url>]

Options:
	-r <repository>   Elasticsearch snapshot repository name (required)
	-u <elastic_url>  Elasticsearch base URL (default: http://localhost:9200)
	-h                Show this help
EOF
}

while getopts ":r:u:h" opt; do
	case "$opt" in
		r) REPOSITORY="$OPTARG" ;;
		u) ELASTIC_URL="$OPTARG" ;;
		h)
			usage
			exit 0
			;;
		:) echo "Error: Option -$OPTARG requires an argument." >&2; usage; exit 1 ;;
		\?) echo "Error: Invalid option -$OPTARG" >&2; usage; exit 1 ;;
	esac
done

if [[ -z "$REPOSITORY" ]]; then
	echo "Error: -r <repository> is required" >&2
	exit 1
fi

DATETIME_VAR="$(date +%Y%m%d_%H%M)"
SNAPSHOT_NAME="snapshot_${DATETIME_VAR}"

curl --fail --silent --show-error \
	-X PUT "${ELASTIC_URL}/_snapshot/${REPOSITORY}/${SNAPSHOT_NAME}" \
	-H 'Content-Type: application/json' \
	-d '{"indices": "metadata_v1", "ignore_unavailable": true, "include_global_state": false}'

echo "Created Elasticsearch snapshot ${SNAPSHOT_NAME} in repository ${REPOSITORY}"
