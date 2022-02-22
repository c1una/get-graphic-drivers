import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = os.path.normpath("chromedriver\98.0.4758.102\chromedriver.exe")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"


def init_chromedriver():
    s = Service(CHROMEDRIVER_PATH)
    op = Options()
    op.add_argument("--headless")
    # op.add_argument("--disable-dev-shm-usage")
    op.add_argument("user-agent={0}".format(USER_AGENT))
    op.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=s, options=op)
    # driver.close()

    return driver


def get_chromedriver_version(driver):
    print("\nchromedriver path -> {}".format(CHROMEDRIVER_PATH))
    print("chromedriver version -> {}".format(driver.capabilities["browserVersion"]))
    return driver.capabilities["browserVersion"]


# test
get_chromedriver_version(init_chromedriver())
