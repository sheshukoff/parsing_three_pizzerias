from dash import html, Input, Output, set_props, dcc, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from components_for_dash_table import waiting_parsing
import time


def init_dash_table_waiting_parsing(dash_app):
    def calculate_percent(brand_cities: list) -> int:
        length_list = len(brand_cities)
        if length_list == 0:
            return 100

        return 100 // length_list

    def create_counter(start=0):
        count = [start]  # используем список для хранения состояния

        def counter(step):
            count[0] += step  # увеличиваем счетчик на заданное значение
            return count[0]  # возвращаем текущее значение счетчика

        return counter

    def is_last_element(element: str, any_list: list) -> bool:
        if element == any_list[-1]:
            return True
        return False

    def get_tuple_values(brands_values: dict) -> tuple[str, str, str]:
        return str(brands_values['Додо']), str(brands_values['Ташир']), str(brands_values['Томато'])

    def update_percent_brand(brand: str, brands_values: dict, percent: int) -> tuple:
        # if brand == 'Додо':
        #     count_percent_brand[brand] = percent
        # elif brand == 'Ташир':
        #     count_percent_brand[brand] = percent
        # elif brand == 'Томато':
        #     count_percent_brand[brand] = percent

        return brands_values['Додо'], brands_values['Ташир'], brands_values['Томато']

    @dash_app.long_callback(
        inputs=[Input('table_for_waiting_parsing', 'children')],
        state=[State('choose_cities_session', 'data'),
               State('count_percent_session', 'data')],
        progress=[Output("dodo-progress", "value"),
                  Output("tashir-progress", "value"),
                  Output("tomato-progress", "value")]
    )
    def processing_waiting_parsing(update_progress, table, cities_for_parsing, brands_values):
        print('processing_waiting_parsing',
              f"""
              update_progress -> {update_progress}
              table -> {table}
              cities_for_parsing -> {cities_for_parsing}
              count_percent_brand -> {brands_values}
              """)
        if brands_values is None:
            brands_values = {'Додо': 0, 'Ташир': 0, 'Томато': 0}

        for brand, cities in cities_for_parsing.items():
            count_percent = create_counter(0)
            percent_incremet = calculate_percent(cities)

            if percent_incremet == 100:
                brands_values[brand] = percent_incremet
                update_progress(get_tuple_values(brands_values))

            for city in cities:
                time.sleep(3)  # парсинг "Функция"
                if is_last_element(city, cities):  # можно сделать функицю "Обновление прогресс бара"
                    now_percent = 100
                    print('70 row', now_percent)
                else:
                    now_percent = count_percent(percent_incremet)
                print(brand, now_percent)

                brands_values[brand] = now_percent
                update_progress(get_tuple_values(brands_values))

    @dash_app.callback(
        Output('table_for_waiting_parsing', 'children'),
        Input('page-content', 'children'),
    )
    def get_table_waiting_parsing(table):
        print('get_table_waiting_parsing')
        waiting_table = waiting_parsing()

        return waiting_table

    # @dash_app.callback(
    #     Input('table_for_waiting_parsing', 'children'),
    #     State('choose_cities_session', 'data')
    # )
    # def(table, cities_for_parsing):
    #     print('')

    # @dash_app.callback(
    #     Output("dodo-progress", "value"),
    #     Input("progress-interval", 'n_interval'),
    # )
    # def timer(dodo_progress):
    #     print('timer', dodo_progress)
    #     if dodo_progress is None:
    #         dodo_progress = 0
    #
    #     progress = min(dodo_progress % 110, 100)
    #
    #     if progress == 100:
    #         return 100
    #
    #     return progress

    # @dash_app.callback(
    #     Input()
    #     Input('now_brand_session', 'data'),
    #     prevent_initial_call=True,
    # )
    # def change_progress_bar(dodo_value, tahir_value, tomato_value, brand):
    #     if ctx.triggered_id == "dodo-progress":
    #         value = dodo_value
    #     elif ctx.triggered_id == "tashir-progress":
    #         value = tahir_value
    #     elif ctx.triggered_id == "tomato-progress":
    #         value = tomato_value
    #     else:
    #         raise PreventUpdate
    #
    #     if brand is None:
    #         brand = 'dodo'
    #     value += 5

    # @dash_app.callback(
    #     [Input("dodo-progress", "value"),
    #      Input("tashir-progress", "value"),
    #      Input("tomato-progress", "value"),
    #      Input("progress-interval", 'n_interval'),
    #      Input("progress-interval", 'disabled')],
    #     prevent_initial_call=True,
    # )
    # def change_progress_bar(dodo_value, tahir_value, tomato_value, _, disabled):
    #     if ctx.triggered_id == "dodo-progress":
    #         value = dodo_value
    #         brand = 'dodo'
    #     elif ctx.triggered_id == "tashir-progress":
    #         value = tahir_value
    #         brand = 'tashir'
    #     elif ctx.triggered_id == "tomato-progress":
    #         value = tomato_value
    #         brand = 'tomato'
    #     else:
    #         raise PreventUpdate
    #
    #     print('change_progress_bar', value)
    #     # if brand is None:
    #     #     brand = 'dodo'
    #     # value += 5
    #
    #     if value <= 100:
    #         change_set_props(value, brand)
    #         print('change_set_props', value)

    # else:
    # if brand == 'dodo':
    #     brand = 'tashir'
    # elif brand == 'tashir':
    #     brand = 'tomato'
    # elif brand == 'tomato':
    #     brand = None

    # if brand is None:
    #     set_props("progress-interval", {'disabled': True})
    # else:
    #     print(brand)
    #     set_props('now_brand_session', {'data': brand})
    #     set_props(f"{brand}-progress", {'value': 0})

    # сделать set_props обычной функцией

    table_waiting_parsing = html.Div(
        children=[
            dcc.Store(id='now_brand_session', storage_type='session'),
            dcc.Store(id='choose_cities_session', storage_type='session'),
            dcc.Store(id='count_percent_session', storage_type='session'),
            dbc.Table(id='table_for_waiting_parsing'),
            html.Button('Промежуточный итог', id='subtotal-input'),
        ],
        className="table-pagination",
    )

    return table_waiting_parsing

