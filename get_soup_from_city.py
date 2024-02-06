import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import shutil
import time

from bs4 import BeautifulSoup
from parser import find_url_cities, get_data_from_locality
from word_correction import get_correct_city
from load_in_postgresql import load_database_description_product_card, load_table_brand, \
    load_table_city, load_table_section


def get_page_soup_from_url(city_url: str) -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    param city_url: str
    return: BeautifulSoup
    """

    chrome_options = Options()  # после получение разметки можно не использовать
    chrome_options.add_argument('--no-sandbox')  # после получение разметки можно не использовать
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)  # после получение разметки можно не использовать
    URL = f"https://dodopizza.ru{city_url}"  # после получение разметки можно не использовать

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

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
    path_dodo = 'Додо пицца'

    with open(f"{path_dodo}/{name_city}.html", "w", encoding='utf-8') as file:  # делаем файл в html, чтобы дергать сайт лишний раз
        file.write(str(soup))


def create_file_html(city: str) -> str:
    """
    Функция создает html файлы для дальнейшей работы (что бы не дергать сайт)
    param list_cities: list
    """
    path_dodo = 'Додо пицца'
    all_url_cities = find_url_cities()  # получение всех возможных городов для парсинга

    url_city = all_url_cities[city]
    soup_city = get_page_soup_from_url(url_city)
    write_file_from_soup(soup_city, city)
    file_name = f'{path_dodo}/{city}.html' # Переделать так как город уже есть

    return file_name


def parsing_dodo_pizza():
    """
    Функция загружает данные по Бренду, городам и продуктам в базу данных
    """
    brand = 'Додо пицца'
    check_path(brand)  # проверяет существует ли папка "Додо пицца"
    os.mkdir(brand)  # Создается папка "Додо пицца"
    load_table_brand(brand)

    all_correct_city = get_correct_city()
    brand_id = 1
    city_id = 1

    load_sections = False

    for city in all_correct_city:
        print(city)
        file_name = create_file_html(city)

        load_table_city(city)

        data_from_locality = get_data_from_locality(file_name)
        sections = data_from_locality.keys()

        if not load_sections:
            for section in sections:
                try:
                    load_table_section(section) # Load in table Section - name section (example - 'Пицца')
                    load_sections = True
                except Exception as error:
                    print('Загружать в таблицу (Section) можно только уникальные названия секций/разделов!!!')

        load_database_description_product_card(data_from_locality, brand_id, city_id)

        city_id += 1
