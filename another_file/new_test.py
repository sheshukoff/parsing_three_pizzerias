import time
import dash
from dash import html, dcc, Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager
import plotly.graph_objects as go
import multiprocess
## Diskcache
import diskcache
import dash_bootstrap_components as dbc
from components_for_dash_table import waiting_parsing

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)


def make_progress_graph(progress, total):
    progress_graph = (
        go.Figure(data=[go.Bar(x=[progress])])
        .update_xaxes(range=[0, total])
        .update_yaxes(
            showticklabels=False,
        )
        .update_layout(height=100, margin=dict(t=20, b=40))
    )
    return progress_graph


def progress_bar(brand: str):
    progress = html.Div(
        [
            dcc.Interval(id="progress-interval", n_intervals=0, interval=2000),
            dbc.Progress(id=f"{brand}-progress", color='#ffffff'),
        ]
    )

    return progress


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE], long_callback_manager=long_callback_manager)

app.layout = html.Div(
        html.Div(
            [
                html.P(id="paragraph_id", children=["Button not clicked"]),
                dcc.Graph(id="progress_bar_graph", figure=make_progress_graph(0, 10)),
            ]
        ),
        html.Button(id="button_id", children="Run Job!"),
        html.Button(id="cancel_button_id", children="Cancel Running Job!"),
)

# table = waiting_parsing()
#
# create_table = dbc.Table(id='table_for_waiting_parsing'),
#
# dash_app.layout = html.Div(
#     children=[
#         table,
#         dbc.Table(id='table_for_waiting_parsing')
#     ]
# )


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


# Input("dodo-progress", "value"),
# Input("tashir-progress", "value"),
# Input("tomato-progress", "value"),
# @dash_app.long_callback(
#     inputs={
#         "all_inputs": {
#             "dodo_progress": Input("btn-1", "n_clicks"),
#             "tashir_progress": Input("btn-2", "n_clicks"),
#             "tomato_progress": Input("btn-3", "n_clicks")
#         }
#     },
#     output=Output("dodo-progress", "value"),
#     # inputs=Input("table_for_waiting_parsing", "children"),
#     # running=[
#     #     (Output("button_id", "disabled"), True, False),
#     #     (Output("cancel_button_id", "disabled"), False, True),
#     #     (
#     #             Output("paragraph_id", "style"),
#     #             {"visibility": "hidden"},
#     #             {"visibility": "visible"},
#     #     ),
#     #     (
#     #             Output("progress_bar_graph", "style"),
#     #             {"visibility": "visible"},
#     #             {"visibility": "hidden"},
#     #     ),
#     # ],
#     # cancel=[Input("cancel_button_id", "n_clicks")],
#     progress=Output("progress_bar_graph", "figure"),
#     progress_default=make_progress_graph(0, 100),
#     interval=1000,
# )
# def callback(set_progress, n_clicks):
#     brands = {'Додо': ['Воронеж', 'Белгород', 'Калуга', 'Москва', 'Ростов', 'Аскай'],
#               'Ташир': [],
#               'Томато': ['Воронеж', 'Белгород', 'Калуга', 'Москва']}
#
#     for brand, cities in brands.items():
#         count_percent = create_counter(0)
#         percent_incremet = calculate_percent(cities)
#
#         if percent_incremet == 100:
#             set_progress(make_progress_graph(percent_incremet, 100))
#         for city in cities:
#             if is_last_element(city, cities):
#                 now_percent = 100
#             else:
#                 now_percent = count_percent(percent_incremet)
#
#             set_progress(make_progress_graph(now_percent, 100))
#             time.sleep(2)
#
#     # total = 10
#     # for i in range(total):
#     #     time.sleep(0.5)
#     #     set_progress(make_progress_graph(i, 10))
#
#     return [f"Clicked {n_clicks} times"]


# @app.long_callback(
#     output=Output("paragraph_id", "children"),
#     inputs=Input("button_id", "n_clicks"),
#     running=[
#         (Output("button_id", "disabled"), True, False),
#         (Output("cancel_button_id", "disabled"), False, True),
#         (
#                 Output("paragraph_id", "style"),
#                 {"visibility": "hidden"},
#                 {"visibility": "visible"},
#         ),
#         (
#                 Output("progress_bar_graph", "style"),
#                 {"visibility": "visible"},
#                 {"visibility": "hidden"},
#         ),
#     ],
#     cancel=[Input("cancel_button_id", "n_clicks")],
#     progress=Output("progress_bar_graph", "figure"),
#     progress_default=make_progress_graph(0, 100),
#     interval=1000,
# )
# def callback(set_progress, n_clicks):
#     brands = {'Додо': ['Воронеж', 'Белгород', 'Калуга', 'Москва', 'Ростов', 'Аскай'],
#               'Ташир': [],
#               'Томато': ['Воронеж', 'Белгород', 'Калуга', 'Москва']}
#
#     for brand, cities in brands.items():
#         count_percent = create_counter(0)
#         percent_incremet = calculate_percent(cities)
#
#         if percent_incremet == 100:
#             set_progress(make_progress_graph(percent_incremet, 100))
#         for city in cities:
#             if is_last_element(city, cities):
#                 now_percent = 100
#             else:
#                 now_percent = count_percent(percent_incremet)
#
#             set_progress(make_progress_graph(now_percent, 100))
#             time.sleep(2)
#
#     # total = 10
#     # for i in range(total):
#     #     time.sleep(0.5)
#     #     set_progress(make_progress_graph(i, 10))
#
#     return [f"Clicked {n_clicks} times"]


if __name__ == "__main__":
    app.run(debug=True)
