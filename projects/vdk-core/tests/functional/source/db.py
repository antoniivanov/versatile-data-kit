# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0


def transform():
    pass


def run(job_input):
    db_connection = job_input.get_managed_connection()

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM p3")

    job_input.send_tabular_data_for_ingestion(
        transform(),
        column_names=[column_info[0] for column_info in cursor.description],
        destination_table="backup_employees",
    )
