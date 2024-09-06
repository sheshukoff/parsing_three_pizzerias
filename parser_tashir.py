from bs4 import BeautifulSoup


def get_name(figure: BeautifulSoup) -> str:
    """
    Функция возвращает название продукта
    :param figure: BeautifulSoup
    :return: str
    """

    return figure.a.text.strip()


def get_description(figure: BeautifulSoup) -> str | None:
    """
    Функция возвращает описание продукта
    :param figure: BeautifulSoup
    :return: str | None
    """

    description = figure.find("span", {"class": "descr"}).text.strip()

    if description == "":
        return None

    return description


def get_price(figure: BeautifulSoup) -> str:
    """
    Функция возращает цену.
    :param figure: BeautifulSoup
    :return: str
    """
    new_price = figure.find("span", {"class": "price"}).text.strip()
    return new_price


def get_new_and_old_prices(div: BeautifulSoup) -> tuple:
    """
    Функция возращает новую и страрую цену.
    :param div: BeautifulSoup
    :return: tuple
    """
    get_old_price = div.div.extract()
    old_price = get_old_price.text.strip()

    new_price = div.text.strip()
    return new_price, old_price


def get_product_data(product_card: BeautifulSoup) -> dict:
    """
    Функция возращает все поля из карточки продукта
    :param product_card: BeautifulSoup
    :return: dict
    """

    new_price = None
    old_price = None

    figure = product_card

    name = get_name(figure)
    description = get_description(figure)
    new_price = get_price(figure)

    description_card_product = {
        "name": name,
        "description": description,
        "new_price": new_price,
        "old_price": old_price,
    }

    return description_card_product


def get_products_cards_from_section(section: BeautifulSoup) -> BeautifulSoup:
    """
    Функция возращает товары из секции
    :param section: BeautifulSoup
    :return: BeautifulSoup
    """
    product_cards = section.find_all("figure")
    return product_cards


def get_sections_from_page(page_soup: BeautifulSoup) -> BeautifulSoup:
    """
    Функция возращает список секций
    :param page_soup: BeautifulSoup
    :return: BeautifulSoup
    """

    sections = page_soup.find_all("section", {"class": "products"})
    return sections


def get_name_catalog(soup_page) -> list:
    """
    Функция возращает список
    :param soup_page: BeautifulSoup
    :return: list
    """
    sections = soup_page.find("section", {"class": "wrap catalogs"})
    section_pizza = sections.section.h1
    other_section = sections.find_all("strong")

    other_section.insert(0, section_pizza)

    return other_section


def get_page_soup_from_file(file_name: str) -> BeautifulSoup:
    """
    Функция возращает html разметку из файла
    :param file_name: str
    :return: BeautifulSoup
    """
    with open(file_name, "r", encoding="utf-8") as file:
        file_html = file.read()

    soup = BeautifulSoup(file_html, "html.parser")

    return soup


def get_data_from_locality_tashir(file_name: str) -> dict[list[dict]]:
    """
    Функция парсит данные со страницы населенного пункта или города.
    :param file_name: str
    :return: dict[list[dict]]
    """
    result = {}

    page_soup = get_page_soup_from_file(file_name)  # получение html страницы
    all_sections = get_sections_from_page(page_soup)
    all_name_section = get_name_catalog(page_soup)

    i = 0
    for section in all_sections:
        temp = []
        name_section = all_name_section[i].text.strip()
        products_cards = get_products_cards_from_section(section)
        for product_card in products_cards:
            definition_card = get_product_data(product_card)
            temp.append(definition_card)

        result[name_section] = temp
        i += 1

    return result
