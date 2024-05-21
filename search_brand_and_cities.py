def split_array(choose_user_cities: list) -> list[list]:
    split_choose_user = []
    index = 0

    # Цикл, который берет по три элемента из списка
    while index < len(choose_user_cities):
        three_elements = choose_user_cities[index:index + 3]
        split_choose_user.append(three_elements)
        index += 3

    return split_choose_user
