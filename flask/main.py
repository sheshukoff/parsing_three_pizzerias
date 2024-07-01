from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, LoginManager, login_user, logout_user
from flask_bcrypt import Bcrypt

from create_table import session, Authorized_users
from write_query_sql import search_password, recieve_user_login, load_table_authorized_users

import dash_bootstrap_components as dbc
from dash import html, Input, Output, ALL, callback, State, dcc, no_update, dash_table
import dash
from work_with_dash import data
from components_for_dash_table import get_data_pagination, get_total_page, split_array
from output_info_for_user import dash_page_output
from create_table_sql import Brand, City, Section, Product, session


flask_app = Flask(__name__)
flask_app.secret_key = "some secret petelka_458"
bcrypt = Bcrypt(flask_app)

login_manager = LoginManager()
login_manager.init_app(flask_app)


# СТРАНИЦЫ FLASK
@login_manager.user_loader
def loader_user(user_id):
    print("================ loader_user ==================")
    return session.get(Authorized_users, user_id)


def index_page():
    if request.method == "GET":
        print("GET")
    elif request.method == "POST":
        print("POST")
    else:
        print("another_method")
    return render_template("index.html")


def sign_in():
    if request.method == "GET":
        print("GET")
    elif request.method == "POST":
        print("POST")

        input_login = request.form.get("login")
        input_password = request.form.get("password")

        user = (
            session.query(Authorized_users)
            .filter(Authorized_users.login == input_login)
            .first()
        )

        if not input_login or not input_password:
            flash("Пожалуйста, заполните все поля")
        else:
            login_user_db = recieve_user_login(input_login)  # логин пользователя из БД
            hash_password_user_db = search_password(input_login)  # хешированный пароль пользоватея из БД
            if login_user_db is None or hash_password_user_db is None:
                flash("Логин или пароль не правильный")
                return redirect(url_for("sign_in"))

            is_valid = bcrypt.check_password_hash(hash_password_user_db, input_password)

            if input_login == login_user_db and is_valid is True:
                login_user(user, remember=False)
                # return redirect(url_for("dashboard", login=input_login))
                return redirect('/dash/page_input')
            else:
                flash("Логин или пароль не правильный")
    else:
        print("another_method")
    return render_template("sign_in.html")


def sign_up():
    if request.method == "GET":
        print("GET")
    elif request.method == "POST":
        print("POST")
        login = request.form.get("login")
        password = request.form.get("password_first")
        password_repeat = request.form.get("password_second")

        if not (login or password or password_repeat):
            flash("Пожалуйста, заполните все поля")
        elif password != password_repeat:
            flash("Пароли должны быть совпадать")
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8", "ignore")
            print(login, hashed_password)

            # здесь происходит загрузка в базу данных login и password (пароль уже хеширован)
            load_table_authorized_users(login, hashed_password)
            return redirect(url_for("sign_in"))
    else:
        print("another_method")
    return render_template("sign_up.html")


@login_required
def log_out():
    logout_user()
    return redirect(url_for("index_page"))


# ТАБЛИЦЫ DASH TABLE
dash_app = dash.Dash(__name__,
                     server=flask_app,
                     title="Checklist Test",
                     suppress_callback_exceptions=True,
                     external_stylesheets=[dbc.themes.SLATE],
                     routes_pathname_prefix='/dash/'
                     )

PAGE_SIZE = 15
previous_page = 1


@callback(
    Output('container-output-text', 'children'),
    Input('pagination', 'active_page'),
    State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
)
def choose_brand_and_cities(number_page: int, choose_user_cities: list):
    global previous_page

    if number_page is None:
        number_page = 1

    start = (previous_page - 1) * PAGE_SIZE
    split_choose_user = split_array(choose_user_cities)  # разбито на три

    for number, values in enumerate(split_choose_user):
        dodo_value, tashir_value, tomato_value = values

        data[start + number]['dodo_value'] = dodo_value
        data[start + number]['tashir_value'] = tashir_value
        data[start + number]['tomato_value'] = tomato_value

    previous_page = number_page

    return ''


