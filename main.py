# from get_soup_from_city_dodo import parsing_dodo_pizza
# from get_soup_from_city_tashir import parsing_tashir_pizza
from get_soup_from_city_tomato import parsing_tomato_pizza


def main():
    brands = [{'Додо': ['Абакан', 'Абинск', 'Адлер', 'Азов']},
              {'Ташир': ['Аксай', 'Астрахань', 'Белгород', 'Волгоград', 'Волжский']},
              {'Томато': ['Белгород', 'Воронеж', 'Калуга', 'Обнинск', 'Курск', 'Елец']}]

    for brand in brands:
        for name_brand, cities in brand.items():
            if name_brand == 'Додо':
                dodo_cities = cities
                # print(name_brand, dodo_cities)
                # parsing_dodo_pizza(dodo_cities)
            elif name_brand == 'Ташир':
                tashir_cities = cities
                # print(name_brand, tashir_cities)
                # parsing_tashir_pizza(tashir_cities)
            elif name_brand == 'Томато':
                tomato_cities = cities
                print(tomato_cities)
                parsing_tomato_pizza(tomato_cities)


if __name__ == "__main__":
    main()
