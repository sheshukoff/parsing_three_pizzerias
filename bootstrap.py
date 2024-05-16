import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_table
from dash_bootstrap_components import Table

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'Город', 'id': 'city'},
            {'name': 'Бренд 1', 'id': 'brand1', 'presentation': 'dropdown'},
            {'name': 'Бренд 2', 'id': 'brand2', 'presentation': 'dropdown'},
            {'name': 'Бренд 3', 'id': 'brand3', 'presentation': 'dropdown'}
        ],
        data=[
            {'city': 'Город 1', 'brand1': False, 'brand2': True, 'brand3': False},
            {'city': 'Город 2', 'brand1': True, 'brand2': False, 'brand3': True},
            # Добавьте остальные данные здесь
        ],
        page_size=10
    ),
    html.Div(id='output-data')
])

@app.callback(
    Output('output-data', 'children'),
    [Input('table', 'data')],
    [State('table', 'page_current')]
)
def update_output(data, page_current):
    return f"Текущая страница: {page_current}, Данные: {data}"


if __name__ == '__main__':
    app.run_server(debug=True)

