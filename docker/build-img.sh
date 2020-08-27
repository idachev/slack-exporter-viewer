#!/bin/bash
[ "$1" = -x ] && shift && set -x
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# set to fail if some command return error
set -e

DOCKER_TAG=slack-export-viewer:1.0

cd "${DIR}"

TARGET_DIR="${DIR}"/target

mkdir -p "${TARGET_DIR}"

rm -rf "${TARGET_DIR}"/src
rm -rf "${TARGET_DIR}"/slack-export-viewer

cp -a "${DIR}"/../src "${TARGET_DIR}"/
cp -a "${DIR}"/../slack-export-viewer "${TARGET_DIR}"/

echo -e "\nBuilding img: ${DOCKER_TAG}"
docker build --rm -t "${DOCKER_TAG}" -f "${DIR}"/Dockerfile .

echo -e "\nCleanup"
docker image prune --force

echo -e "\nGrep docker images"
docker images | grep "slack-export-viewer"
