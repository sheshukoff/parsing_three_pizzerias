import time

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def update_url_cities_dodo() -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    :return: BeautifulSoup
    """

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    URL = "https://dodopizza.ru/voronezh"

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    input_box = driver.find_element(By.XPATH, "//span//a")
    input_box.click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def update_url_cities_tashir() -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    :return: BeautifulSoup
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    URL = "https://tashirpizza.ru/voronej"

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    input_box = driver.find_element(By.XPATH, "//a[@class='city']")
    input_box.click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def update_url_cities_tomato() -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    :return: BeautifulSoup
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    URL = "https://www.tomato-pizza.ru/cities"

    try:
        driver.get(URL)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {URL}")
        exit(1)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    return soup


def write_file_urls(soup: BeautifulSoup, name_brand: str):
    """
    Функция записывает в файл html разметку города в файл формата HTML
    :param soup: BeautifulSoup
    :param name_brand: str
    """
    with open(f"URLS_{name_brand}.html", "w", encoding='utf-8') as file:
        file.write(str(soup))
