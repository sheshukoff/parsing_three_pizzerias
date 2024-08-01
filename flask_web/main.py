from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, LoginManager, login_user, logout_user
from flask_bcrypt import Bcrypt

from create_table import session, Authorized_users
from write_query_sql import search_password, recieve_user_login, load_table_authorized_users

from dash_table_input import init_dash_table, init_dash_table_input, PAGE_SIZE
from dash_table_output import init_dash_table_output
from dash_table_waiting_parsing import init_dash_table_waiting_parsing


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


if __name__ == "__main__":
    flask_app = Flask(__name__)
    flask_app.secret_key = "some secret petelka_458"
    bcrypt = Bcrypt(flask_app)

    login_manager = LoginManager()
    login_manager.init_app(flask_app)


    @login_manager.user_loader
    def loader_user(user_id):
        print("================ loader_user ==================")
        return session.get(Authorized_users, user_id)

    flask_app.add_url_rule("/", "index_page", index_page, methods=["GET", "POST"])
    flask_app.add_url_rule("/sign_in", "sign_in", sign_in, methods=["GET", "POST"])
    flask_app.add_url_rule("/sign_up", "sign_up", sign_up, methods=["GET", "POST"])

    flask_app.add_url_rule("/" "log_out", log_out, methods=["GET", "POST"])

    dash_app = init_dash_table(flask_app)
    dash_page_output = init_dash_table_output()
    dash_table_waiting_parsing = init_dash_table_waiting_parsing(dash_app)
    init_dash_table_input(dash_app, PAGE_SIZE, dash_table_waiting_parsing, dash_page_output)

    flask_app.run()
