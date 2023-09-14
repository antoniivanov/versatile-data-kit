# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import json
from typing import Any
from typing import Dict
from typing import List

from vdk.internal.control.utils import output_printer_streamlit_run
from vdk.internal.control.utils.output_printer import Printer
from vdk.internal.control.utils.output_printer import printer

try:
    import streamlit as st
    import pandas as pd

    @printer("streamlit")
    class __PrinterStreamlit(Printer):
        def print_table(self, table: List[Dict[str, Any]]):
            import tempfile

            fd, path = tempfile.mkstemp(suffix=".json", dir="/tmp")
            with open(fd, "w+t") as f:
                json.dump(table, f)

            import subprocess

            subprocess.call(
                [
                    "streamlit",
                    "run",
                    "--browser.serverAddress=0.0.0.0",
                    output_printer_streamlit_run.__file__,
                    "--",
                    path,
                ]
            )

except ImportError as e:
    print(e)
    pass
