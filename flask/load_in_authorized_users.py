from create_table import Authorized_users
from create_table import session
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
