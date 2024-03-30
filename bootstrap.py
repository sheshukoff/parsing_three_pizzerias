# Import packages
from dash import Dash, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

# Initialise the App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                dbc.Switch(
                    value=False,
                    id='restricted_search',
                    inputClassName=None
                ),
            ], width=6)])
    ]
)


@callback(
    Output('restricted_search', 'inputClassName'),
    Input('restricted_search', 'value')
)
def update_switch(activated):
    if activated:
        return 'bg-success',
    return None


# Run the App
if __name__ == '__main__':
    app.run_server()
