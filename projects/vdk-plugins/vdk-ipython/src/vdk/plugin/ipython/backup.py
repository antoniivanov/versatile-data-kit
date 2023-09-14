# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0


def prepare_result_cell_output_itables(result_df):
    from itables import show

    new_columns = [
        f"{col} ({str(dtype)})"
        for col, dtype in zip(result_df.columns, result_df.dtypes)
    ]
    result_df.columns = new_columns

    options = {"paging": True, "pageSize": 50, "lengthMenu": [10, 25, 50, 75, 100]}

    return show(result_df, options=options)


def prepare_result_cell_output_qgrid(result_df):
    import qgrid

    # Configure qgrid options
    qgrid_options = {
        "fullWidthRows": True,
        "syncColumnCellResize": True,
        "forceFitColumns": True,
        "rowHeight": 28,
        "enableColumnReorder": True,
        "enableTextSelectionOnCells": True,
        "editable": False,
        "autoEdit": False,
        "explicitInitialization": True,
        "maxVisibleRows": 15,
        "minVisibleRows": 8,
        "sortable": True,
        "filterable": True,
        "highlightSelectedCell": False,
        "highlightSelectedRow": True,
    }

    # Create qgrid widget
    qgrid_widget = qgrid.show_grid(result_df, grid_options=qgrid_options)

    return qgrid_widget


def prepare_result_cell_output_beakerx(result_df):
    from beakerx import TableDisplay

    columns = [
        {"field": col, "type": str(result_df[col].dtype)} for col in result_df.columns
    ]

    table_display = TableDisplay(
        result_df,
        columnNames=[col["field"] for col in columns],
        types=[col["type"] for col in columns],
        showRowNumbers=False,
    )

    table_display.setStringFormatForTimes("%Y-%m-%d %H:%M:%S")
    table_display.setStringFormatForType("double", TableDisplay.StringFormat("%.3f"))
    table_display.setStringFormatForColumn(
        "column_name", "%.3f"
    )  # Replace "column_name" with the actual column name

    return table_display
