# import time
#
#
# def calculate_percent(brand_cities: list) -> int:
#     length_list = len(brand_cities)
#     if length_list == 0:
#         return 100
#
#     return 100 // length_list
#
#
# def increment_percent(percent):
#     global count_percent
#     count_percent += percent
#     return count_percent
#
#
# def is_last_element(element: str, any_list: list) -> bool:
#     if element == any_list[-1]:
#         return True
#     return False
#
#
# brands = {'Додо': ['Воронеж', 'Белгород', 'Калуга', 'Москва', 'Ростов', 'Аскай'],
#           'Ташир': [],
#           'Томато': ['Воронеж', 'Белгород', 'Калуга', 'Москва']}
#
# # brands = {'Ташир': []}
#
#
# for brand, cities in brands.items():
#     count_percent = 0
#     percent_incremet = calculate_percent(cities)
#
#     if percent_incremet == 100:
#         print(f"Парсинг {brand} - {percent_incremet}%")
#
#     for city in cities:
#         if is_last_element(city, cities):
#             now_percent = 100
#             print(f"Парсинг {brand} - {now_percent}%")
#         else:
#             now_percent = increment_percent(percent_incremet)
#             print(f"Парсинг {brand} - {now_percent}%")
#         time.sleep(1)
#     print()


print(100//1)
