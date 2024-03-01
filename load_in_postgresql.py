from create_table_sql import Brand, City, Section, Product
from create_table_sql import session
from sqlalchemy import insert


def int_price(price: str) -> int | None:
    """
    Функция принимает на входе цены в str формате. На выходе получаем цену в формате - int.
    param price: str
    return: int | None
    """

    if price is None:
        return None

    new_price = ""

    for element in price:
        if element.isdigit():
            new_price += element

    if len(new_price) == 0:
        return None
    else:
        return int(new_price)


def get_brand_id(name_brand: str) -> int | None:
    """
    Функция ищет id бренда по названию в базе данных
    :param name_brand: str
    :return: int | None
    """
    brand = session.query(Brand).filter(Brand.name == name_brand).first()
    if brand:
        return brand.id
    return None


def get_city_id(name_city: str) -> int | None:
    """
    Функция ищет id города по названию в базе данных
    :param name_city: str
    :return: int | None
    """

    city = session.query(City).filter(City.name == name_city).first()
    if city:
        return city.id
    return None


def get_section_id(name_section: str) -> int | None:
    """
    Функция ищет id секции по названию в базе данных
    :param name_section: str
    :return: int | None
    """

    section = session.query(Section).filter(Section.name == name_section).first()
    if section:
        return section.id
    return None


def update_date_product(brand_id: int, city_id: int):
    """
    Функция удаляет данные по бренду в определенном городе.
    :param brand_id: int
    :param city_id: int
    """
    data_to_delete = (
        session.query(Product)
        .filter(Product.brand_id == brand_id)
        .filter(Product.city_id == city_id).all()
    )

    for item in data_to_delete:
        session.delete(item)

    session.commit()


def load_table_brand(brand: str):
    """
    Функция загружает данные в базу данных, в таблицу "brand".
    Пример ('Додо пицца')
    :param brand: str
    """

    insert_brand = [
        {"name": brand},
    ]

    insert_value = session.scalars(insert(Brand).returning(Brand), insert_brand)
    result = insert_value.all()
    print(result)

    session.commit()


def load_table_city(name_city: str):
    """
    Функция загружает данные в базу данных, в таблицу "city".
    Пример ('Воронеж')
    :param name_city: str
    """

    insert_city = [
        {"name": name_city},
    ]

    insert_value = session.scalars(insert(City).returning(City), insert_city)
    result = insert_value.all()
    print(result)

    session.commit()


def load_table_section(name_section: str):
    """
    Функция загружает данные в базу данных, в таблицу "section".
    Пример ('Пицца', 'Закуски' и т.п)
    :param name_section: str
    """

    insert_section = [
        {"name": name_section},
    ]

    insert_value = session.scalars(insert(Section).returning(Section), insert_section)
    result = insert_value.all()
    print(result)

    session.commit()


def load_database_description_product_card(data_from_locality: dict[list[dict]], brand_id: int, city_id: int):
    """
    Функция загружает данные в базу данных, в таблицу 'product'.
    :param data_from_locality: dict[list[dict]]
    :param brand_id: int
    :param city_id: int
    """

    for section, products_cards in data_from_locality.items():
        section_id = get_section_id(section)
        if not section_id:
            load_table_section(section)

            section_id = get_section_id(section)
        print(section_id, section)
        for product_card in products_cards:
            name = product_card.get("name")
            description = product_card.get("description")
            new_price = product_card.get("new_price")
            new_price = int_price(new_price)
            old_price = product_card.get("old_price")
            old_price = int_price(old_price)

            insert_product_card = [
                {
                    "name": name,
                    "description": description,
                    "new_price": new_price,
                    "old_price": old_price,
                    "brand_id": brand_id,
                    "city_id": city_id,
                    "section_id": section_id,
                },
            ]

            insert_value = session.scalars(
                insert(Product).returning(Product), insert_product_card
            )
            result = insert_value.all()
            print(result)

    session.commit()


session.close()
