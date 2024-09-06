from create_table import Authorized_users, session, engine
from sqlalchemy import insert


def load_table_authorized_users(login: str, hash_password: str):
    """
    Функция загружает данные в базу данных, в таблицу "authorized_users".
    """

    insert_authorized_users = [
        {"login": login, "password": hash_password},
    ]

    insert_value = session.scalars(
        insert(Authorized_users).returning(Authorized_users), insert_authorized_users
    )
    result = insert_value.all()

    session.commit()


def recieve_user_login(input_login: str):
    """
    Функция ищет пользователя по логину в базе данных
    :param input_login: str
    :return: str
    """
    user = session.query(Authorized_users).filter(Authorized_users.login == input_login).first()
    if user is None:
        return None
    user_login = user.login
    return user_login


def search_password(input_login: str) -> None | str:
    """
    Функция ищет пользователя по логину и возращает хешированный пароль
    :param input_login: str
    :return: str
    """
    user = (
        session.query(Authorized_users)
        .filter(Authorized_users.login == input_login)
        .first()
    )
    if user is None:
        return None
    hash_password = user.password
    return hash_password


connection = engine.connect()
print("подключено")
connection.close()
