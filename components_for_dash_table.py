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
    style={'margin-left': '40%'},
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
    style={'margin-left': '40%'},
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
                html.Th("Города",
                        style={'width': '30%', 'text-transform': 'uppercase'}),
                html.Th("Додо",
                        style={'width': '10%', 'text-transform': 'uppercase'}),
                html.Th("Ташир",
                        style={'width': '10%', 'text-transform': 'uppercase'}),
                html.Th("Томато",
                        style={'width': '10%', 'text-transform': 'uppercase'}),
            ]),
            style={'font-family': 'Lobster', 'text-align': 'center'}
        )
    ]

    table_rows = []
    for row in part_table:
        table_row = html.Tr([
            html.Td(row['city'], style={'width': '30%', 'font-size': '16px'}),
            html.Td(check_toggle_switch(row['dodo']), style={'width': '10%'}),
            html.Td(check_toggle_switch(row['tashir']), style={'width': '10%'}),
            html.Td(check_toggle_switch(row['tomato']), style={'width': '10%'}),
        ])
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3', size='sm')

    return table
