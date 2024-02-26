import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import shutil
import time

from bs4 import BeautifulSoup
from working_with_the_user import find_url_cities_dodo
from parser_dodo import get_data_from_locality_dodo
from load_in_postgresql import load_database_description_product_card, load_table_brand, \
    load_table_city, get_brand_id, get_city_id


def get_page_soup_from_url(city_url: str) -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    :param city_url: str
    :return: BeautifulSoup
    """

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome()
    URL = f"https://dodopizza.ru{city_url}"

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()

    return soup


def check_path(path: str):
    """
    Функция проверяет существует ли папка
    :param path: str
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def write_file_from_soup(soup: BeautifulSoup, name_city: str, path_brand: str):
    """
    Функция записывает в файл html разметку города в файл формата HTML
    :param soup: BeautifulSoup
    :param name_city: str
    :param path_brand: str
    """

    with open(f"{path_brand}/{name_city}.html", "w", encoding="utf-8") as file:
        file.write(str(soup))


def create_file_html(path_brand: str, city: str) -> str:
    """
    Функция создает html файлы для дальнейшей работы (что бы не дергать сайт)
    :param path_brand: str
    :param city: str
    :return: str
    """

    all_url_cities = find_url_cities_dodo()  # получение всех возможных городов для парсинга

    url_city = all_url_cities[city]
    soup_city = get_page_soup_from_url(url_city)
    write_file_from_soup(soup_city, city, path_brand)
    file_name = f"{path_brand}/{city}.html"

    return file_name


def parsing_dodo_pizza(brand: str, dodo_cities: list):
    """
    Функция загружает данные по Бренду, городам и продуктам в базу данных
    :param brand: str
    :param dodo_cities: list
    """

    check_path(brand)  # проверяет существует ли папка "Додо пицца"
    os.mkdir(brand)  # Создается папка "Додо пицца"

    brand_id = get_brand_id(brand)
    if not brand_id:
        load_table_brand(brand)

    brand_id = get_brand_id(brand)

    for city in dodo_cities:
        city_id = get_city_id(city)
        if not city_id:
            load_table_city(city)

        city_id = get_city_id(city)

        file_name = create_file_html(brand, city)
        data_from_locality = get_data_from_locality_dodo(file_name)
        load_database_description_product_card(data_from_locality, brand_id, city_id)
