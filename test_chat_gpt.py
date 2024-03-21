import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page

app = dash.Dash(__name__, title="Checklist Test", external_stylesheets=[dbc.themes.SLATE])

PAGE_SIZE = 15


@app.callback(Output('score-list', 'data'),
              Input('form-check-input', 'id'))
def update_loosers(id_number):
    print(id_number)
    return None


@callback(
    Output('score-list', 'children'),
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
        dbc.Table(id="score-list"),
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
