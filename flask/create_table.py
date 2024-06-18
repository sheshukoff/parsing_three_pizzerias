from dotenv import dotenv_values
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass


class Authorized_users(UserMixin, Base):
    __tablename__ = "authorized_users"

    id = Column(Integer, primary_key=True)
    login = Column(String(20), nullable=False, unique=True)
    password = Column(String(60), nullable=False)


config = dotenv_values(".env")

USERNAME = config.get("USERNAME")
PASSWORD = config.get("PASSWORD")
HOST = config.get("HOST")
PORT = config.get("PORT")
DATABASE = config.get("DATABASE")

# Создаем подключение к базе данных PostgreSQL
engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# Создаём таблицы
Base.metadata.create_all(engine)

# Создаём сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()
