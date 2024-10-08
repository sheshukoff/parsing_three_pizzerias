from bs4 import BeautifulSoup
from update_urls_cities import update_url_cities_dodo, update_url_cities_tashir, \
    update_url_cities_tomato, write_file_urls


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


def find_url_cities_dodo() -> dict:
    """
    Функция на возращает all_url_cities. Пример -> ('Воронеж': '/voronezh').
    :return: dict
    """

    URL = 'URLS_Додо.html'

    all_url_cities = {}

    soup = get_page_soup_from_file(URL)
    table_cities = soup.find("div", {"class": "locality-selector-popup__table"})
    print(table_cities)
    all_tags_a = table_cities.find_all("a")

    for city in all_tags_a:
        all_url_cities[city.text.strip()] = city['href']

    return all_url_cities


def find_url_cities_tashir() -> dict:
    """
    Функция на возращает all_url_cities. Пример -> ('Воронеж': '/voronezh').
    :return: dict
    """

    URL = 'URLS_Ташир.html'

    all_url_cities = {}

    soup = get_page_soup_from_file(URL)

    table_cities = soup.find("div", {"class": "cont"})

    all_tags_a = table_cities.find_all("a")

    for city in all_tags_a:
        all_url_cities[city.text.strip()] = city['href']

    return all_url_cities


def find_url_cities_tomato() -> dict:
    """
    Функция на возращает all_url_cities. Пример -> ('Воронеж': '/voronezh').
    :return: dict
    """

    URL = 'URLS_Томато.html'

    all_url_cities = {}

    soup = get_page_soup_from_file(URL)
    table_cities = soup.find_all("ul", {"class": "cities-cities"})

    for section in table_cities:
        for cities in section:
            city = cities.find("div")
            if city == -1:
                continue
            else:
                tag_a = cities.find("a", {"class": "text-underline"})["href"]
                url_city = f"{tag_a.split('/')[2]}"
                name_city = city.text.strip()

                all_url_cities[name_city] = url_city

    return all_url_cities


def choose_brand():
    """
    Функция возращает список брендов, коротые выбрал пользователь.
    :return: list
    """
    BRAND_LIST = ["Додо", "Ташир", "Томато"]
    selected_brands = []

    while True:
        print("Выберите бренд или введите 'готово', чтобы закончить:")
        for number, brand in enumerate(BRAND_LIST, 1):
            print(f"{number}. {brand}")

        choice = input()

        if choice.isdigit() and 1 <= int(choice) <= len(BRAND_LIST):
            selected_brands.append(BRAND_LIST[int(choice) - 1])
            BRAND_LIST.remove(BRAND_LIST[int(choice) - 1])
        elif choice.lower() == "готово":
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите число от 1 до", len(BRAND_LIST))

    print("Выбранные бренды:")
    for brand in selected_brands:
        print(brand)

    return selected_brands


def choose_city(brand: str, url_cities_brand: dict) -> list:
    """
    Функция возращает список брендов, коротые выбрал пользователь.
    :param brand: str
    :param url_cities_brand: dict
    :return: dict
    """
    list_cities = list(url_cities_brand.keys())
    selected_cities = []

    while True:
        for number, city in enumerate(list_cities, 1):
            print(f"{number} -- {city}")
        print(f'Выберите "номер" города для бренда {brand} или введите "готово", чтобы закончить ->')
        choice = input()

        if choice.isdigit() and 1 <= int(choice) <= len(list_cities):
            selected_cities.append(list_cities[int(choice) - 1])
            list_cities.remove(list_cities[int(choice) - 1])
        elif choice.lower() == "готово":
            break
        else:
            print(f"Некорректный ввод. Пожалуйста, выберите число от 1 до {len(list_cities)}")

    return selected_cities


def get_city_for_brand(list_brands: list) -> dict:
    """
    Функция возращает список городов для брендов
    :param list_brands: str
    :return: list
    """

    cities_for_brand = {'Додо': [], 'Ташир': [], 'Томато': []}

    for brand in list_brands:
        if brand == "Додо":
            url_cities_dodo = find_url_cities_dodo()
            selected_cities_dodo = choose_city(brand, url_cities_dodo)
            cities_for_brand['Додо'] = selected_cities_dodo
            print("Выбранные города:")
            print(selected_cities_dodo)
        elif brand == "Ташир":
            url_cities_tashir = find_url_cities_tashir()
            selected_cities_tashir = choose_city(brand, url_cities_tashir)
            cities_for_brand['Ташир'] = selected_cities_tashir
            print("Выбранные города:")
            print(selected_cities_tashir)
        elif brand == "Томато":
            url_cities_tomato = find_url_cities_tomato()
            selected_cities_tomato = choose_city(brand, url_cities_tomato)
            cities_for_brand['Томато'] = selected_cities_tomato
            print("Выбранные города:")
            print(selected_cities_tomato)

    return cities_for_brand


def update_cities_for_brands():
    list_brands = choose_brand()
    for brand in list_brands:
        if brand == 'Додо':
            soup_dodo = update_url_cities_dodo()
            write_file_urls(soup_dodo, brand)
            print(f'Города бренда "{brand}" обновлены')
        elif brand == 'Ташир':
            soup_tashir = update_url_cities_tashir()
            write_file_urls(soup_tashir, brand)
            print(f'Города бренда "{brand}" обновлены')
        elif brand == 'Томато':
            soup_tomato = update_url_cities_tomato()
            write_file_urls(soup_tomato, brand)
            print(f'Города бренда "{brand}" обновлены')


def big_work_with_user() -> dict:
    """
    Функция для работы с пользователем. Обновляет города, которые будут доступны для пользователяю.
    :return: list
    """

    input_message = input("Нужно ли обновить города по пиццериям напишите Y/n: ")
    if input_message.lower() == 'y':
        update_cities_for_brands()
    elif input_message.lower() == 'n':
        list_brands = choose_brand()

    return get_city_for_brand(list_brands)
