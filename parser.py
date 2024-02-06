from bs4 import BeautifulSoup


def find_url_cities() -> dict:
    """
    Функция на возращает all_url_cities. Пример -> ('Воронеж': '/voronezh').
    return: dict
    """

    URL = 'URLS.html'

    all_url_cities = {}

    soup = get_page_soup_from_file(URL)
    table_cities = soup.find("div", {"class": "locality-selector-popup__table"})
    all_tags_a = table_cities.find_all("a")

    for city in all_tags_a:
        all_url_cities[city.text.strip()] = city['href']

    return all_url_cities


def get_name(div: BeautifulSoup) -> str:
    """
    Функция возвращает название продукта
    param div: BeautifulSoup
    return: str
    """
    return div.text.strip()


def get_description(main: BeautifulSoup) -> str | None:
    """
    Функция возвращает описание продукта
    param main: BeautifulSoup
    return str | None
    """

    description = main.text.strip()

    if description == '':
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

    article = product_card

    main = article.main
    main.picture.decompose()  # удаляю блок picture он не нужен # +
    div = main.div.extract()  # удалил блок div и вернул его в качестве результата # +

    name = get_name(div)
    description = get_description(main)

    footer = article.footer
    div_price = footer.find("div", {"class": "product-control-price"})

    if div_price.div is None:
        new_price = get_price(div_price)
    else:
        new_price, old_price = get_new_and_old_prices(div_price)

    description_card_product = {
        'name': name,
        'description': description,
        'new_price': new_price,
        'old_price': old_price
    }

    return description_card_product


def get_products_cards_from_section(section: BeautifulSoup) -> BeautifulSoup:
    """
    Функция возращает товары из секции
    param section: BeautifulSoup
    return: BeautifulSoup
    """
    cards_products = section.find_all("article")
    return cards_products


def get_sections_from_page(page_soup: BeautifulSoup) -> BeautifulSoup:
    """
    Функция возращает список секций
    param page_soup: BeautifulSoup
    return: BeautifulSoup
    """
    sections = page_soup.main.find_all("section")
    return sections


def get_page_soup_from_file(file_name: str) -> BeautifulSoup:
    """
    Функция возращает html разметку из файла
    param file_name: str
    return: BeautifulSoup
    """
    with open(file_name, "r", encoding='utf-8') as file:  # правильное открытие файла в формате html
        file_html = file.read()

    soup = BeautifulSoup(file_html, 'html.parser')

    return soup


def get_data_from_locality(file_name: str) -> dict[list[dict]]:
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
        if 'id' in section.attrs.keys():
            name_sections = section.h2.text.strip()
            cards_products = get_products_cards_from_section(section)
            for product_card in cards_products:
                definition_product = get_product_data(product_card)
                temp.append(definition_product)

            result[name_sections] = temp

    return result


# TODO Вынести в функцию пользоватся когда парсить с телефона
# chrome_options.add_argument("user-agent=Mozilla/5.0"
#                             " (iPhone; CPU iPhone OS 14_6 like Mac OS X)"
#                             " AppleWebKit/605.1.15 (KHTML, like Gecko) "
#                             "Version/14.0.3 Mobile/15E148 Safari/604.1") # парсинг со смартфона
# driver = webdriver.Chrome(options=chrome_options) # веб драйвер
#  {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 24, 25, 26, 27, 28, 29, 31, 32} длинна слова
