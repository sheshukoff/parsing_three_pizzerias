from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, LoginManager, login_user, logout_user
from flask_bcrypt import Bcrypt
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import flask

from create_table import session, Authorized_users
from write_query_sql import search_password, recieve_user_login, load_table_authorized_users
from test_chat_gpt import dash_app
from output_info_for_user import dash_app_output

flask_app = Flask(__name__)
flask_app.secret_key = "some secret petelka_458"
bcrypt = Bcrypt(flask_app)

login_manager = LoginManager()
login_manager.init_app(flask_app)


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
                return redirect(url_for("dashboard", login=input_login))
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


@login_required
def dashboard():
    data = flask.request.form
    row = dict(data)
    column = row['name']
    print(column, '109')
    if column:
        return flask.redirect('/output_info_for_user/')
    # if flask.request.form == "GET":
    #     print("106 GET")
    # elif flask.request.form == "POST":
    #     print('108 POST')
    #     print(column)
    # else:
    #     print("another_method")
    # return redirect(url_for('output_info_for_user'))


@login_required
def output_info_for_user():
    pass


flask_app.add_url_rule("/", "index_page", index_page, methods=["GET", "POST"])
flask_app.add_url_rule("/sign_in", "sign_in", sign_in, methods=["GET", "POST"])
flask_app.add_url_rule("/sign_up", "sign_up", sign_up, methods=["GET", "POST"])
flask_app.add_url_rule("/dashboard/", "dashboard", dashboard, methods=["GET", "POST"])
flask_app.add_url_rule(
    "/output_info_for_user/", "output_info_for_user", output_info_for_user, methods=["GET", "POST"]
)

flask_app.add_url_rule("/" "log_out", log_out, methods=["GET", "POST"])

dispatcher_application = DispatcherMiddleware(
    flask_app,
    {
        "/dashboard": dash_app.server,
        "/output_info_for_user": dash_app_output.server,
    },
)

if __name__ == "__main__":
    # flask_app.run(debug=True)
    run_simple("localhost", 5000, application=dispatcher_application)

# проверить как сейчас работает парсинг
# перенести функции относящиеся к классу юзер и переписать код
# сделать страницы только авторизованным пользователем
# @login_required -> декоратор позволяет находится только авторизованным пользователям
# можно ли убрать функцию dashboard

# def test_choose_city():
#     if request.method == 'GET':
#         print('GET')
#     elif request.method == 'POST':
#         correct_password = '123'
#         input_password = request.form.get('password')
#         print(input_password)
#         if input_password == correct_password:
#             print('пароль правильный')
#         else:
#             print('попробуй заново')
#
#     # content = {
#     #     'input_password': input_password
#     # }
#
#         # cities = recieve_cities()
#         # print(cities)
#     return render_template('test_choose_city.html')


# app.add_url_rule(
#     "/choose_brand/choose_city", "choose_city", choose_city, methods=["GET", "POST"]
# )
# app.add_url_rule("/choose_brand/test_choose_city", 'test_choose_city', test_choose_city, methods=['GET', 'POST'])
