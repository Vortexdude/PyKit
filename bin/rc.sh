#!/usr/bin/env bash

set -x

VIRTUAL_ENV_NAME=".venv"
DEFAULT_PACKAGE_VERSION="1.0.1"
HOME_PATH="${PWD}"
PROJECT_PATH="${HOME_PATH}/src/cloudhive"

#source "${VIRTUAL_ENV_NAME}/bin/activate"

package_version=${1:-DEFAULT_PACKAGE_VERSION}

echo $package_version

if [[ "$GITHUB_ACTIONS" == "true" ]]; then
    echo "Running in GitHub Actions"
fi

if [[ "$GITLAB_CI" == "true" ]]; then
    echo "Running in GitLab Runner"
fi

if [[ -z "$GITHUB_ACTIONS" && -z "$GITLAB_CI" ]]; then
    echo "Running in Local Shell"
fi

