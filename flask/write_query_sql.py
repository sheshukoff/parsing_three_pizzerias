from create_table import Authorized_users, session, engine


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


def search_password(input_login: str) -> str:
    """
    Функция ищет пользователя по логину и возращает хешированный пароль
    :param input_login: str
    :return: str
    """
    user = session.query(Authorized_users).filter(Authorized_users.login == input_login).first()
    if user is None:
        return None
    hash_password = user.password
    return hash_password


connection = engine.connect()
print('подключено')
connection.close()