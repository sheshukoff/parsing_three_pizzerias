from flask import Flask, render_template_string, url_for
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import flask
# from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.exceptions import NotFound

# Создаем сервер Flask
flask_app = Flask(__name__)


# Определяем маршруты Flask
def index():
    return render_template_string(
        '''<h1>Страница 1</h1>
                <form action = "http://localhost:5000/dash/page2" method = "post">
                    <p>Пойти на страницу 2</p>
                        <input type="submit" class="button sign_in" value="Войти">
                </form>''')


@flask_app.route('/dash/page2', methods=['POST'])
def method_post():
    print('24 row')
    return flask.redirect(url_for('display_page'))


def page4():
    return render_template_string('<h1>Страница 4</h1><a href="/">Далее</a>')


# Создаем приложение Dash
dash_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash/')

# Определяем макеты Dash для разных страниц
page_2_layout = html.Div([
    html.H1('Страница 2'),
    html.Table([
        html.Tr([html.Td('Ячейка 1'), html.Td('Ячейка 2')]),
        html.Tr([html.Td('Ячейка 3'), html.Td('Ячейка 4')])
    ]),
    html.Form([
        html.Button('Отправить на парсинг', id='submit-button', className='btn btn-primary', n_clicks=0),
    ], action='/dash/page3', method='post'),
])

page_3_layout = html.Div([
    html.H1('Страница 3'),
    html.Table([
        html.Tr([html.Td('Клетка A'), html.Td('Клетка B')]),
        html.Tr([html.Td('Клетка C'), html.Td('Клетка D')])
    ]),
    html.A('Далее', href='/page4')
])


# Обработчики для переключения между страницами
@dash_app.callback(Output('page-content', 'children'),
                   [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dash/page2':
        return page_2_layout
    elif pathname == '/dash/page3':
        return page_3_layout
    else:
        return '404'


@dash_app.server.route('/dash/page3', methods=['POST'])
def on_post():
    data = flask.request.form
    print(data, '62 row')
    row = list(data)
    if len(row) == 0:
        return flask.redirect('/dash/page3')
    else:
        return flask.redirect('/dash/page2')


dash_app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ], id='main_div')


flask_app.add_url_rule("/", "index", index, methods=["GET", "POST"])
flask_app.add_url_rule("/dash/page2", "display_page", display_page, methods=["GET"])
flask_app.add_url_rule("/dash/page3", "display_page", display_page, methods=["GET"])
flask_app.add_url_rule("/page4", "page4", page4, methods=["GET", "POST"])
# # Объединяем приложения Flask и Dash
# dispatcher_application = DispatcherMiddleware(
#     flask_app,
#     {
#         "/dash": dash_app.server,
#         "/dash": dash_app.server
#     },
# )

flask_app.wsgi_app = DispatcherMiddleware(
    flask_app.wsgi_app,
    {
        "/dash": dash_app.server,
    })


# application = DispatcherMiddleware(
#     server,
#     {"/app1": app1.server, "/app2": app2.server},
# )

if __name__ == '__main__':
    flask_app.run(debug=True)

# https://dev.to/naderelshehabi/securing-plotly-dash-using-flask-login-4ia2
