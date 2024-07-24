from dash import Dash, html, dcc, no_update
from dash.dependencies import Input, Output
from test import flask_app

dash_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash/')


@dash_app.callback(
    Output('url', 'pathname'),
    [Input('page-2-button', 'n_clicks')],
    prevent_initial_call=True
)
def go_to_page_3(n_clicks):
    print('go_to_page_3()')
    if n_clicks and n_clicks > 2:
        return '/dash/page3'
    else:
        return no_update


@dash_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def return_dash_layout(pathname):
    print('return_dash_layout()')
    if pathname == '/dash/page2':
        return page_2_layout
    elif pathname == '/dash/page3':
        return page_3_layout
    else:
        return '404'


page_2_layout = html.Div([
    html.H1('Страница 2'),
    html.Table([
        html.Tr([html.Td('Ячейка 1'), html.Td('Ячейка 2')]),
        html.Tr([html.Td('Ячейка 3'), html.Td('Ячейка 4')])
    ]),
    html.Button('Далее', id='page-2-button')
])


page_3_layout = html.Div([
    html.H1('Страница 3'),
    html.Table([
        html.Tr([html.Td('Клетка A'), html.Td('Клетка B')]),
        html.Tr([html.Td('Клетка C'), html.Td('Клетка D')])
    ]),
    html.A(html.Button('Далее'), href='/page4')
])



