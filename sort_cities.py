from working_with_the_user import find_url_cities_dodo, find_url_cities_tashir, find_url_cities_tomato


def search_brand_on_cities() -> dict:
    """
    Функция возврвщает наличие бренда в городах
    :return: object
    """
    cities_dodo = find_url_cities_dodo()
    cities_tashir = find_url_cities_tashir()
    cities_tomato = find_url_cities_tomato()

    list_city_dodo = list(cities_dodo.keys())
    list_city_tashir = list(cities_tashir.keys())
    list_city_tomato = list(cities_tomato.keys())

    brand_dodo = {'Додо': list_city_dodo}
    brand_tashir = {'Ташир':  list_city_tashir}
    brand_tomato = {'Томато': list_city_tomato}

    common_cities = set(brand_dodo['Додо']) & set(brand_tashir['Ташир']) & set(brand_tomato['Томато'])

    cities2 = (
            set(brand_dodo['Додо']) & set(brand_tashir['Ташир']) |
            set(brand_dodo['Додо']) & set(brand_tomato['Томато']) |
            set(brand_tashir['Ташир']) & set(brand_tomato['Томато'])
    )
    cities1 = set(brand_dodo['Додо']) | set(brand_tashir['Ташир']) | set(brand_tomato['Томато'])

    result_cities = {'common': list(common_cities), 'two_brands': list(cities2 - common_cities),
                     'one_brand': list(cities1 - cities2)}

    single_sheet = {}

    for brand, cities in result_cities.items():
        for city in cities:
            temp = []
            if city in (brand_dodo['Додо']):
                temp.append(True)
            else:
                temp.append(False)

            if city in (brand_tashir['Ташир']):
                temp.append(True)
            else:
                temp.append(False)

            if city in (brand_tomato['Томато']):
                temp.append(True)
            else:
                temp.append(False)
            single_sheet[city] = temp

    return single_sheet


def sorted_cities(brand_cities: dict) -> dict:
    """
    Функция сортирует города
    :param brand_cities: list
    :return: dict
    """
    sort_cities = {}

    temp = {}

    for city, brands in brand_cities.items():
        if brands == [True, True, True]:
            temp[city] = brands

    sorted_brand_cities = dict(sorted(temp.items()))
    sort_cities = sort_cities | sorted_brand_cities

    temp = {}

    for city, brands in brand_cities.items():
        if brands == [True, False, True]:
            temp[city] = brands

    sorted_brand_cities = dict(sorted(temp.items()))
    sort_cities = sort_cities | sorted_brand_cities

    temp = {}

    for city, brands in brand_cities.items():
        if brands == [False, False, True]:
            temp[city] = brands

    sorted_brand_cities = dict(sorted(temp.items()))
    sort_cities = sort_cities | sorted_brand_cities

    temp = {}

    for city, brands in brand_cities.items():
        if brands == [True, True, False]:
            temp[city] = brands

    sorted_brand_cities = dict(sorted(temp.items()))
    sort_cities = sort_cities | sorted_brand_cities

    temp ={}

    for city, brands in brand_cities.items():
        if brands == [True, False, False]:
            temp[city] = brands

    sorted_brand_cities = dict(sorted(temp.items()))
    sort_cities = sort_cities | sorted_brand_cities

    return sort_cities


def sorted_brand_and_cities() -> dict:
    """
    Функция возвращает отсортированный словарь городов
    :return: dict
    """
    brand_and_cities = search_brand_on_cities()
    sort_cities = sorted_cities(brand_and_cities)
    return sort_cities


def create_dash_table() -> list:
    """
    Функция возвращает список брендов и городов (для frontend'a)
    :return: list
    """
    data_frame = sorted_brand_and_cities()

    data = []

    for city, brands in data_frame.items():
        dodo, tashir, tomato = brands

        data.append({
            'city': city,
            'dodo': dodo,
            'dodo_value': False,
            'tashir': tashir,
            'tashir_value': False,
            'tomato': tomato,
            'tomato_value': False
        },
        )
    return data
