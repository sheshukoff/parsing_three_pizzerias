from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
from components_for_dash_table import waiting_parsing


def init_dash_table_waiting_parsing(dash_app):
    @dash_app.callback(
        Output('table_for_waiting_parsing', 'children'),
        Input('page-content', 'children'),
    )
    def get_table_waiting_parsing(table):
        print('get_table_waiting_parsing')
        waiting_table = waiting_parsing(12)
        return waiting_table

    @dash_app.callback(
        Output('url', 'pathname'),
        [Input('subtotal-input', 'n_clicks')],
    )
    def return_output_table(button):
        if button:
            return '/dash/page_output'

    table_waiting_parsing = html.Div(
        children=[
            dbc.Table(id='table_for_waiting_parsing'),
            html.Button('Промежуточный итог', id='subtotal-input'),
        ],
        className="table-pagination",
    )

    return table_waiting_parsing
