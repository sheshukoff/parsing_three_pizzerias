import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from webdriver_manager.chrome import ChromeDriverManager

import os
import shutil
import time

from bs4 import BeautifulSoup
from working_with_the_user import find_url_cities_tomato
from parser_tomato import get_data_from_locality_tomato


def get_page_soup_from_url(city_url: str) -> dict[str, BeautifulSoup]:
    """
    Функция возращает html разметку города.
    param city_url: str
    return: dict[str, BeautifulSoup]
    """

    section_tomato = ["pizza", "action", "snacks", "dessertdrink", "drinks"]

    chrome_options = Options()  # после получение разметки можно не использовать
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    roster_soups = {}

    for section in section_tomato:
        driver = webdriver.Chrome(options=chrome_options)
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
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def write_file_from_soup(roster_soups: dict, name_city: str) -> list:
    """
    Функция записывает в файл html разметку города в файл формата HTML
    param soup: BeautifulSoup
    name_city: str
    """
    path_tomato = "Томато"

    file_sections = []
    os.makedirs(os.path.join(path_tomato, name_city))
    time.sleep(3)

    for section, soup in roster_soups.items():
        time.sleep(3)
        with open(f"{path_tomato}/{name_city}/{section}.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
            file_sections.append(f"{path_tomato}/{name_city}/{section}.html")

    return file_sections


def parsing_tomato_pizza(tomato_cities):
    path_tomato = "Томато"

    all_url_cities = find_url_cities_tomato()
    # all_correct_city = get_correct_city()

    check_path(path_tomato)  # проверяет существует ли папка "Томато"
    os.mkdir(path_tomato)  # Создается папка "Томато"

    for city in tomato_cities:
        print(city)
        url_city = all_url_cities[city]
        soup_city = get_page_soup_from_url(url_city)
        file_sections = write_file_from_soup(soup_city, city)
        for file_section in file_sections:
            data_from_locality = get_data_from_locality_tomato(file_section)
            print(data_from_locality)
