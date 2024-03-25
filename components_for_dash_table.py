import dash_bootstrap_components as dbc
from dash import html


def check_toggle_switch(type_boolean: bool, id: str) -> object:
    if type_boolean is True:
        return html.Div(
            [
                dbc.Switch(
                    id={'type': 'dynamic-switch', 'index': id},
                    # id=id,
                    label="switch-active",
                    value=False,
                ), html.Div(id='output-switch-active')
            ],
            className='toggle_switch_active',
        )
    return html.Div(
        [
            dbc.Switch(
                id=id,
                # id={'type': 'dynamic-switch', 'index': id},
                label="switch-disabled",
                value=False,
                disabled=True,
            ), html.Div(id='output-switch-disabled')
        ],
        className='toggle_switch_disabled',
    )


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
    for id, row in enumerate(part_table):
        table_row = html.Tr(
            [
                html.Td(row['city'], id="city-cell"),
                html.Td(check_toggle_switch(row['dodo'], f'{id}-0'), id="dodo-cell"),
                html.Td(check_toggle_switch(row['tashir'], f'{id}-1'), id="tashir-cell"),
                html.Td(check_toggle_switch(row['tomato'], f'{id}-2'), id="tomato-cell"),
            ]
        )
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3', size='sm')

    return table
