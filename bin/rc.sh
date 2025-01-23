#!/usr/bin/env bash

set -x

CREATE_RELEASE=0
VIRTUAL_ENV_NAME=".venv"
DEFAULT_PACKAGE_VERSION="1.0.1"
HOME_PATH="${PWD}"
PROJECT_PATH="${HOME_PATH}/src/cloudhive"

#source "${VIRTUAL_ENV_NAME}/bin/activate"

commit_message="${1}"

function extract_message() {
    # filter - '(dev|release)-YYYY-qX.X.X'
    if [[ $commit_message =~ "^(dev|release)-([0-9]+)\.([0-9]+)\.(.+)$" ]]; then
        package_version=$(echo $package_version | cut -d '-' -f 2)
        CREATE_RELEASE=1
    fi
}

function change_version() {
    local filename=$1
    local version=$2
    sed -i "s/version = \".*\"/version = \"${version}\"/" $filename

}

if [[ "$GITHUB_ACTIONS" == "true" ]]; then
    echo "[ INFO ] Running in GitHub Actions"
    extract_message
    echo "Changing the version of the package cloudhive ${package_version}"
    change_version "${HOME_PATH}/pyproject.toml" "${package_version}"
    echo "[ INFO ] Package cloudhive has updated successfully!"
    cat "${HOME_PATH}/pyproject.toml"
fi

if [[ "$GITLAB_CI" == "true" ]]; then
    echo "Running in GitLab Runner"
fi

if [[ -z "$GITHUB_ACTIONS" && -z "$GITLAB_CI" ]]; then
    echo -e "[Warning] You are Running in Local Shell\n# -> Provide the version along with the script."
fi
