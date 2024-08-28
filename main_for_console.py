from working_with_the_user import big_work_with_user

from get_soup_from_city_dodo import parsing_dodo_pizza
from get_soup_from_city_tashir import parsing_tashir_pizza
from get_soup_from_city_tomato import parsing_tomato_pizza


def main():
    brands = big_work_with_user()
    print(brands)

    for name_brand, cities in brands.items():
        print(name_brand, cities)
        if name_brand == 'Додо':
            for city in cities:
                parsing_dodo_pizza(name_brand, city)
        elif name_brand == 'Ташир':
            for city in cities:
                parsing_tashir_pizza(name_brand, city)
        elif name_brand == 'Томато':
            for city in cities:
                parsing_tomato_pizza(name_brand, city)


if __name__ == "__main__":
    main()
