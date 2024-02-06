from dotenv import dotenv_values
from sqlalchemy import create_engine, text

config = dotenv_values("..\.env")

USERNAME = config.get('USERNAME')
PASSWORD = config.get('PASSWORD')
HOST = config.get('HOST')
PORT = config.get('PORT')
DATABASE = config.get('DATABASE')

engine = create_engine(
    f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
)

def recieve_cities():

    connection = engine.connect()

    print('подключено')
    choose_brand = ['dodo', 'tashir', 'tomato']

    tomato = 'tomato'
    tashir = 'tashir'

    sql = text('select dodo from choose_city where (tomato) is not null')
    result = connection.execute(sql)

    list_city = []

    for row in result:
        list_city.append(row[0])

    connection.close()
    return list_city


if __name__ == '__main__':
    recieve_cities()














# Создаём таблицы
# Base.metadata.create_all(engine)

# Создаём сессию для работы с базой данных
# Session = sessionmaker(bind=engine)
# session = Session()