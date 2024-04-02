import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback_context, ALL, callback, State
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page
from search_brand_and_cities import split_array, sort_brand_and_city, search_brand_city

app = dash.Dash(__name__,
                title="Checklist Test",
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SLATE]
                )

PAGE_SIZE = 15


@callback(
    Output('container-output-text', 'children'),
    Input('submit-button', 'n_clicks'),
    # [Input({'type': 'dynamic-disabled', 'index': ALL}, 'value')],
    State({'type': 'dynamic-switch', 'index': ALL}, 'value')
)
def choose_brand_and_cities(save_changes: int, choose_user_cities: list):
    if not choose_user_cities:
        return "Нажмите на любой переключатель"
    else:
        # {'Додо': ['Воронеж', 'Рязань'], 'Ташир': ['Рязань']} пример того как сделать нужно
        current_page = 1
        # ctx = callback_context
        # switch_id = ctx.triggered_id
        # switch_value = ctx.triggered[0]['value']
        # search_brand_and_cities(data, click_switch, current_page)
        print(choose_user_cities)
        split_choose_user = split_array(choose_user_cities)
        search_brand_cities = search_brand_city(split_choose_user)
        found_brand_and_city = sort_brand_and_city(search_brand_cities)
        print(found_brand_and_city)

        return f'Нажат переключатель {choose_user_cities}'

    # ctx = callback_context
    # if not ctx.triggered:
    #     return 'Переключите один из переключателей'
    # else:
    #     switch_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #     switch_value = ctx.triggered[0]['value']
    #     print(switch_id, switch_value)
    #     return f'Переключатель {switch_id} теперь {"включен" if switch_value else "выключен"}'


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

