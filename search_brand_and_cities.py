def split_array(choose_user_cities: list) -> list[list]:
    split_choose_user = []
    index = 0

    # Цикл, который берет по три элемента из списка
    while index < len(choose_user_cities):
        three_elements = choose_user_cities[index:index + 3]
        split_choose_user.append(three_elements)
        index += 3

    return split_choose_user


def search_brand_city(split_choose_user, table):  # здесь состояние переключателя
    search_brand_cities = {}
    for num, cities in enumerate(table):
        temp = {}
        for number in range(0, 3):
            if number == 0:
                temp['dodo_value'] = split_choose_user[num][number]
            elif number == 1:
                temp['tashir_value'] = split_choose_user[num][number]
            elif number == 2:
                temp['tomato_value'] = split_choose_user[num][number]
        search_brand_cities[cities['city']] = temp

    return search_brand_cities


def sort_brand_and_city(found_brand_city):
    found_brand_and_city = {'dodo': [], 'tashir': [], 'tomato': []}

    for city, brands in found_brand_city.items():
        if brands['dodo_value'] is True:
            found_brand_and_city['dodo'].append(city)
        if brands['tashir_value'] is True:
            found_brand_and_city['tashir'].append(city)
        if brands['tomato_value'] is True:
            found_brand_and_city['tomato'].append(city)

    return found_brand_and_city


def changes_in_data(found_brand_and_city, data):
    print(found_brand_and_city)
    print(data[:30])

    for cities in data:
        city_dodo = found_brand_and_city['dodo']
        city_tashir = found_brand_and_city['tashir']
        city_tomato = found_brand_and_city['tomato']
        if len(city_dodo) != 0:
            for city in city_dodo:
                if cities['city'] == city:
                    cities['dodo_value'] = True
        elif len(city_dodo) == 0:
            print(f'Список {city_dodo} пустой')

        if len(city_tashir) != 0:
            for city in city_tashir:
                if cities['city'] == city:
                    cities['tashir_value'] = True
        elif len(city_tashir) == 0:
            print(f'Список {city_tashir} пустой')

        if len(city_tomato) != 0:
            for city in city_tashir:
                if cities['city'] == city:
                    cities['tomato_value'] = True
        elif len(city_tomato) == 0:
            print(f'Список {city_tomato} пустой')

    print(f'Изменения в {data} внесены')




