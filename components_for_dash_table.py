import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


def split_array(choose_user_cities: list) -> list[list]:
    split_choose_user = []
    index = 0

    # Цикл, который берет по три элемента из списка
    while index < len(choose_user_cities):
        three_elements = choose_user_cities[index:index + 3]
        split_choose_user.append(three_elements)
        index += 3

    return split_choose_user


def progress_bar(progress_parsing: int, id_str: str):
    progress = html.Div(
        [
            dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
            dbc.Progress(id=f"{id_str}-progress", value=progress_parsing, striped=True, color='green'),
        ]
    )

    return progress


def check_toggle_switch(type_boolean: bool, id_str: str, value: bool) -> object:
    if type_boolean is True:
        return html.Div(
            [
                dbc.Switch(
                    id={'type': 'dynamic-switch', 'index': id_str},
                    # id=id,
                    label="switch-active",
                    value=value,
                ), html.Div(id='output-switch-active')
            ],
            className='toggle_switch_active',
        )
    return html.Div(
        [
            dbc.Switch(
                id={'type': 'dynamic-switch', 'index': id_str},
                # id={'type': 'dynamic-switch', 'index': id},
                label="switch-disabled",
                value=value,
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
                html.Td(check_toggle_switch(row['dodo'], f'{id}-0', row['dodo_value']), id="dodo-cell"),
                html.Td(check_toggle_switch(row['tashir'], f'{id}-1', row['tashir_value']), id="tashir-cell"),
                html.Td(check_toggle_switch(row['tomato'], f'{id}-2', row['tomato_value']), id="tomato-cell"),
            ]
        )
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3', size='sm')

    return table


def waiting_parsing(progress_parsing: int) -> object:
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Бренд", id="brands-city"),
                html.Th("Прогресс", id="progress-bar"),
            ]),
            className="header",
        ),
    ]

    brands = ['Додо', 'Ташир', 'Томато']

    table_rows = []
    for id, row in enumerate(brands):
        table_row = html.Tr(
            [
                html.Td(row, id="brand-cell"),
                html.Td(progress_bar(progress_parsing, f'{id}-0'), id="progress-cell"),
            ]
        )
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3', size='sm')

    return table
