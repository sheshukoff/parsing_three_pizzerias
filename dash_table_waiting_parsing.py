from dash import html, Input, Output, set_props, dcc, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from components_for_dash_table import waiting_parsing


def init_dash_table_waiting_parsing(dash_app):
    @dash_app.callback(
        Output('table_for_waiting_parsing', 'children'),
        Input('page-content', 'children')
    )
    def get_table_waiting_parsing(table):
        print('get_table_waiting_parsing')
        waiting_table = waiting_parsing()
        return waiting_table

    @dash_app.callback(
        Output("dodo-progress", "value"),
        Input("progress-interval", 'n_interval'),
    )
    def timer(dodo_progress):
        print('timer', dodo_progress)
        if dodo_progress is None:
            dodo_progress = 0

        progress = min(dodo_progress % 110, 100)

        if progress == 100:
            return 100

        return progress

    @dash_app.callback(
        [Input("dodo-progress", "value"),
         Input("tashir-progress", "value"),
         Input("tomato-progress", "value"),
         Input("progress-interval", 'n_interval'),
         Input("progress-interval", 'disabled')],
        State('now_brand_session', 'data'),
        prevent_initial_call=True,
    )
    def change_progress_bar(dodo_value, tahir_value, tomato_value, _, disabled, brand):
        if ctx.triggered_id == "dodo-progress":
            value = dodo_value
        elif ctx.triggered_id == "tashir-progress":
            value = tahir_value
        elif ctx.triggered_id == "tomato-progress":
            value = tomato_value
        else:
            raise PreventUpdate

        print('change_progress_bar', value)
        if brand is None:
            brand = 'dodo'
        value += 5

        if value <= 100:
            change_set_props(value, brand)
            print('change_set_props', value)
        else:
            if brand == 'dodo':
                brand = 'tashir'
            elif brand == 'tashir':
                brand = 'tomato'
            elif brand == 'tomato':
                brand = None

            if brand is None:
                set_props("progress-interval", {'disabled': True})
            else:
                print(brand)
                set_props('now_brand_session', {'data': brand})
                set_props(f"{brand}-progress", {'value': 0})

    def change_set_props(value, brand):
        set_props(f'{brand}-progress', {'value': value})
        set_props(f"{brand}-progress", {'label': f'{value}%'})

    # сделать set_props обычной функцией

    table_waiting_parsing = html.Div(
        children=[
            dcc.Store(id='now_brand_session', storage_type='session'),
            dcc.Store(id='choose_cities_session', storage_type='session'),
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
