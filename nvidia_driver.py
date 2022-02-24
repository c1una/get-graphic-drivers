import re
import sys, os
from init_chromedriver import init_chromedriver
from download_driver import download_driver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def fetch_nvidia_driver(url, system_info):
    system = system_info()
    if system["vendor"] != "NVIDIA":
        return
    gpu_info_arr = system["gpu_info_arr"]
    os = system["os"]
    driver = init_chromedriver()

    # initialize nvidia options
    product_type = gpu_info_arr[1]  # eg. GeForce
    product_series = "{} Series".format(" ".join(parse_product_series(gpu_info_arr)))
    product = "{}".format(" ".join(gpu_info_arr[1 : len(gpu_info_arr)]))
    os = os if "11" not in os else "Windows 11"
    # operating_system = "Windows 10 64-bit"
    print_gpu_info(product_type, product_series, product, os)
    try:
        driver.get(url)
        if not "Official" in driver.title:
            raise Exception("could not load page")
        # product series type
        sel_product_series_type = Select(
            driver.find_element(By.ID, "selProductSeriesType")
        )
        print(f"\nPopulating options...")
        sel_product_series_type_options = sel_product_series_type.options
        for option in sel_product_series_type_options:
            if product_type in option.text:
                sel_product_series_type.select_by_visible_text(option.text)
                print(f"sel_product_type:", option.text)

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
        ).select_by_visible_text(os)
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
        get_nvidia_url_from_element(driver)
    except Exception as e:
        print("\n{}".format(e))


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


def get_nvidia_url_from_element(driver):
    try:
        driver_url = driver.find_element(
            By.XPATH,
            "//*[@id='mainContent']/table/tbody/tr/td/a",
        ).get_attribute("href")

    except Exception as e:
        print("\n{}".format(e))
    else:
        driver.quit()
        download_driver(driver_url)


def print_gpu_info(product_type, product_series, product, operating_system):
    print(f"Parsed output: ")
    print("Product type: {}".format(product_type))
    print("Product series: {}".format(product_series))
    print("Product: {}".format(product))
    print("Operating system: {}".format(operating_system))


# fetch_nvidia_driver()
