import dash_bootstrap_components as dbc
from dash import html, Input, Output, ALL, callback, State
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page
from search_brand_and_cities import split_array, search_brand_city, sort_brand_and_city, changes_in_data

app = dash.Dash(__name__,
                title="Checklist Test",
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SLATE]
                )

PAGE_SIZE = 15
previous_page = 1
cities_for_parsing = {'dodo': [], 'tashir': [], 'tomato': []}  # в таком формате должно быть


@callback(
    Output('container-output-text', 'children'),
    Input('pagination', 'active_page'),
    State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
)
def choose_brand_and_cities(number_page: int, choose_user_cities: list):
    global previous_page

    if number_page is None:
        active_page = 1
    else:
        active_page = int(number_page)

    if not number_page:
        return "Нажмите на любой переключатель"
    elif number_page:
        start = (active_page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        part_table = data[start:end]

        start = (previous_page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        previous_part_table = data[start:end]

        split_choose_user = split_array(choose_user_cities)  # разбито на три

        for number, values in enumerate(split_choose_user):
            dodo_value, tashir_value, tomato_value = values
            data[start+number]['dodo_value'] = dodo_value
            data[start+number]['tashir_value'] = tashir_value
            data[start+number]['tomato_value'] = tomato_value

        previous_page = number_page
        return f'Нажат переключатель'


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


# я беру split_choose_user и вношу изменения в data, город я беру из previous_part_table и меняю _value
# TODO сделать для превой страницы и последней страницы что бы были изменения переключателей
# for num, cities in enumerate(split_choose_user):
#     print(previous_part_table[num]['city'], num, cities)
# for number in range(0, 3):
#     if number == 0:
#         for city_brands in data:
#             if city_brands['city'] == previous_part_table[num]['city']:
#                 city_brands['dodo_value'] = True
#     elif number == 1:
#         for city_brands in data:
#             if city_brands['city'] == previous_part_table[num]['city']:
#                 city_brands['tashir_value'] = True
#     elif number == 2:
#         for city_brands in data:
#             if city_brands['city'] == previous_part_table[num]['city']:
#                 city_brands['tomato_value'] = True

# for element in data[0:30]:
#     print(element)

# for city, brands in choose_brand_cities.items():
#     for city_data in data:
#         if city == city_data['city']:
#             if brands['dodo'] is True:
#                 city_data.update({"dodo_value": True})
#             elif brands['dodo'] is False:
#                 city_data.update({"dodo_value": False})
#             if brands['tashir'] is True:
#                 city_data.update({"tashir_value": True})
#             elif brands['tashir'] is False:
#                 city_data.update({"tashir_value": False})
#             if brands['tomato'] is True:
#                 city_data.update({"tomato_value": True})
#             elif brands['tomato'] is False:
#                 city_data.update({"tomato_value": False})

# found_brand_and_city = sort_brand_and_city(choose_brand_cities)