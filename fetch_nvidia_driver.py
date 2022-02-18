from distutils.log import error
from system_info import system_info
from init_chrome_driver import init_chromedriver
from config import DOWNLOADS_PATH, NVIDIA_URL
import re
from urllib.request import urlopen, Request
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def fetch_nvidia_driver(url=NVIDIA_URL):
    system = system_info()
    gpu_info_arr = system["gpu_info_arr"]
    os = system["os"]

    driver = init_chromedriver()
    # print(gpu_info_arr)

    product_type = gpu_info_arr[1]  # eg. GeForce
    product_series = "{} Series".format(" ".join(parse_product_series(gpu_info_arr)))
    product = "{}".format(" ".join(gpu_info_arr[1 : len(gpu_info_arr)]))
    operating_system = os if "11" not in os else "Windows 11"
    # operating_system = "Windows 10 64-bit"
    print("Product Type:", product_type)
    print("Product Series:", product_series)
    print("Product:", product)
    print("OS:", operating_system)
    try:
        driver.get(url)
        if not "Official" in driver.title:
            raise Exception("could not load page")
        # product series type
        sel_product_series_type = Select(
            driver.find_element(By.ID, "selProductSeriesType")
        )
        sel_product_series_type_options = sel_product_series_type.options
        for option in sel_product_series_type_options:
            if product_type in option.text:
                sel_product_series_type.select_by_visible_text(option.text)
                print(f"\nsel_product_type:", option.text)

        # product series
        sel_product_series = Select(driver.find_element(By.ID, "selProductSeries"))
        sel_product_series_options = sel_product_series.options
        for option in sel_product_series_options:
            if re.fullmatch(product_series, option.text):
                sel_product_series.select_by_visible_text(option.text)
                print("sel_product_series:", option.text)

        # product
        sel_product_family = Select(driver.find_element(By.ID, "selProductFamily"))
        sel_product_family_options = sel_product_family.options
        for option in sel_product_family_options:
            if re.fullmatch(product, option.text):
                sel_product_family.select_by_visible_text(option.text)
                print("sel_product_family:", option.text)

        # operating system
        sel_operating_system = Select(
            driver.find_element(By.ID, "selOperatingSystem")
        ).select_by_visible_text(operating_system)
        print("sel_operating_system:", sel_operating_system)

        # navigate through some pages
        search_button = driver.find_element(
            By.XPATH, "//*[@id='Table1']/tbody/tr/td/table[2]/tbody/tr/td/a"
        ).click()
        driver.implicitly_wait(1)
        driver_list = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[3]/form/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/b/a",
        ).click()
        first_download_button = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[3]/table/tbody/tr/td/div/table[1]/tbody/tr[8]/td[1]/a",
        ).click()
        driver.implicitly_wait(1)
        # get href link
        driver_url = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/table/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/a",
        ).get_attribute("href")

        driver.quit()
        download_driver(driver_url)

    except:
        print(error)


def parse_product_series(gpu_info_arr):
    """
    Grabs the first two digits from the series number
    """
    filtered = []
    for element in gpu_info_arr[1 : len(gpu_info_arr)]:
        if element.isnumeric():
            series = element[0:2]
            filtered.append(series)
            break
        filtered.append(element)
    return filtered


def download_driver(url, is_amd=False):
    # clear = lambda: system("cls")
    # clear()
    print("\ngot the driver".format(url))
    req = Request(url)
    if is_amd:
        req.add_header("Referer", "https://www.amd.com/")
    with urlopen(req) as file:
        print("\nDownloading to -> {} ...".format(DOWNLOADS_PATH))
        content = file.read()
    with open("\n{}\\output2.exe".format(DOWNLOADS_PATH), "wb") as download:
        download.write(content)
    return print("\ndone!")


fetch_nvidia_driver()
