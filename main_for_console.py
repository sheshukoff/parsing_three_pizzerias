from working_with_the_user import big_work_with_user

from get_soup_from_city_dodo import parsing_dodo_pizza
from get_soup_from_city_tashir import parsing_tashir_pizza
from get_soup_from_city_tomato import parsing_tomato_pizza


def definition_parsing(name_brand):
    if name_brand == 'Додо':
        parsing = parsing_dodo_pizza
    elif name_brand == 'Ташир':
        parsing = parsing_tashir_pizza
    elif name_brand == 'Томато':
        parsing = parsing_tomato_pizza
    else:
        raise f'нет такого бренда {name_brand}'

    return parsing


def main():
    brands = big_work_with_user()
    print(brands)

    for name_brand, cities in brands.items():
        print(name_brand, cities)
        parsing = definition_parsing(name_brand)
        if name_brand == 'Додо':
            parsing = parsing_dodo_pizza
        elif name_brand == 'Ташир':
            parsing = parsing_tashir_pizza
        elif name_brand == 'Томато':
            parsing = parsing_tomato_pizza
        else:
            raise f'нет такого бренда {name_brand}'

        for city in cities:
            parsing(name_brand, city)


if __name__ == "__main__":
    main()
