def split_array(choose_user_cities: list) -> list[list]:
    split_choose_user = []
    index = 0

    # Цикл, который берет по три элемента из списка
    while index < len(choose_user_cities):
        three_elements = choose_user_cities[index:index + 3]
        split_choose_user.append(three_elements)
        index += 3

    return split_choose_user


def search_brand_city(split_choose_user, part_table):
    search_brand_cities = {}

    for num, cities in enumerate(part_table):
        temp = {}
        for number in range(0, 3):
            if number == 0:
                temp['Додо'] = split_choose_user[num][number]
            elif number == 1:
                temp['Ташир'] = split_choose_user[num][number]
            elif number == 2:
                temp['Томато'] = split_choose_user[num][number]

        search_brand_cities[cities['city']] = temp

    return search_brand_cities


def sort_brand_and_city(found_brand_city):
    found_brand_and_city = {'Додо': [], 'Ташир': [], 'Томато': []}

    for city, brands in found_brand_city.items():
        if brands['Додо'] is True:
            found_brand_and_city['Додо'].append(city)
        if brands['Ташир'] is True:
            found_brand_and_city['Ташир'].append(city)
        if brands['Томато'] is True:
            found_brand_and_city['Томато'].append(city)

    return found_brand_and_city
