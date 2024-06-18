from werkzeug import run_simple
from flask import redirect, url_for, request
from flask import Flask, render_template_string
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Создаем сервер Flask
flask_app = Flask(__name__)


# Определяем маршруты Flask

def index():
    if request.method == "GET":
        print("GET")
    elif request.method == "POST":
        print("POST")
        # return redirect(url_for())
    return render_template_string('''
    <h1>Страница 1</h1>
        <form action = "/dash/page2" method = "post">
            <p>Есть логин и пароль</p>
                <input type="submit" class="button sign_in" value="Войти">
        </form>
    ''')


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
    dcc.Link(html.Button(
            'Отправить на парсинг', id='submit-button', className='btn btn-primary', n_clicks=0),
            href='/dash/page3')
    # html.A('Далее', href='/dash/page3')
])

page_3_layout = html.Div([
    html.H1('Страница 3'),
    html.Table([
        html.Tr([html.Td('Клетка A'), html.Td('Клетка B')]),
        html.Tr([html.Td('Клетка C'), html.Td('Клетка D')])
    ]),
    html.A(html.Button(
        'Отправить на парсинг', id='submit-button', className='btn btn-primary', n_clicks=0),
        href='/page4'),
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


dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

flask_app.add_url_rule("/", "index", index, methods=["GET", "POST"])
flask_app.add_url_rule("/page4", "page4", page4, methods=["GET", "POST"])

# # Объединяем приложения Flask и Dash
# application = DispatcherMiddleware(
#     flask_app,
#     {
#         '/dash': dash_app.server,
#     }
# )

if __name__ == '__main__':
    flask_app.run(debug=True)
    # run_simple("localhost", 5000, application=application)
