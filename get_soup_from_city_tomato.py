import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os
import shutil
import time

from bs4 import BeautifulSoup
from working_with_the_user import find_url_cities_tomato
from parser_tomato import get_data_from_locality_tomato
from load_in_postgresql import load_database_description_product_card, load_table_brand, \
    load_table_city, get_brand_id, get_city_id, update_date_product


def get_page_soup_from_url(city_url: str) -> dict[str, BeautifulSoup]:
    """
    Функция возращает html разметку города.
    :param city_url: str
    :return: dict[str, BeautifulSoup]
    """

    section_tomato = ["pizza", "action", "snacks", "dessertdrink", "drinks"]

    chrome_options = Options()  # после получение разметки можно не использовать
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    roster_soups = {}

    for section in section_tomato:
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        URL = f"https://www.tomato-pizza.ru/menu/{city_url}/{section}"

        try:
            driver.get(URL)
        except selenium.common.exceptions.WebDriverException as error:
            print(f"адрес сайта не доступен или есть ошибка {URL}")
            exit(1)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        roster_soups[section] = soup

    return roster_soups


def check_path(path: str):
    """
    Функция проверяет существует ли папка
    :param path: str
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def write_file_from_soup(roster_soups: dict, name_city: str, path_brand: str) -> list:
    """
    Функция записывает в файл html разметку города в файл формата HTML
    :param roster_soups: dict
    :param name_city: str
    :param path_brand: str
    :return: list
    """

    file_sections = []
    os.makedirs(os.path.join(path_brand, name_city))
    time.sleep(3)

    for section, soup in roster_soups.items():
        time.sleep(3)
        with open(f"{path_brand}/{name_city}/{section}.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
            file_sections.append(f"{path_brand}/{name_city}/{section}.html")

    return file_sections


def create_file_html(path_brand: str, city: str) -> list:
    """
    Функция создает html файлы для дальнейшей работы (что бы не дергать сайт)
    :param path_brand: str
    :param city: str
    :return: list
    """

    all_url_cities = find_url_cities_tomato()

    url_city = all_url_cities[city]
    soup_city = get_page_soup_from_url(url_city)
    file_sections = write_file_from_soup(soup_city, city, path_brand)
    return file_sections


def parsing_tomato_pizza(brand: str, city: str):
    """
    Функция загружает данные по Бренду, городам и продуктам в базу данных
    :param brand: str
    :param city: list
    """

    check_path(brand)
    os.mkdir(brand)

    brand_id = get_brand_id(brand)
    if not brand_id:
        load_table_brand(brand)
        brand_id = get_brand_id(brand)

    city_id = get_city_id(city)
    if not city_id:
        load_table_city(city)
        city_id = get_city_id(city)
    else:
        update_date_product(brand_id, city_id)

    file_sections = create_file_html(brand, city)
    for file_section in file_sections:
        data_from_locality = get_data_from_locality_tomato(file_section)
        load_database_description_product_card(data_from_locality, brand_id, city_id)
