#! /bin/bash

# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0

export VDK_PATCH_VERSION=2-rc1

hatch version 0.1.$VDK_PATCH_VERSION

rm -rf dist/*

python -m build

twine upload --repository-url $PIP_REPO_UPLOAD_URL -u "$PIP_REPO_UPLOAD_USER_NAME" -p "$PIP_REPO_UPLOAD_USER_PASSWORD" dist/* --verbose
