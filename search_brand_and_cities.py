from work_with_dash import data
import numpy as np

import pandas as pd

data = {
    'города': ['Москва', 'Санкт-Петербург', 'Казань'],
    'додо': [True, False, True],
    'ташир': [False, True, False],
    'томато': [False, False, True]
}

df = pd.DataFrame(data)

result = df.loc[df['додо'] == True, ['города', 'додо']]
print(result)

choose_user = [True, False, False, False, True, False, False, False, True, False, False, False, False, False, False,
               False, True, False, False, False, False, True, True, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False, True, False, False, False, False, False, False]

# part_table = data[:15]


split_list = []

# Инициализируем переменную для хранения текущего индекса
index = 0

# Цикл, который берет по три элемента из списка
while index < len(choose_user):
    three_elements = choose_user[index:index + 3]
    split_list.append(three_elements)
    index += 3

# print(split_list)


# split_list = np.array_split(choose_user, 15)
# [{'Додо': ['Абакан', 'Абинск']}, {'Ташир': ['Аксай', 'Астрахань']}, {'Томато': ['Белгород', 'Воронеж']}]

list_brand_and_cities = []

# for element in choose_user:
# print(part_table[0]['city'])
roster_brands = {}

# dodo = element['dodo']
# tashir = element['tashir']
# tomato = element['tomato']
# print(city)

#
# for number, row in enumerate(part_table):
#     temp = []
#     city = row['city']
#     print(number, city, split_list[number])
#     brands = split_list[number]
#     if brands[2] is True:
#         roster_brands['Додо'] = [city]
#
#
# print(roster_brands)


# for number, row in enumerate(split_list):
#     dodo, tashir, tomato = row
#
#     print(number, dodo, tashir, tomato)

# for num, row in enumerate(split_list):
#     dodo, tashir, tomato = row
#     for element in part_table:
#         print(element['city'])
#

# for element in part_table:
#     city = element['city']

# print(roster_brands)

#     for num_brand, brand in enumerate(split_list[num]):
#         print(num_brand, brand)

import numpy as np
