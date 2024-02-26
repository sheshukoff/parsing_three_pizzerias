from working_with_the_user import big_work_with_user

from get_soup_from_city_dodo import parsing_dodo_pizza
from get_soup_from_city_tashir import parsing_tashir_pizza
from get_soup_from_city_tomato import parsing_tomato_pizza


def main():
    brands = big_work_with_user()

    for brand in brands:
        for name_brand, cities in brand.items():
            if name_brand == 'Додо':
                parsing_dodo_pizza(name_brand, cities)
            elif name_brand == 'Ташир':
                parsing_tashir_pizza(name_brand, cities)
            elif name_brand == 'Томато':
                parsing_tomato_pizza(name_brand, cities)


if __name__ == "__main__":
    main()
