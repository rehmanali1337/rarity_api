from api import store
from selenium import webdriver
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time


def connect_drivers():
    time.sleep(30)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless")
    while len(store.DRIVERS) < 2:
        try:
            print('Driver is connecting to hub')
            driver = webdriver.Remote(
                command_executor=store.HUB_URL,
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options)
            driver.set_window_size(1920, 1080)
        except exceptions.WebDriverException:
            print('Connections failed once!')
            time.sleep(5)
            driver = webdriver.Remote(
                command_executor=store.HUB_URL, desired_capabilities=DesiredCapabilities.CHROME)
            print('Driver connected!')
        driver.implicitly_wait(30)
        driver.get(store.RARITY_BASE_URL)
        print('Driver connected!')
        store.DRIVERS.append(driver)
        print(f'Total connected drivers : {len(store.DRIVERS)}')


def get_rank_and_score(driver: webdriver.Remote, collection_slug, asset_name):
    URL = f'{store.RARITY_BASE_URL}/{collection_slug}/view/{asset_name}'
    driver.get(URL)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.LINK_TEXT, "View on OpenSea"))
    )
    rank = driver.find_element_by_xpath(
        '//*[@id="__layout"]/div/div[3]/div[2]/div/div[1]/div/div[1]/div[1]/span').text
    score = driver.find_element_by_xpath(
        '//*[@id="__layout"]/div/div[3]/div[2]/div/div[2]/div/div[1]/div[2]').text
    return (rank, score)