@callback(
    Output('table', 'children'),
    Input('pagination', 'active_page'),
)
def table_pagination(number_page: int) -> object:
    active_page = 1 if not number_page else int(number_page)

    start = (active_page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    part_table = data[start:end]
    table = get_data_pagination(part_table)

    return table


@callback(
    Output('url', 'pathname'),
    [Input('page-input-button', 'n_clicks')],
    State({'type': 'dynamic-switch', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def handle_next(button, choose_user_cities):
    global previous_page

    if button:
        print(button, choose_user_cities)
        choose_brand_and_cities(previous_page, choose_user_cities)

        dodo_values = [city['dodo_value'] for city in data]
        tashir_values = [city['tashir_value'] for city in data]
        tomato_values = [city['tomato_value'] for city in data]
        all_switches = dodo_values + tashir_values + tomato_values
        print(all_switches)

        if True in all_switches:
            return '/dash/dash_page_output'
    return no_update


@dash_app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def return_dash_layout(pathname):
    print('return_dash_layout()')
    if pathname == '/dash/page_input':
        return page_input
    elif pathname == '/dash/dash_page_output':
        return dash_page_output
    else:
        return '404'


dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

page_input = html.Div(
    children=[
        dbc.Table(id="table"),
        dbc.Pagination(
            id="pagination",
            max_value=get_total_page(PAGE_SIZE, len(data)),
            fully_expanded=False,
        ),
        html.Button('Отправить на парсинг', id='page-input-button'),
        html.Div(id='container-output-text', children='Enter a value and press submit'),
    ],
    className="table-pagination",
)


get_table = (session.query(
    Brand.name, City.name, Section.name, Product.name, Product.description, Product.new_price, Product.old_price
).join(Brand).join(City).join(Section)).all()

output_info = []

for row in get_table:
    brand, city, section, product_name, description, new_price, old_price = row

    output_info.append({
        'brand': brand,
        'city': city,
        'section': section,
        'product_name': product_name,
        'description': description,
        'new_price': new_price,
        'old_price': old_price
    }, )

columns = [
    {'name': 'Бренд', 'id': 'brand'},
    {'name': 'Город', 'id': 'city'},
    {'name': 'Секция', 'id': 'section'},
    {'name': 'Название продукта', 'id': 'product_name'},
    {'name': 'Описание', 'id': 'description'},
    {'name': 'Новая цена', 'id': 'new_price'},
    {'name': 'Старая цена', 'id': 'old_price'},
]

dash_page_output = html.Div(
    children=[
        dash_table.DataTable(
            data=output_info,
            columns=columns,
            page_action="native",
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            page_current=0,
            page_size=15,
            tooltip_duration=500,
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in output_info
            ],
            style_data={
                # 'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_header={'backgroundColor': '#161a1d',
                          'fontWeight': 'bold',
                          'color': '#FFFFFF',
                          'border': '1px solid black',
                          'font-family': 'Noto Kufi Arabic'
                          },
            style_table={'height': '670px',
                         'overflow': 'auto',
                         'width': '100%',
                         'margin': 'auto'},
            style_cell={'padding': '5px',
                        'fontSize': 16,
                        'font-family': 'Noto Kufi Arabic',
                        'textAlign': 'left',
                        'border': '2px solid grey',
                        'backgroundColor': '#161a1d',
                        'color': '#a0a1ab',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': 0},
            style_cell_conditional=[
                {'if': {'column_id': 'Бренд'},
                    'width': '5%'},
                {'if': {'column_id': 'Город'},
                 'width': '5%'},
                {'if': {'column_id': 'Секция'},
                 'width': '5%'},
                {'if': {'column_id': 'Название продукта'},
                 'width': '10%'},
                {'if': {'column_id': 'Описание'},
                 'width': '65%'},
                {'if': {'column_id': 'Новая цена'},
                 'width': '5%'},
                {'if': {'column_id': 'Старая цена'},
                 'width': '5%'},
            ],
        )
    ]
)



flask_app.add_url_rule("/", "index_page", index_page, methods=["GET", "POST"])
flask_app.add_url_rule("/sign_in", "sign_in", sign_in, methods=["GET", "POST"])
flask_app.add_url_rule("/sign_up", "sign_up", sign_up, methods=["GET", "POST"])

flask_app.add_url_rule("/" "log_out", log_out, methods=["GET", "POST"])

if __name__ == "__main__":
    flask_app.run(debug=True)
    # run_simple("localhost", 5000, application=dispatcher_application)

# проверить как сейчас работает парсинг
# перенести функции относящиеся к классу юзер и переписать код
# сделать страницы только авторизованным пользователем
# @login_required -> декоратор позволяет находится только авторизованным пользователям
# можно ли убрать функцию dashboard
