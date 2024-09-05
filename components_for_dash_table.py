import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


def split_array(choose_user_cities: list) -> list[list]:
    """
    Функция разбивает список на три элемента, (возвращает список)
    :param choose_user_cities: list
    :return: list
    """
    split_choose_user = []
    index = 0

    # Цикл, который берет по три элемента из списка
    while index < len(choose_user_cities):
        three_elements = choose_user_cities[index:index + 3]
        split_choose_user.append(three_elements)
        index += 3

    return split_choose_user


def progress_bar(brand: str) -> object:
    """
    Функция возвращает объект прогресс бар
    :param brand: str
    :return: object
    """
    progress = html.Div(
        [
            dcc.Interval(id="progress-interval", n_intervals=0, interval=2000),
            dbc.Progress(id=f"{brand}-progress", color='#ffffff'),
        ]
    )

    return progress


def check_toggle_switch(type_boolean: bool, id_str: str, value: bool) -> object:
    """
    Функция проверяет включен ли переключатель
    :param type_boolean: str
    :param id_str: str
    :param value: bool
    :return: object
    """
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
    """
    Функция возращает количество страниц
    :param page_size: int
    :param total_data: int
    :return: int
    """
    data_div_page_size = total_data // page_size
    data_mod_page_size = total_data % page_size
    total_page = data_div_page_size if data_mod_page_size == 0 else (data_div_page_size + 1)

    return total_page


def get_data_pagination(part_table: list) -> object:
    """
    Функция стоит таблицу выбора бренда и городов (page_input)
    :param part_table: list
    :return: object
    """
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


def waiting_parsing() -> object:
    """
    Функция стоит таблицу ожидание парсинга (waiting_parsing)
    :return: object
    """
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Бренд", id="brands-city"),
                html.Th("Прогресс", id="progress-bar"),
            ]),
            className="header",
        ),
    ]

    brands = {'Додо': 'dodo', 'Ташир': 'tashir', 'Томато': 'tomato'}

    table_rows = []
    for name_brand, id_name_brand in brands.items():
        table_row = html.Tr(
            [
                html.Td(name_brand, id="brand-cell"),
                html.Td(progress_bar(id_name_brand), id=f"row-progress-{id_name_brand}"),
            ]
        )
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3', size='sm')

    return table
