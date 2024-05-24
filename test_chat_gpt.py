import dash_bootstrap_components as dbc
from dash import html, Input, Output, ALL, callback, State
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page
from search_brand_and_cities import split_array

app = dash.Dash(__name__,
                title="Checklist Test",
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SLATE],
                url_base_pathname='/dashboard/'
                )

PAGE_SIZE = 15
previous_page = 1
cities_for_parsing = {'dodo': [], 'tashir': [], 'tomato': []}  # в таком формате должно быть


@callback(
    Output('container-output-text', 'children'),
    Input('pagination', 'active_page'),
    Input('submit-button', 'n_clicks'),
    State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
)
def choose_brand_and_cities(number_page: int, button: None | int, choose_user_cities: list):
    global previous_page

    if number_page is None:
        number_page = 1

    start = (previous_page - 1) * PAGE_SIZE
    split_choose_user = split_array(choose_user_cities)  # разбито на три

    for number, values in enumerate(split_choose_user):
        dodo_value, tashir_value, tomato_value = values

        data[start+number]['dodo_value'] = dodo_value
        data[start+number]['tashir_value'] = tashir_value
        data[start+number]['tomato_value'] = tomato_value

    previous_page = number_page

    return f''


@callback(
    Output('table', 'children'),
    Input('pagination', 'active_page'),
)
def table_pagination(number_page: int) -> object:
    active_page = 1 if not number_page else int(number_page)

    start = (active_page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    part_table = data[start:end]
    table = get_data_pagination(part_table)

    return table


app.layout = html.Div(
    children=[
        dbc.Table(id="table"),
        dbc.Pagination(
            id="pagination",
            max_value=get_total_page(PAGE_SIZE, len(data)),
            fully_expanded=False,
        ),
        html.Button('Отправить на парсинг', id='submit-button', n_clicks=0),
        html.Div(id='container-output-text',
                 children='Enter a value and press submit'),
    ],
    className="table-pagination",
)

if __name__ == "__main__":
    app.run_server(debug=True)

# https://dash.plotly.com/advanced-callbacks
# https://dash.plotly.com/determining-which-callback-input-changed
# https://dash.plotly.com/pattern-matching-callbacks

# нужно сделать проверку, если ни один город не выбран, информацию можно получить из data
# нужно ли сделать много пользовательский режим, для этого нужно избавится от глобальных переменных
# динамически продгужать данные из базы данных, когда работает парсинг (ИДЕЯ)

# Сделать переход из flask в dash table и в результат на выходе для пользователя.