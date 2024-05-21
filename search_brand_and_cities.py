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
    found_brand_and_city = {
        'dodo_true': [],
        'tashir_true': [],
        'tomato_true': [],
        'dodo_false': [],
        'tashir_false': [],
        'tomato_false': [],
    }

    for city, brands in found_brand_city.items():
        if brands['dodo_value'] is True:
            found_brand_and_city['dodo_true'].append(city)
        else:
            found_brand_and_city['dodo_false'].append(city)
        if brands['tashir_value'] is True:
            found_brand_and_city['tashir_true'].append(city)
        else:
            found_brand_and_city['tashir_false'].append(city)
        if brands['tomato_value'] is True:
            found_brand_and_city['tomato_true'].append(city)
        else:
            found_brand_and_city['tomato_false'].append(city)

    return found_brand_and_city


def changes_in_data(found_brand_and_city, data):
    print(found_brand_and_city)
    print(data[:30])

    for cities in data:
        if len(found_brand_and_city['dodo_true']) != 0:
            for city in found_brand_and_city['dodo_true']:
                if cities['city'] == city:
                    cities['dodo_value'] = True

        elif len(found_brand_and_city['dodo_true']) == 0:
            print(f'Список {found_brand_and_city['dodo_true']} пустой')

        if len(found_brand_and_city['dodo_false']) != 0:
            for city in found_brand_and_city['dodo_false']:
                if cities['city'] == city:
                    cities['dodo_value'] = False

        elif len(found_brand_and_city['dodo_false']) == 0:
            print(f'Список {found_brand_and_city['dodo_false']} пустой')

        if len(found_brand_and_city['tashir_true']) != 0:
            for city in found_brand_and_city['tashir_true']:
                if cities['city'] == city:
                    cities['tashir_value'] = True

        elif len(found_brand_and_city['tashir_true']) == 0:
            print(f'Список {found_brand_and_city['tashir_true']} пустой')

        if len(found_brand_and_city['tashir_false']) != 0:
            for city in found_brand_and_city['tashir_false']:
                if cities['city'] == city:
                    cities['tashir_value'] = False

        elif len(found_brand_and_city['tashir_false']) == 0:
            print(f'Список {found_brand_and_city['tashir_false']} пустой')

        if len(found_brand_and_city['tomato_true']) != 0:
            for city in found_brand_and_city['tomato_true']:
                if cities['city'] == city:
                    cities['tomato_value'] = True

        elif len(found_brand_and_city['tomato_true']) == 0:
            print(f'Список {found_brand_and_city['tomato_true']} пустой')

        if len(found_brand_and_city['tomato_false']) != 0:
            for city in found_brand_and_city['tomato_false']:
                if cities['city'] == city:
                    cities['tomato_value'] = False

        elif len(found_brand_and_city['tomato_false']) == 0:
            print(f'Список {found_brand_and_city['tomato_false']} пустой')
