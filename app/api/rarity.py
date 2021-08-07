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
from api.models import Collection
import traceback


def connect_drivers():
    time.sleep(30)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless")
    while len(store.DRIVERS) < 4:
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
    try:
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
    except Exception as e:
        traceback.print_exc()
        return None, None


def get_collections_list(driver: webdriver.Remote):
    driver.get(store.RARITY_BASE_URL)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dataTable"))
    )
    table = driver.find_element_by_class_name("dataTable")
    rows = table.find_elements_by_tag_name("tr")[1:]
    collections = list()
    for row in rows:
        col_name = row.text.split('\n')[1]
        col_url = row.find_element_by_tag_name('a').get_attribute('href')
        col_slug = col_url.split('/')[-1]
        collections.append(Collection(collection_name=col_name,
                                      collection_url=col_url, collection_slug=col_slug))
    return collections
