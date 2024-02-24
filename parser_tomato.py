from bs4 import BeautifulSoup


def get_name(div: BeautifulSoup) -> str:
    """
    Функция возвращает название продукта
    param div: BeautifulSoup
    return: str
    """
    return div.text.strip()


def get_description(div: BeautifulSoup) -> str | None:
    """
    Функция возвращает описание продукта
    param main: BeautifulSoup
    return str | None
    """

    description = div.text.strip()

    if description == "":
        return None

    return description


def get_price(div: BeautifulSoup) -> str:
    """
    Функция возращает цену.
    param div: BeautifulSoup
    return: str
    """
    return div.text.strip()


def get_new_and_old_prices(div: BeautifulSoup) -> tuple:
    """
    Функция возращает новую и страрую цену.
    param div: BeautifulSoup
    return tuple
    """
    get_old_price = div.div.extract()
    old_price = get_old_price.text.strip()

    new_price = div.text.strip()
    return new_price, old_price


def get_product_data(product_card: BeautifulSoup) -> dict:
    """
    Функция возращает все поля из карточки продукта
    param product_card: BeautifulSoup
    return: dict
    """

    new_price = None
    old_price = None

    tag_picture = product_card.picture.decompose()

    div_name = product_card.find("div", {"class": "product-name"})
    name = get_name(div_name)

    div_description = product_card.find("div", {"class": "product-description"})
    description = get_description(div_description)

    div_small_price = product_card.find("div", {"class": "product-item-price"})
    price = get_price(div_small_price)

    description_card_product = {
        "name": name,
        "description": description,
        "new_price": price,
        "old_price": old_price,
    }

    return description_card_product


def get_products_cards_from_section(section: BeautifulSoup) -> BeautifulSoup:
    """
    Функция возращает товары из секции
    param section: BeautifulSoup
    return: BeautifulSoup
    """
    cards_products = section.find_all("div", {"class": "product-container"})
    return cards_products


def processing_section_name(page_soup: BeautifulSoup) -> str:
    """
    Функция обрабатывает название секции (В пиццерии ТОМАТО секция 'Пицца в Воронеже: меню с ценами' -> 'Пицца'
    :param page_soup: BeautifulSoup
    :return: str
    """
    title_section = page_soup.find('li', {'class': 'nav-item active tab_selected'})
    name_section = title_section.meta['content']

    return name_section


def get_sections_from_page(page_soup: BeautifulSoup) -> BeautifulSoup:
    """
    Функция возращает список секций
    param page_soup: BeautifulSoup
    return: BeautifulSoup
    """
    sections = page_soup.find_all("div", {"class": "row is-flex"})
    return sections


def get_page_soup_from_file(file_name: str) -> BeautifulSoup:
    """
    Функция возращает html разметку из файла
    param file_name: str
    return: BeautifulSoup
    """
    with open(file_name, "r", encoding="utf-8") as file:
        file_html = file.read()

    soup = BeautifulSoup(file_html, "html.parser")

    return soup


def get_data_from_locality_tomato(file_name: str) -> dict[list[dict]]:
    """
    Функция парсит данные со страницы населенного пункта или города.
    :param file_name: str
    :return: dict[list[dict]]
    """
    result = {}
    page_soup = get_page_soup_from_file(file_name)  # получение html страницы

    sections_page = get_sections_from_page(page_soup)

    for section in sections_page:
        name_section = processing_section_name(page_soup)
        temp = []
        cards_products = get_products_cards_from_section(section)
        for product_card in cards_products:
            definition_product = get_product_data(product_card)
            temp.append(definition_product)

        result[name_section] = temp

    return result
