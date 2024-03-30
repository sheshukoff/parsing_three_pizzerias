import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df[' index'] = range(1, len(df) + 1)
app = dash.Dash(__name__)
PAGE_SIZE = 15

app.layout = html.Div([
    html.Div('Data table pagination test'),
    dcc.Dropdown(
        id='select_page_size',
        options=[{'label': '5', 'value': 5}, {'label': '10', 'value': 10}, {'label': '15', 'value': 15}],
        value=5
    ),
    html.Div(dash_table.DataTable(
        id='datatable-paging',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        page_size=PAGE_SIZE,
        page_current=0,
    ))
])


@app.callback(
    Output('datatable-paging', 'page_size'),
    [Input('select_page_size', 'value')])
def update_graph(page_size):
    return page_size


if __name__ == '__main__':
    app.run_server(debug=True)
