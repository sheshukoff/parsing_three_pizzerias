from dash import Dash, html, callback, dcc, Input, Output


def make_dash(server):
    return Dash(
        server=server,
        url_base_pathname='/dash/'
    )


def make_layout():
    return html.Div(
        [
            html.P("Hey this is a Dash app :)"),
            dcc.Input(id="input"),
            html.Div(id="output"),
        ]
    )


def define_callbacks():
    @callback(
        Output("output", "children"),
        Input("input", "value"),
    )
    def show_output(text):
        return f"you entered: '{text}'"