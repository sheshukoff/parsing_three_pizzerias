import dash_bootstrap_components as dbc
from dash import html

toggle_switch_active = html.Div(
    [
        dbc.Switch(
            id="active-switches-input",
            label="switch",
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


def check_toggle_switch(type_boolean: bool) -> object:
    if type_boolean is True:
        return toggle_switch_active
    return toggle_switch_disabled


def get_total_page(page_size: int, total_data: int) -> int:
    data_div_page_size = total_data // page_size
    data_mod_page_size = total_data % page_size
    total_page = data_div_page_size if data_mod_page_size == 0 else (data_div_page_size + 1)

    return total_page


def get_data_pagination(part_table) -> object:
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Города", id="header-city"),
                html.Th("Додо", id="header-dodo"),
                html.Th("Ташир", id="header-tashir"),
                html.Th("Томато", id="header-tomato"),
            ]),
            className="header",
        ),
    ]

    table_rows = []
    for row in part_table:
        table_row = html.Tr(
            [
                html.Td(row['city'], id="city-cell"),
                html.Td(check_toggle_switch(row['dodo']), id="dodo-cell"),
                html.Td(check_toggle_switch(row['tashir']), id="tashir-cell"),
                html.Td(check_toggle_switch(row['tomato']), id="tomato-cell"),
            ]
        )
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3', size='sm')

    return table