# https://community.plotly.com/t/asynchronous-logic-progress-bar-update/43869/5


# dcc.Store now_percent

# Начало процесса парсинга от table_for_waiting_parsing


# def parsing_brand():
#
# def parsing():
#     for brand in brands:
#         parsing_brand()
#         percent_incremet = calculate_percent(cities_brand)  # 20 -> 5
#         now_percent = increment_percent(percent_incremet)
#         change_progress_bar(now_percent, brand)
#         # Пауза для симуляции (обновлять информацию раз в минуту)
#
# def calculate_percent(cities_brand: list): -> int  # вычисляет процент приращения изменения прогресса в зависимости
# от количества городов
#     # если len(cities_brand) = 0, то 100 %
#
# def is_last_incremet(): -> bool  # Определяет является ли текущий инкремент последним
#
# def increment_percent(percent_incremet: int): -> int  # Увеличивает процент на число приращения
#     if is_last_incremet():
#         return 100
#
# # Как запускать эту функцию
# Input(dcc.Store now_percent)
# Output('dodo_progress', 'value')
# Output('dodo_progress', 'label')
# def change_progress_bar(now_percent: int, brand: ?)  # Отображает изменение прогрессбара на страницце
#     return value, label

# Условие окончания парсинга
# Все перечисленное выше (функция должна работать до тех пор пока прогрессия не будет равна 100%)

# как изменить свойство компонета component_property


# progress = min(dodo_progress % 110, 100)
#
# if progress == 100:
#     return 100, '100%', not disabled_dodo
#
# return progress, f"{progress} %" if progress >= 5 else "", False
