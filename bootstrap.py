from flask import Flask, render_template, redirect, url_for
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash


# Определяем функцию для первой страницы
def page1():
    return '<h1>Страница 1</h1><a href="/page2"><button>Далее</button></a>'


# Определяем функцию для третьей страницы
def page3():
    return '<h1>Страница 3</h1>'


# Создаем Flask-приложение
flask_app = Flask(__name__)

# Добавляем правила URL для Flask-приложения
flask_app.add_url_rule('/', 'page1', page1)
flask_app.add_url_rule('/page3', 'page3', page3)


# Создаем Dash-приложение
dash_app = Dash(
    __name__,
    server=flask_app,
    routes_pathname_prefix='/page2/'
)


# Определяем макет Dash-приложения
dash_app.layout = html.Div([
    html.H1('Страница 2'),
    dcc.Store(id='button-clicks', data=0),  # Хранилище для счетчика нажатий
    dbc.Table([
        html.Thead(html.Tr([html.Th("Колонка 1"), html.Th("Колонка 2")])),
        html.Tbody([
            html.Tr([html.Td("Ячейка 1"), html.Td("Ячейка 2")]),
            html.Tr([html.Td("Ячейка 3"), html.Td("Ячейка 4")])
        ])
    ]),
    # Используем callback для обработки нажатия кнопки
    html.Button('Далее', id='next-button', className='btn btn-primary'),
    dcc.Location(id='redirect', refresh=True)
])


# Callback для обработки нажатия кнопки
@dash_app.callback(
    Output('redirect', 'pathname'),
    [Input('next-button', 'n_clicks')],
    [Input('button-clicks', 'data')]
)
def handle_next(n_clicks, button_clicks):
    if n_clicks > button_clicks:
        print("Далее")  # Выводим сообщение в консоль
        return '/page3'  # Перенаправляем на страницу 3
    return dash.no_update


# Запускаем приложение
if __name__ == '__main__':
    flask_app.run()

# https://dev.to/naderelshehabi/securing-plotly-dash-using-flask-login-4ia2
