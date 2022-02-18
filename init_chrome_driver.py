import os
from config import USER_AGENT
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# TODO test this on a client pc
CHROMEDRIVER_PATH = os.path.abspath("chromedriver\98.0.4758.102\chromedriver.exe")


def init_chromedriver():
    s = Service(CHROMEDRIVER_PATH)
    op = Options()
    op.add_argument("--headless")
    op.add_argument("--disable-dev-shm-usage")
    op.add_argument("user-agent={0}".format(USER_AGENT))
    op.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=s, options=op)
    print("\nchrome_driver_path: {}".format(CHROMEDRIVER_PATH))
    # driver.close()

    return driver


def get_chromedriver_version(driver):
    print("\nchromedriver version -> {}".format(driver.capabilities["browserVersion"]))
    return driver.capabilities["browserVersion"]


# test
get_chromedriver_version(init_chromedriver())
