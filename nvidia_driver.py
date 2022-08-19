import re
from init_chromedriver import init_chromedriver
from download_driver import download_driver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def fetch_nvidia_driver(url, system):
    gpu_arr = system["gpu_info_arr"]
    # gpu_arr = []
    # gpu_arr = ["NVIDIA", "Quadro", "K620"]
    # gpu_arr = ["NVIDIA", "Quadro", "P4000"]
    # gpu_arr = ["NVIDIA", "T1000"]
    gpu_arr_len = len(gpu_arr)
    gpu = " ".join(gpu_arr)
    os = system["os"]
    is_quadro = False
    index = 0
    driver = init_chromedriver()  # initialize web chrome driver

    # initialize nvidia options
    if gpu_arr_len >= 3:
        index = 1
    product_type = gpu_arr[index]  # eg. GeForce | Quadro
    product_series = get_product_series(
        gpu, gpu_arr
    )  # eg. Quadro Series | GeForce RTX 20 Series
    product = "{}".format(" ".join(gpu_arr[index:gpu_arr_len]))  # gpu name
    os = os if "11" not in os else "Windows 11"
    # os = "Windows 10 64-bit"
    if "Quadro" == product_type or "NVIDIA" == product_type:
        is_quadro = True
    print_gpu_info(product_type, product_series, product, os)
    print("is_quadro: ", is_quadro)
    try:
        driver.get(url)
        if not "Official" in driver.title:
            raise Exception("could not load page")

        print(f"\nPopulating options...")
        # product series type
        sel_product_series_type = Select(
            driver.find_element(By.ID, "selProductSeriesType")
        )
        # Get options from the element that matches the ID and parse through items until item match variable
        sel_product_series_type_options = sel_product_series_type.options
        for option in sel_product_series_type_options:
            if product_type in option.text:
                sel_product_series_type.select_by_visible_text(option.text)
                print(f"sel_product_type:", option.text)

        # product series
        sel_product_series = Select(
            driver.find_element(By.ID, "selProductSeries"))
        sel_product_series_options = sel_product_series.options
        for option in sel_product_series_options:
            if re.fullmatch(product_series, option.text):
                sel_product_series.select_by_visible_text(option.text)
                print("sel_product_series:", option.text)

        # product
        sel_product_family = Select(
            driver.find_element(By.ID, "selProductFamily"))
        sel_product_family_options = sel_product_family.options
        for option in sel_product_family_options:
            if re.fullmatch(product, option.text):
                sel_product_family.select_by_visible_text(option.text)
                print("sel_product_family:", option.text)

        # operating system
        sel_operating_system = Select(
            driver.find_element(By.ID, "selOperatingSystem")
        ).select_by_visible_text(os)
        print("sel_operating_system:", os)

        # navigate through pages
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
        get_nvidia_url_from_element(driver, is_quadro)
    except Exception as e:
        print("\n{}".format(e))


def parse_product_series(gpu_info_arr):
    """
    Grabs the first two digits from the series number
    """
    filtered = []
    for element in gpu_info_arr[1: len(gpu_info_arr)]:
        if element.isnumeric():
            series = element[0:2]
            filtered.append(series)
            break
        filtered.append(element)
    return filtered


def get_product_series(gpu, gpu_info_arr):
    if "GeForce" in gpu:
        return "{} Series".format(" ".join(parse_product_series(gpu_info_arr)))
    if "Quadro" in gpu:
        return "{} Series".format(gpu_info_arr[1])
    if "Quadro RTX" in gpu:
        return "{} Series".format(gpu_info_arr[1:3])
    if "T1000" in gpu:
        return "NVIDIA RTX Series"
    raise ValueError(f"Could not find a match for 'Product series'\n")


def get_nvidia_url_from_element(driver, is_quadro=False):
    if is_quadro:
        # Different html structure for specific product types ...
        xpath = "//*[@id='dnldBttns']/table/tbody/tr/td[1]/a"
    else:
        xpath = "//*[@id='mainContent']/table/tbody/tr/td/a"
    try:
        driver_url = driver.find_element(By.XPATH, xpath).get_attribute("href")

    except Exception as e:
        print("\n{}".format(e))
    else:
        driver.quit()
        download_driver(driver_url)


def print_gpu_info(product_type, product_series, product, operating_system):
    print(f"Parsed output")
    print("Product type: {}".format(product_type))
    print("Product series: {}".format(product_series))
    print("Product: {}".format(product))
    print("Operating system: {}".format(operating_system))


# fetch_nvidia_driver()
