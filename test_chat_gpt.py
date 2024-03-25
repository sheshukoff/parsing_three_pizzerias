import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback_context, ALL, callback
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page

app = dash.Dash(__name__,
                title="Checklist Test",
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SLATE]
                )

PAGE_SIZE = 15


@callback(
    Output('output-switch-active', 'children'),
    [Input({'type': 'dynamic-switch', 'index': ALL}, 'value')]
)
def display(*args):
    ctx = callback_context
    if not ctx.triggered:
        return 'Переключите один из переключателей'
    else:
        switch_id = ctx.triggered[0]['prop_id'].split('.')[0]
        switch_value = ctx.triggered[0]['value']
        print(switch_id, switch_value)
        return f'Переключатель {switch_id} теперь {"включен" if switch_value else "выключен"}'


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
    ],
    className="table-pagination",
)

if __name__ == "__main__":
    app.run_server(debug=True)
