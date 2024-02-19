import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from webdriver_manager.chrome import ChromeDriverManager

import os
import shutil
import time

from bs4 import BeautifulSoup
from parser_dodo import find_url_cities_dodo, get_data_from_locality_dodo

from word_correction import get_correct_city

# from load_in_postgresql import load_database_description_product_card, load_table_brand, \
#     load_table_city, load_table_section


def get_page_soup_from_url(city_url: str) -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    param city_url: str
    return: BeautifulSoup
    """

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    URL = f"https://dodopizza.ru{city_url}"

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def check_path(path: str):
    """
    Функция проверяет существует ли папка
    :param path: str
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def write_file_from_soup(soup: BeautifulSoup, name_city: str):
    """
    Функция записывает в файл html разметку города в файл формата HTML
    param soup: BeautifulSoup
    name_city: str
    """
    path_dodo = "Додо пицца"

    with open(f"{path_dodo}/{name_city}.html", "w", encoding="utf-8") as file:
        file.write(str(soup))


def create_file_html(city: str) -> str:
    """
    Функция создает html файлы для дальнейшей работы (что бы не дергать сайт)
    param list_cities: list
    """
    path_dodo = "Додо пицца"
    all_url_cities = (
        find_url_cities_dodo()
    )  # получение всех возможных городов для парсинга

    url_city = all_url_cities[city]
    soup_city = get_page_soup_from_url(url_city)
    write_file_from_soup(soup_city, city)
    file_name = f"{path_dodo}/{city}.html"  # Переделать так как город уже есть

    return file_name


def parsing_dodo_pizza():
    """
    Функция загружает данные по Бренду, городам и продуктам в базу данных
    """
    brand = "Додо пицца"
    check_path(brand)  # проверяет существует ли папка "Додо пицца"
    os.mkdir(brand)  # Создается папка "Додо пицца"
    # load_table_brand(brand)

    all_correct_city = get_correct_city()
    brand_id = 1
    city_id = 1

    load_sections = False

    for city in all_correct_city:
        print(city)
        file_name = create_file_html(city)

        # load_table_city(city)
        #
        data_from_locality = get_data_from_locality_dodo(file_name)
        print(data_from_locality)
        # sections = data_from_locality.keys()
        #
        # if not load_sections:
        #     for section in sections:
        #         try:
        #             load_table_section(section) # Load in table Section - name section (example - 'Пицца')
        #             load_sections = True
        #         except Exception as error:
        #             print('Загружать в таблицу (Section) можно только уникальные названия секций/разделов!!!')
        #
        # load_database_description_product_card(data_from_locality, brand_id, city_id)
        #
        # city_id += 1
