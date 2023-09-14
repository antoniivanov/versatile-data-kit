# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
from vdk.api.job_input import IJobInput


def run(job_input: IJobInput):
    job_input.set_all_properties({"test": "test"})
