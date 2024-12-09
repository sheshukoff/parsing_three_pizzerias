import time

from dash import html, Input, Output, dcc, State, set_props
import dash_bootstrap_components as dbc
from components_for_dash_table import waiting_parsing

from get_soup_from_city_dodo import parsing_dodo_pizza
from get_soup_from_city_tashir import parsing_tashir_pizza
from get_soup_from_city_tomato import parsing_tomato_pizza


def init_dash_table_waiting_parsing(dash_app):
    def calculate_percent(brand_cities: list) -> int:
        """
        Функция возвращает процент прироста для прогресс бар
        :param brand_cities: list
        :return: int
        """
        length_list = len(brand_cities)
        if length_list == 0:
            return 100

        return 100 // length_list

    def create_counter(start=0):
        """
        Функция создает счетчик и возврещает процент прироста прогресс бара
        :param start: int
        :return: int
        """
        count = [start]

        def counter(step):

            count[0] += step
            return count[0]

        return counter

    def is_last_element(element: str, any_list: list) -> bool:
        """
        Функция проверяет являится ли элемент последним в списке
        :param element: int
        :param any_list: list
        :return: bool
        """
        if element == any_list[-1]:
            return True
        return False

    def get_tuple_values(brands_values: dict) -> tuple[str, str, str, str, str, str]:
        """
        Функция возвращает кортеж (для прогресс бара)
        :param brands_values: dict
        :return: tuple
        """
        return (str(brands_values['Додо']), str(f'{brands_values['Додо']}%'),
                str(brands_values['Ташир']), str(f'{brands_values['Ташир']}%'),
                str(brands_values['Томато']), str(f'{brands_values['Томато']}%'))

    def definition_parsing(name_brand: str):
        """
        Функция определяет какой сейчас будет парсинг
        :param name_brand: str
        """
        if name_brand == 'Додо':
            parsing = parsing_dodo_pizza
        elif name_brand == 'Ташир':
            parsing = parsing_tashir_pizza
        elif name_brand == 'Томато':
            parsing = parsing_tomato_pizza
        else:
            raise f'нет такого бренда {name_brand}'

        return parsing

    @dash_app.callback(
        inputs=[Input('table_for_waiting_parsing', 'children')],
        state=[State('choose_cities_session', 'data'),
               State('count_percent_session', 'data')],
        progress=[Output("dodo-progress", "value"),
                  Output("dodo-progress", "label"),
                  Output("tashir-progress", "value"),
                  Output("tashir-progress", "label"),
                  Output("tomato-progress", "value"),
                  Output("tomato-progress", "label")],
        background=True,
    )
    def processing_waiting_parsing(update_progress, table: list, cities_for_parsing: dict, brands_values: dict):
        """
        Функция (здесь происходит ожидание парсинга)
        :param update_progress:
        :param table: list
        :param cities_for_parsing: int
        :param brands_values: dict
        """
        if brands_values is None:
            brands_values = {'Додо': 0, 'Ташир': 0, 'Томато': 0}

        for brand, cities in cities_for_parsing.items():
            count_percent = create_counter(0)
            percent_incremet = calculate_percent(cities)

            if len(cities) == 0:
                brands_values[brand] = 100
                update_progress(get_tuple_values(brands_values))

            for city in cities:
                parsing = definition_parsing(brand)
                parsing(brand, city)

                if is_last_element(city, cities):
                    now_percent = 100
                    print('70 row', now_percent)
                else:
                    now_percent = count_percent(percent_incremet)
                print(brand, now_percent)

                brands_values[brand] = now_percent
                update_progress(get_tuple_values(brands_values))
            time.sleep(2)

        set_props('subtotal-input', {'disabled': False})

    @dash_app.callback(
        Output('table_for_waiting_parsing', 'children'),
        Input('page-content', 'children'),
    )
    def get_table_waiting_parsing(table: object) -> object:
        """
        Функция строит таблицу 'ожидание парсинга'
        :param table: object
        :return: object
        """
        print('get_table_waiting_parsing')
        waiting_table = waiting_parsing()

        return waiting_table

    table_waiting_parsing = html.Div(
        children=[
            dcc.Store(id='now_brand_session', storage_type='session'),
            dcc.Store(id='choose_cities_session', storage_type='session'),
            dcc.Store(id='count_percent_session', storage_type='session'),
            dbc.Table(id='table_for_waiting_parsing'),
            html.Button('Промежуточный итог', id='subtotal-input', disabled=True),
        ],
        className="table-pagination",
    )

    return table_waiting_parsing
