from flask import Flask, render_template_string, request, redirect, session
from dash import Dash, html, dcc, no_update
from dash.dependencies import Input, Output


flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash/')


flask_app.secret_key = 'ololo'


def index():
    print('index()')

    if 'counter' not in session or session['counter'] <= 0:
        session['counter'] = 2

    if request.method == 'POST':
        session['counter'] -= 1
        if session['counter'] <= 0:
            return redirect('/dash/page2')

    return render_template_string('''
        <h1>Страница 1</h1>
        <h2>Для перехода нажми ещё: {{session["counter"]}} раз...</h2>
        <form method="post">
            <input type="submit" value="Далее">
        </form>
    ''')


def page4():
    print('page4()')
    return render_template_string('<h1>Страница 4</h1><a href="/">Вернуться на главную</a>')


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


flask_app.add_url_rule('/', 'index', index, methods=["GET", "POST"])
flask_app.add_url_rule('/page4', 'page4', page4)


dash_app.layout = html.Div([
    # dcc.Store(id='button-store', storage_type='session'),  # Хранение в сессии браузера на стороне клиента
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


if __name__ == '__main__':
    flask_app.run(debug=True)
