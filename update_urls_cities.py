import time

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from test_get_soup_from_city_any_pizzerias import choose_brand, work_with_user_part_two

# from parser_dodo import find_url_cities_dodo, get_data_from_locality_dodo

# from word_correction import get_correct_city
# from load_in_postgresql import load_database_description_product_card, load_table_brand, \
#     load_table_city, load_table_section


def update_url_cities_dodo() -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    return: BeautifulSoup
    """

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    URL = 'https://dodopizza.ru/voronezh'

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    input_box = driver.find_element(By.XPATH, "//span//a")
    input_box.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def update_url_cities_tashir() -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    return: BeautifulSoup
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    URL = 'https://tashirpizza.ru/voronej'

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    input_box = driver.find_element(By.XPATH, "//a[@class='city']")
    input_box.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def update_url_cities_tomato() -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    return: BeautifulSoup
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    URL = 'https://www.tomato-pizza.ru/menu/voronezh/action'

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    input_box = driver.find_element(By.XPATH, "//span[@class='city-name']")
    input_box.click()
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return soup


def write_file_urls(soup: BeautifulSoup, name_brand: str):
    """
    Функция записывает в файл html разметку города в файл формата HTML
    param soup: BeautifulSoup
    name_city: str
    """
    with open(f"URLS_{name_brand}.html", "w", encoding='utf-8') as file:  # делаем файл в html, чтобы дергать сайт лишний раз
        file.write(str(soup))


def work_with_user_part_one():

    input_message = input("Нужно ли обновить города по пиццериям напишите Y/n: ")
    if input_message.lower() == 'y':
        list_brands = choose_brand()
        for brand in list_brands:
            if brand == 'Додо':
                soup_dodo = update_url_cities_dodo()
                write_file_urls(soup_dodo, brand)
                print(f'Города бренда "{brand}" обновлены:')
            elif brand == 'Ташир':
                soup_tashir = update_url_cities_tashir()
                write_file_urls(soup_tashir, brand)
                print(f'Города бренда "{brand}" обновлены:')
            elif brand == 'Томато':
                soup_tomato = update_url_cities_tomato()
                write_file_urls(soup_tomato, brand)
                print(f'Города бренда "{brand}" обновлены:')
    elif input_message.lower() == 'n':
        recieve_brand_and_cities = work_with_user_part_two()
        print(recieve_brand_and_cities)


work_with_user_part_one()
