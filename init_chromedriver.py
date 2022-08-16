import os
import sys
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# CHROMEDRIVER_PATH = os.path.normpath("chromedriver\98.0.4758.102\chromedriver.exe")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# CHROMEDRIVER_PATH = resource_path("chromedriver\98.0.4758.102\chromedriver.exe")


def init_chromedriver():
    try:
        # s = Service(CHROMEDRIVER_PATH)
        op = Options()
        op.add_argument("--headless")
        op.add_argument("user-agent={0}".format(USER_AGENT))
        # op.add_argument("--disable-dev-shm-usage")
        op.add_experimental_option("excludeSwitches", ["enable-logging"])
        # driver = webdriver.Chrome(service=s, options=op)
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=op)
        return driver
    except Exception as e:
        print(e)


# def get_chromedriver_version(driver):
#     try:
#         print("\nchromedriver path -> {}".format(CHROMEDRIVER_PATH))
#         print(
#             "chromedriver version -> {}".format(driver.capabilities["browserVersion"])
#         )
#     except Exception as e:
#         print(e)
#     return driver.capabilities["browserVersion"]


# test
# get_chromedriver_version(init_chromedriver())
