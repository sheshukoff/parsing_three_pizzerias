from bs4 import BeautifulSoup


def is_digit(div):
    new_price = ''
    for symbol in div:
        if symbol.isdigit():
            new_price += symbol

    return new_price


def get_name(div: BeautifulSoup) -> str:
    """
    Функция возвращает название продукта
    :param div: BeautifulSoup
    :return: str
    """
    return div.text.strip()


def get_description(main: BeautifulSoup) -> str | None:
    """
    Функция возвращает описание продукта
    :param main: BeautifulSoup
    :return: str | None
    """

    description = main.text.strip()

    if description == "":
        return None

    return description


def get_new_price(div_new_price) -> str | None:
    """
    Функция возращает новую цену.
    param div: BeautifulSoup
    return: None | int
    """
    if div_new_price is None:
        return None
    new_price = div_new_price.text.strip().split('₽')

    if 'от' in new_price:
        return is_digit(new_price[1])

    return is_digit(new_price[0])


def get_old_price(div_old_price) -> str | None:
    """
    Функция возращает старую цену.
    param div: BeautifulSoup
    return: str
    """

    if div_old_price is None:
        return None
    old_price = div_old_price.text.strip()
    return is_digit(old_price[:-1])


def get_product_data(product_card: BeautifulSoup) -> dict:
    """
    Функция возращает все поля из карточки продукта
    :param product_card: BeautifulSoup
    :return: dict
    """

    new_price = None
    old_price = None

    article = product_card

    main = article.main
    main.picture.decompose()  # удаляю блок picture он не нужен # +
    div = main.div.extract()  # удалил блок div и вернул его в качестве результата # +

    name = get_name(div)
    description = get_description(main)

    footer = article.footer

    div_price = footer.find("div", {"class": "product-control-price"})
    if div_price:
        div_new_price = footer.find("div", {"class": "product-control-price"})
        div_old_price = footer.find("div", {"class": "product-control-oldprice"})
        new_price = get_new_price(div_new_price)
        old_price = get_old_price(div_old_price)
    else:
        div_new_price = footer.text.strip()
        new_price = is_digit(div_new_price)

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
    cards_products = section.find_all("article")
    return cards_products


def get_sections_from_page(page_soup: BeautifulSoup) -> BeautifulSoup:
    """
    Функция возращает список секций
    :param page_soup: BeautifulSoup
    :return: BeautifulSoup
    """
    sections = page_soup.main.find_all("section")
    return sections


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


def get_data_from_locality_dodo(file_name: str) -> dict[list[dict]]:
    """
    Функция парсит данные со страницы населенного пункта или города.
    :param file_name: str
    :return: dict[list[dict]]
    """
    result = {}

    page_soup = get_page_soup_from_file(file_name)  # получение html страницы
    sections_page = get_sections_from_page(page_soup)

    for section in sections_page:
        temp = []
        if "id" in section.attrs.keys():
            name_sections = section.h2.text.strip()
            cards_products = get_products_cards_from_section(section)
            for product_card in cards_products:
                definition_product = get_product_data(product_card)
                temp.append(definition_product)

            result[name_sections] = temp

    return result
