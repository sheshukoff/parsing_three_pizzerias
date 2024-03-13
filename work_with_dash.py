from sort_cities import sorted_brand_and_cities

from dash import Dash, dash_table, dcc, html, Input, Output, callback
import dash_ag_grid as dag
import dash_daq as daq
from flask import Flask
import pandas as pd


def index():
    # возвращаем приветственное сообщение
    return "Hello, world!"


# создаем экземпляр приложения flask
flask_app = Flask(__name__)

# создаем экземпляр приложения dash, используя сервер flask
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/table/')

# switch_active = daq.BooleanSwitch(
#     on=True,
#     color="#9B51E0",
# )
#
# switch_disable = daq.BooleanSwitch(
#     disabled=True,
#     labelPosition="bottom"
# )
#
#
# @callback(
#     Output('boolean-switch-output-1', 'children'),
#     Input('my-boolean-switch', 'on')
# )
# def update_output(on):
#     return on


# определяем данные для таблицы в виде списка словарей
data_frame = sorted_brand_and_cities()

data = []

for city, brands in data_frame.items():
    dodo, tashir, tomato = brands
    # print(dodo, tashir, tomato)

    data.append({'city': city, 'dodo': dodo, 'tashir': tashir, 'tomato': tomato}, )

# определяем столбцы для таблицы в виде списка словарей
columns = [
    {'name': 'Города', 'id': 'city'},
    {'name': 'Додо', 'id': 'dodo'},
    {'name': 'Ташир', 'id': 'tashir'},
    {'name': 'Томато', 'id': 'tomato'},
]

dash_app.layout = html.Div(
    [
        # daq.BooleanSwitch(on=True, color="#9B51E0"),
        # daq.BooleanSwitch(disabled=True, labelPosition="bottom"),
        # html.Div(id='boolean-switch-output-1'),
        dash_table.DataTable(
            data=data,
            columns=columns,
            page_action="native",
            page_current=0,
            page_size=20,
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold', 'border': '1px solid black'},
            style_table={'height': '670px', 'overflowY': 'auto', 'width': '70%', 'margin': 'auto'},
            style_cell={'padding': '5px', 'fontSize': 14, 'font-family': 'Lobster', 'color': '#92badd',
                        'textAlign': 'center', 'border': '1px solid grey'},
            style_cell_conditional=[
                {'if': {'column_id': 'Города'},
                 'width': '30%'},
                {'if': {'column_id': 'Додо'},
                 'width': '10%'},
                {'if': {'column_id': 'Ташир'},
                 'width': '10%'},
                {'if': {'column_id': 'Томато'},
                 'width': '10%'},
            ],
        )
    ]
)

# создаем компонент dash_table и добавляем его в макет приложения dash
# dash_app.layout = dash_table.DataTable(
#     data=data,
#     columns=columns,
#     page_action="native",
#     page_current=0,
#     page_size=20,
#     style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},
#     style_table={'height': '670px', 'overflowY': 'auto', 'width': '70%', 'margin': 'auto'},
#     style_cell={'padding': '5px', 'fontSize': 14, 'font-family': 'Lobster', 'color': '#92badd', 'textAlign': 'center'},
#     style_cell_conditional=[
#         {'if': {'column_id': 'Города'},
#             'width': '30%'},
#         {'if': {'column_id': 'Додо'},
#             'width': '10%'},
#         {'if': {'column_id': 'Ташир'},
#             'width': '10%'},
#         {'if': {'column_id': 'Томато'},
#             'width': '10%'},
#         # {
#         #     'if': {
#         #         "headerName": "Додо",
#         #         "field": "boolean",
#         #         "cellEditor": "agSelectCellEditor",
#         #         "cellEditorParams": {
#         #          "values": ['+']}
#         #     },
#         #     'cellEditor': switch_active
#         # },
#         # {
#         #     "headerName": "Select Editor",
#         #     "field": "color",
#         #     "cellEditor": "agSelectCellEditor",
#         #     "cellEditorParams": {
#         #         "values": ["red", "yellow", "green"],
#         #     },
#     ],
# )


# добавляем путь к главной странице
flask_app.add_url_rule("/", "index", index, methods=["GET"])

# запускаем приложение flask, если файл запущен как основная программа
# if __name__ == "__main__":
    # flask_app.run(debug=True)
