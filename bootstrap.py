import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Checklist(
        id='toggle-switch',
        options=[
            {'label': 'Toggle', 'value': 'toggle'}
        ],
        value=[]
    ),
    html.Div(id='toggle-switch-output')
])


@app.callback(
    Output('toggle-switch-output', 'children'),
    [Input('toggle-switch', 'value')]
)
def update_output(value):
    if 'toggle' in value:
        return "Switch is turned on"
    else:
        return "Switch is turned off"


if __name__ == '__main__':
    app.run_server(port=8050)
