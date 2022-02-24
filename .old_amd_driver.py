from init_chromedriver import init_chromedriver
from download_driver import download_driver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def fetch_amd_driver(url, system_info):
    system = system_info()
    if system["vendor"] != "AMD":
        return
    # gpu_arr = ["AMD", "Radeon", "R5", "430"]
    gpu_arr = ["AMD", "Radeon", "PRO", "W5500"]
    # gpu_arr = system["gpu_info_arr"]
    os = system["os"]
    for i in range(len(gpu_arr)):
        # Add trademark
        if gpu_arr[i] == "Radeon":
            gpu_arr[i] = "Radeon™"

    product_type = "Graphics" if "PRO" not in gpu_arr[2] else "Professional Graphics"
    product_family = "AMD Radeon™ PRO" if "Radeon" and "PRO" in gpu_arr else gpu_arr[2]
    product_model = "{}".format(" ".join(gpu_arr[1 : len(gpu_arr)]))
    if product_type == "Professional Graphics":
        product_line = "{} Series".format(" ".join(parse_product_series(gpu_arr)))
    else:
        product_line = "{} Series".format(" ".join((gpu_arr[0:3])))

    print_gpu_info(product_type, product_family, product_line, product_model)
    driver = init_chromedriver()

    try:
        driver.get(url)
        if not "AMD" in driver.title:
            print(driver.title)
            raise Exception("could not load page")

        if product_type == "Graphics":
            # get autodetect software
            element_link = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div/div/div/article/div/div/div[2]/div/div/div/div[1]/div/div[2]/div/p[5]/a",
            )
            print(f"\nGetting Auto detect software...")
        else:

            # populate options
            sel_product_type = Select(
                driver.find_element(By.ID, "Producttype")
            ).select_by_visible_text(product_type)
            sel_product_family = Select(
                driver.find_element(By.ID, "Productfamily")
            ).select_by_visible_text(product_family)
            sel_product_line = Select(
                driver.find_element(By.ID, "Productline")
            ).select_by_visible_text(product_line)
            sel_product_model = Select(
                driver.find_element(By.ID, "Productmodel")
            ).select_by_visible_text(product_model)
            # navigate through site
            driver.find_element(By.ID, "edit-submit").click()
            driver.implicitly_wait(5)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]",
            )

            element_link = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]/div/div[1]/div/span/div/div[2]/div[4]/a",
            )
            # driver.implicitly_wait(5)
        get_amd_url_from_element(driver, element_link)

    except Exception as e:
        print(e)


def parse_product_series(gpu_info_arr):
    filtered = []
    for element in gpu_info_arr[1 : len(gpu_info_arr)]:
        if element[1].isnumeric():
            series = "{}{}000".format(element[0], element[1])
            filtered.append(series)
            break
        filtered.append(element)
    return filtered


def get_amd_url_from_element(driver, element_link):
    try:
        url = element_link.get_attribute("href")
    except Exception as e:
        print("\n{}".format(e))
    else:
        driver.quit()
        download_driver(url, is_amd=True)


def print_gpu_info(product_type, product_family, product_line, product_model):
    print(f"\nParsed output: ")
    print("Product type: {}".format(product_type))
    print("Product family: {}".format(product_family))
    print("Product line: {}".format(product_line))
    print("Product model: {}".format(product_model))
