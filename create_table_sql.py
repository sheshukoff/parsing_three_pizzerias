from sqlalchemy import create_engine, Integer, String, Column, ForeignKey, SmallInteger
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from dotenv import dotenv_values


class Base(DeclarativeBase):
    pass


class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True)

    def __repr__(self):
        return f"Brand id={self.id}, name={self.name}"


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True)

    def __repr__(self):
        return f"City id={self.id}, name={self.name}"


class Section(Base):
    __tablename__ = "section"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)

    def __repr__(self):
        return f"Section id={self.id}, name={self.name}"


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    new_price = Column(SmallInteger)
    old_price = Column(SmallInteger)
    brand_id = Column(Integer, ForeignKey("brand.id"))
    city_id = Column(Integer, ForeignKey("city.id"))
    section_id = Column(Integer, ForeignKey("section.id"))

    def __repr__(self):
        return f"Product id={self.id}, name={self.name}, description={self.description}, new_price={self.new_price}"


config = dotenv_values(".env")

USERNAME = config.get("USERNAME")
PASSWORD = config.get("PASSWORD")
HOST = config.get("HOST")
PORT = config.get("PORT")
DATABASE = config.get("DATABASE")

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
