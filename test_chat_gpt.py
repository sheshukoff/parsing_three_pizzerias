import dash_bootstrap_components as dbc
from dash import html, Input, Output, ALL, callback, State
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page
from search_brand_and_cities import split_array, search_brand_city, sort_brand_and_city

app = dash.Dash(__name__,
                title="Checklist Test",
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SLATE]
                )

PAGE_SIZE = 15
found_brand_and_city = {'Додо': [], 'Ташир': [], 'Томато': []}  # в таком формате должно быть


@callback(
    Output('container-output-text', 'children'),
    # Input('submit-button', 'n_clicks'),
    Input('pagination', 'active_page'),
    State({'type': 'dynamic-switch', 'index': ALL}, 'value')
)
def choose_brand_and_cities(number_page: int, choose_user_cities: list):
    if number_page is None:
        active_page = 1
    else:
        active_page = int(number_page)

    if not number_page:
        print(active_page, number_page)
        print(choose_user_cities)
        return "Нажмите на любой переключатель"
    elif number_page:
        print(active_page, number_page)
        start = (active_page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        part_table = data[start:end]
        split_choose_user = split_array(choose_user_cities)
        search_brand_cities = search_brand_city(split_choose_user, part_table)

        for city, brands in search_brand_cities.items():
            for city_data in data:
                if city == city_data['city']:
                    if brands['dodo'] is True:
                        city_data.update({"dodo_value": True})
                    elif brands['dodo'] is False:
                        city_data.update({"dodo_value": False})
                    if brands['tashir'] is True:
                        city_data.update({"tashir_value": True})
                    elif brands['tashir'] is False:
                        city_data.update({"tashir_value": False})
                    if brands['tomato'] is True:
                        city_data.update({"tomato_value": True})
                    elif brands['tomato'] is False:
                        city_data.update({"tomato_value": False})


        found_brand_and_city = sort_brand_and_city(search_brand_cities)
        return f'Нажат переключатель {found_brand_and_city}'


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
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.Div(id='container-output-text',
                 children='Enter a value and press submit')
    ],
    className="table-pagination",
)

if __name__ == "__main__":
    app.run_server(debug=True)

# https://dash.plotly.com/advanced-callbacks
# https://dash.plotly.com/determining-which-callback-input-changed
# https://dash.plotly.com/pattern-matching-callbacks
