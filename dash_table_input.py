import dash_bootstrap_components as dbc
from dash import html, Input, Output, ALL, State, dcc, no_update
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page, split_array

PAGE_SIZE = 15
previous_page = 1


def init_dash_table(flask_app):
    dash_app = dash.Dash(__name__,
                         server=flask_app,
                         title="Checklist Test",
                         suppress_callback_exceptions=True,
                         external_stylesheets=[dbc.themes.SLATE],
                         routes_pathname_prefix='/dash/'
                         )
    return dash_app


def init_dash_table_input(dash_app, page_size, dash_page_output):
    @dash_app.callback(
        Output('container-output-text', 'children'),
        Input('pagination', 'active_page'),
        State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
    )
    def choose_brand_and_cities(number_page: int, choose_user_cities: list):
        global previous_page

        if number_page is None:
            number_page = 1

        start = (previous_page - 1) * page_size
        split_choose_user = split_array(choose_user_cities)  # разбито на три

        for number, values in enumerate(split_choose_user):
            dodo_value, tashir_value, tomato_value = values

            data[start + number]['dodo_value'] = dodo_value
            data[start + number]['tashir_value'] = tashir_value
            data[start + number]['tomato_value'] = tomato_value

        previous_page = number_page

        return ''

    @dash_app.callback(
        Output('table', 'children'),
        Input('pagination', 'active_page'),
    )
    def table_pagination(number_page: int) -> object:
        active_page = 1 if not number_page else int(number_page)

        start = (active_page - 1) * page_size
        end = start + page_size

        part_table = data[start:end]
        table = get_data_pagination(part_table)

        return table

    @dash_app.callback(
        Output('url', 'pathname'),
        [Input('page-input-button', 'n_clicks')],
        State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
        prevent_initial_call=True
    )
    def handle_next(button, choose_user_cities):
        global previous_page

        if button:
            print(button, choose_user_cities)
            choose_brand_and_cities(previous_page, choose_user_cities)

            dodo_values = [city['dodo_value'] for city in data]
            tashir_values = [city['tashir_value'] for city in data]
            tomato_values = [city['tomato_value'] for city in data]
            all_switches = dodo_values + tashir_values + tomato_values
            print(all_switches)

            if True not in all_switches:
                return no_update
        return '/dash/page_output'

    @dash_app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def return_dash_layout(pathname):
        print('return_dash_layout()')
        if pathname == '/dash/page_input':
            return page_input
        elif pathname == '/dash/page_output':
            return dash_page_output
        else:
            return '404'

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    page_input = html.Div(
        children=[
            dbc.Table(id="table"),
            dbc.Pagination(
                id="pagination",
                max_value=get_total_page(page_size, len(data)),
                fully_expanded=False,
            ),
            html.Button('Отправить на парсинг', id='page-input-button'),
            html.Div(id='container-output-text', children='Enter a value and press submit'),
        ],
        className="table-pagination",
    )
