from parser import find_url_cities
import nltk


def input_cities() -> list:
    """
    Функция возращает список городов, коротые пользователь ввел.
    return: list
    """

    list_cities = []

    while True:
        write_city = input("Напишите город. Остановить ввод нажмите Enter:  ")
        if write_city == '':
            break
        else:
            list_cities.append(write_city)

    return list_cities


def correct_write_city(list_cities: list) -> list:
    """
    Функция возращает список городов, которые правильно написал пользователь
    param list_cities: list
    return: list
    """

    all_url_cities = find_url_cities()
    all_city = all_url_cities.keys()
    correct_city = []

    for city in list_cities:
        if city in all_city:
            correct_city.append(city)

    return correct_city


def incorrect_write_city(list_cities: list) -> list:
    """
    Функция возращает список городов, которые не правильно написал пользователь
    param list_cities: list
    return: list
    """

    all_url_cities = find_url_cities()
    all_city = all_url_cities.keys()
    incorrect_city = []

    for city in list_cities:
        if city not in all_city:
            incorrect_city.append(city)

    return incorrect_city


def presumably_correct_cities(incorrect_cities: list) -> list:
    """
    Функция возращает список городов, в котором есть несколько вариантов
    param incorrect_cities: list
    return: list
    """

    all_url_cities = find_url_cities()
    all_city = all_url_cities.keys()
    presumably_cities = []
    count = 1

    for input_city in incorrect_cities:
        find_correct_city = {}
        for city in all_city:
            if len(city) <= 6:
                change = nltk.jaccard_distance(set(input_city), set(city))
                if change <= 0.4:
                    find_correct_city[count] = city
                    count += 1
            elif 7 <= len(city) <= 12:
                change = nltk.jaccard_distance(set(input_city), set(city))
                if change <= 0.35:
                    find_correct_city[count] = city
                    count += 1
            elif len(city) > 12:
                change = nltk.jaccard_distance(set(input_city), set(city))
                if change <= 0.3:
                    find_correct_city[count] = city
                    count += 1

        count = 1
        presumably_cities.append(find_correct_city)

    return presumably_cities


def choosing_from_proposed_cities(presumably_cities: list) -> list:
    """
    Функция возращает корретные города. Пользователь выбирает из предположительно правильных
    param presumably_cities: list
    return: list
    """

    find_correct_city = []

    for city in presumably_cities:
        for number, find_city in city.items():
            print(f'{find_city} -> {number}')
        print()
        print("Не правильно написан город.")
        print("Какой город вы имели ввиду?")
        write_number = int(input("Напишите число города, который подходит: "))

        find_city = city[write_number]

        find_correct_city.append(find_city)
        print()

    return find_correct_city


def get_correct_city() -> list:
    """
    Функия возращает корректные города.
    return: list
    """
    list_cities = input_cities()  # пользователь вводит города
    correct_city = correct_write_city(list_cities)  # получение корректных городов
    incorrect_city = incorrect_write_city(list_cities)  # получение не корректных городов
    presumably_cities = presumably_correct_cities(incorrect_city)  # возможные варианты городов
    corrected_cities = choosing_from_proposed_cities(presumably_cities)  # пользователь выбыирает корректный город
    all_correct_city = correct_city + corrected_cities  # получение городов, которые вписал пользователь
    return all_correct_city
