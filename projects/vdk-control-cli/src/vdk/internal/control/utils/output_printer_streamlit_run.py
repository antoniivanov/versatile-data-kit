# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import sys

try:
    import streamlit as st
    import pandas as pd
    from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

    def print_table(file_path: str):
        data = pd.read_json(file_path)
        if len(data) > 0:
            # st.table(data)
            AgGrid(data)
        else:
            st.write("No Data Jobs.")

    if __name__ == "__main__":
        file_path = sys.argv[1]
        print_table(file_path)

except ImportError:
    pass
