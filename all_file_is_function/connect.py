from selenium import webdriver
import time

URL = f"https://www.simplyrecipes.com/latest/"


def connect(url=URL):
    """
    create chrome driver
    :return: chrome driver:obj
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='../chromedriver')
    try:
        driver.get(url)
        time.sleep(5)
    except:
        print('new connection try')
        driver.get(url)
        time.sleep(5)

    return driver
