import dash_bootstrap_components as dbc
from dash import html


toggle_switch_active = html.Div(
    [
        dbc.Switch(
            id="active-switches-input",
            value=False,
        ),
    ],
    className='toggle_switch_active',
)

toggle_switch_disabled = html.Div(
    [
        dbc.Switch(
            id="disabled-switches-input",
            value=False,
            disabled=True,
        ),
    ],
    className='toggle_switch_disabled',
)


def check_toggle_switch(type_boolean: bool):
    if type_boolean is True:
        return toggle_switch_active
    return toggle_switch_disabled


def get_total_page(page_size, total_data):
    data_div_page_size = total_data // page_size
    data_mod_page_size = total_data % page_size
    total_page = data_div_page_size if data_mod_page_size == 0 else (data_div_page_size + 1)

    return total_page


def get_data_pagination(part_table):
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Города"),
                html.Th("Додо"),
                html.Th("Ташир"),
                html.Th("Томато"),
            ])
        )
    ]

    table_rows = []
    for row in part_table:
        table_row = html.Tr([
            html.Td(row['city']),
            html.Td(check_toggle_switch(row['dodo'])),
            html.Td(check_toggle_switch(row['tashir'])),
            html.Td(check_toggle_switch(row['tomato'])),
        ])
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3')

    return table
