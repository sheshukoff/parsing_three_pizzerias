import dash_bootstrap_components as dbc
from dash import html, Input, Output, ALL, State, dcc, no_update, set_props
import dash
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache
from sort_cities import create_dash_table
from components_for_dash_table import get_data_pagination, get_total_page, split_array

PAGE_SIZE = 15


def init_dash_table(flask_app):
    """
    Функция инициализирует dash app
    :param flask_app: bool
    :return: object
    """
    cache = diskcache.Cache("./cache")
    long_callback_manager = DiskcacheLongCallbackManager(cache)
    dash_app = dash.Dash(__name__,
                         server=flask_app,
                         title="Checklist Test",
                         suppress_callback_exceptions=True,
                         external_stylesheets=[dbc.themes.SLATE],
                         routes_pathname_prefix='/dash/',
                         long_callback_manager=long_callback_manager
                         )
    return dash_app


def init_dash_table_input(dash_app, page_size):
    data = create_dash_table()

    @dash_app.callback(
        Output('previous_page_session', 'data'),  # записал данные
        Input('table', 'children'),  # выбрал стрницу
        State('pagination', 'active_page')
    )
    def previous_page_session(number_page: int, active_page: int) -> int:
        """
        Функция возвращает предыдущую страницу (в сессии браузера)
        :param number_page: int
        :param active_page: int
        :return: int
        """
        if active_page is None:
            active_page = 1

        previous_page = active_page
        print(f'previous_page->{previous_page}')

        return previous_page

    @dash_app.callback(
        Output('dash_table_session', 'data'),  # записал данные
        Input('pagination', 'active_page'),  # выбрал стрницу
        [State('dash_table_session', 'data'),
         State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
         State('previous_page_session', 'data')]  # считал данные
    )
    def choose_brand_and_cities(
        active_page: int,
        create_table: list,
        choose_user_cities: list,
        previous_page: int
    ) -> list:
        """
        Функция возвращает выбранные бренды и города пользователем (в сессии браузера)
        :param active_page: int
        :param create_table: list
        :param choose_user_cities: list
        :param previous_page: int
        :return: list
        """
        if create_table is None:
            create_table = data

        if previous_page is None:
            previous_page = 1

        print('66 choose_brand_and_cities', f'active_page->{active_page}  previous_page->{previous_page}')
        start = (previous_page - 1) * page_size
        split_choose_user = split_array(choose_user_cities)  # разбито на три

        for number, values in enumerate(split_choose_user):
            dodo_value, tashir_value, tomato_value = values

            create_table[start + number]['dodo_value'] = dodo_value
            create_table[start + number]['tashir_value'] = tashir_value
            create_table[start + number]['tomato_value'] = tomato_value

        return create_table

    @dash_app.callback(
        Output('table', 'children'),
        Input('dash_table_session', 'data'),
        State('pagination', 'active_page')
    )
    def table_pagination(create_table: list, number_page: int) -> object:
        """
        Функция строит таблицу (в сессии браузера)
        :param create_table: list
        :param number_page: int
        :return: object
        """
        active_page = 1 if not number_page else int(number_page)
        print('86 table_pagination', active_page)

        if create_table is None:
            create_table = data

        start = (active_page - 1) * page_size
        end = start + page_size

        part_table = create_table[start:end]
        table = get_data_pagination(part_table)
        return table

    def any_toggle_switches(create_table: list) -> bool:
        """
        Функция проверяет включен ли хоть один переключатель
        :param create_table: list
        :return: bool
        """
        dodo_values = [city['dodo_value'] for city in create_table]
        tashir_values = [city['tashir_value'] for city in create_table]
        tomato_values = [city['tomato_value'] for city in create_table]
        all_switches = dodo_values + tashir_values + tomato_values

        return True in all_switches

    def get_cities_for_parsing(create_table: list) -> dict:
        """
        Функция возвращает города для парсинга
        :param create_table: list
        :return: dict
        """
        dodo_city = [city['city'] for city in create_table if city['dodo_value'] is True]
        tashir_city = [city['city'] for city in create_table if city['tashir_value'] is True]
        tomato_city = [city['city'] for city in create_table if city['tomato_value'] is True]

        return {'Додо': dodo_city, 'Ташир': tashir_city, 'Томато': tomato_city}

    @dash_app.callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input('page-input-button', 'n_clicks'),
        [State('url', 'pathname'),
         State('dash_table_session', 'data'),
         State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
         State('previous_page_session', 'data'),
         State('pagination', 'active_page')],
        prevent_initial_call=True
    )
    def url_router(
            button: int,
            url_address: str,
            create_table: list,
            choose_user_cities: list,
            previous_page: int,
            active_page: int
    ) -> str:
        """
        Функция возвращает url address
        :param button: int
        :param url_address: str
        :param create_table: list
        :param choose_user_cities: list
        :param previous_page: int
        :param active_page: int
        :return: str
        """
        print('url_router', button, url_address)
        if button:
            if url_address == '/dash/page_input':
                choose_brand_and_cities(active_page, create_table, choose_user_cities, previous_page)
                if any_toggle_switches(create_table):
                    set_props('choose_cities_session', {'data': get_cities_for_parsing(create_table)})
                    return '/dash/page_waiting_parsing'
                else:
                    return no_update

        return no_update

    @dash_app.callback(
        Output('url', 'pathname'),
        Input('subtotal-input', 'n_clicks'),
        State('url', 'pathname')
    )
    def url_router_2(button: int, url_address: str) -> str:
        """
        Функция возвращает url address
        :param button: int
        :param url_address: str
        :return: str
        """
        print('url_router_2', button, url_address)
        if button:
            if url_address == '/dash/page_waiting_parsing':
                return '/dash/page_output'

        return no_update

    # @dash_app.callback(
    #     Output('page-content', 'children'),
    #     Input('url', 'pathname'),
    # )
    # def return_dash_layout(pathname: str) -> object | str:
    #     """
    #     Функция возвращает страницу пользователю
    #     :param pathname: str
    #     :return: object | str
    #     """
    #     print('return_dash_layout()')
    #     if pathname == '/dash/page_input':
    #         return page_input
    #     elif pathname == '/dash/page_waiting_parsing':
    #         return dash_table_waiting_parsing
    #     elif pathname == '/dash/page_output':
    #         return dash_page_output
    #     else:
    #         return '404'

    # dash_app.layout = html.Div([
    #     dcc.Location(id='url', refresh=False),
    #     html.Div(id='page-content'),
    # ])

    page_input = html.Div(
        children=[
            dcc.Store(id='previous_page_session', storage_type='session'),
            dcc.Store(id='dash_table_session', storage_type='session'),
            dcc.Store(id='choose_cities_session', storage_type='session'),
            dcc.Store(id='active_page_session', storage_type='session'),
            dcc.Store(id='url_router_execution_session', storage_type='session'),
            dbc.Table(id='table'),
            dbc.Pagination(
                id="pagination",
                max_value=get_total_page(page_size, len(data)),
                fully_expanded=False,
            ),
            html.Button('Отправить на парсинг', id='page-input-button'),
        ],
        className="table-pagination",
    )

    return page_input
