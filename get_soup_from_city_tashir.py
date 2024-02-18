import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

import os
import shutil
import time

from bs4 import BeautifulSoup
from parser_tashir import find_url_cities_tashir, get_data_from_locality_tashir

from word_correction import get_correct_city


def get_page_soup_from_url(city_url: str) -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    param city_url: str
    return: BeautifulSoup
    """

    chrome_options = Options()  # после получение разметки можно не использовать
    chrome_options.add_argument('--no-sandbox')  # после получение разметки можно не использовать
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome()

    # driver = webdriver.Chrome(options=chrome_options)  # после получение разметки можно не использовать
    URL = f"https://tashirpizza.ru{city_url}"  # после получение разметки можно не использовать

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
    path_tashir = 'Ташир пицца'

    with open(f"{path_tashir}/{name_city}.html", "w", encoding='utf-8') as file:  # делаем файл в html, чтобы дергать сайт лишний раз
        file.write(str(soup))


def create_file_html(city: str) -> str:
    """
    Функция создает html файлы для дальнейшей работы (что бы не дергать сайт)
    param list_cities: list
    """
    path_tashir = 'Ташир пицца'
    all_url_cities = find_url_cities_tashir()  # получение всех возможных городов для парсинга

    url_city = all_url_cities[city]
    soup_city = get_page_soup_from_url(url_city)
    write_file_from_soup(soup_city, city)
    file_name = f'{path_tashir}/{city}.html' # Переделать так как город уже есть

    return file_name


def parsing_tashir_pizza():
    """
    Функция загружает данные по Бренду, городам и продуктам в базу данных
    """
    brand = 'Ташир пицца'
    check_path(brand)  # проверяет существует ли папка "Додо пицца"
    os.mkdir(brand)  # Создается папка "Додо пицца"
    # load_table_brand(brand)

    all_correct_city = get_correct_city()
    brand_id = 2
    city_id = 1

    load_sections = False

    for city in all_correct_city:
        print(city)
        file_name = create_file_html(city)

        data_from_locality = get_data_from_locality_tashir(file_name)
        print(data_from_locality)
