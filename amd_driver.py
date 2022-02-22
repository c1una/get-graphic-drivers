import re
from system_info import system_info
from init_chromedriver import init_chromedriver
from config import DOWNLOADS_PATH, AMD_URL
from urllib.request import urlopen, Request
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def fetch_amd_driver(url=AMD_URL):
    driver = init_chromedriver()
    # system = system_info()
    # gpu_arr = ["AMD", "Radeon", "R5", "430"]
    # TODO Add trademark to Radeon
    gpu_arr = ["AMD", "Radeon", "Pro", "W5500"]
    # gpu1 = " ".join(gpu_arr[2 : len(gpu_arr)])
    # print(gpu1)
    product_type1 = (
        "Graphics" if "Pro" not in gpu_arr[2] else "Professional Graphics"
    )  # "Graphics | Professional Graphics"
    # product_family = (
    #     "{} Series".format(gpu)
    #     if product_type == "Graphics"
    #     else gpu  # e.g AMD Radeon™ R5 Series | AMD Radeon™ PRO
    # )
    product_type2 = "AMD Radeon™ PRO" if "Radeon" and "Pro" in gpu_arr else False
    # product_line = "Radeon™ PRO WX x100 Series"
    product_line = "{} Series".format(
        " ".join(parse_product_series(gpu_arr))
    )  # AMD Radeon™ R5 400 Series
    # product_model = name  # AMD Radeon™ R5 M430

    print(product_type1)
    print(product_line)
    print(product_type2)
    # TODO: if not pro graphics card download auto-detect software
    # try:
    #     driver.get(url)
    #     if not "AMD" in driver.title:
    #         print(driver.title)
    #         raise Exception("could not load page")

    #     if "PRO" not in name:
    #         product_type = "Graphics"
    #     # populate options
    #     sel_product_type = Select(
    #         driver.find_element(By.ID, "Producttype")
    #     ).select_by_visible_text(product_type)
    #     sel_product_family = Select(
    #         driver.find_element(By.ID, "Productfamily")
    #     ).select_by_visible_text(product_family)
    #     sel_product_line = Select(
    #         driver.find_element(By.ID, "Productline")
    #     ).select_by_visible_text(product_line)
    #     sel_product_model = Select(
    #         driver.find_element(By.ID, "Productmodel")
    #     ).select_by_visible_text(product_model)
    #     # navgiate through site
    #     driver.find_element(By.ID, "edit-submit").click()
    #     driver.implicitly_wait(5)
    #     driver.find_element(
    #         By.XPATH,
    #         "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]",
    #     )
    #     # driver.implicitly_wait(5)
    #     driver_url = driver.find_element(
    #         By.XPATH,
    #         "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]/div/div[1]/div/span/div/div[2]/div[4]/a",
    #     ).get_attribute("href")

    #     driver.quit()
    #     # download_driver(driver_url, is_amd=True)
    # except Exception as e:
    #     print(e)


def parse_product_series(gpu_info_arr):
    # TODO Implement regex and keep disecting gpu_arr to get the first two letters
    filtered = []
    # new_arr =
    # refgex (W5.)
    for element in gpu_info_arr[1 : len(gpu_info_arr)]:
        if element[0] == "W":
            # print(series)
            series = element[0:2] + "000"
            filtered.append(series)
            break
        filtered.append(element)
    return filtered


fetch_amd_driver()
