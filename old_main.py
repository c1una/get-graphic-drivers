from itertools import product
import re
from os import system
from time import sleep
from pathlib import Path
from urllib.request import urlopen, Request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import wmi

# config
DOWNLOADS_PATH = str(Path.home() / "Downloads")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{} Safari/537.36"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent={0}".format(USER_AGENT))
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# TODO: separate functions into their own python files
def main():
    computer = wmi.WMI()
    os_info = computer.Win32_OperatingSystem()[0]
    architecture = os_info.OSArchitecture
    os_caption = os_info.Caption.split()
    os = "{} {} {}".format(os_caption[1], os_caption[2], architecture)
    gpu_info_arr = computer.Win32_VideoController()[0].Name.split()
    vendor = gpu_info_arr[0]

    def vendor_url(vendor):
        NVIDIA_URL = "https://www.nvidia.com/Download/Find.aspx"
        AMD_URL = "https://www.amd.com/en/support"
        match vendor:
            case "NVIDIA":
                print("getting driver from {}\n".format(vendor))
                return fetch_nvidia_driver(NVIDIA_URL)
            case "AMD":
                print("getting driver from {}".format(vendor))
                return fetch_amd_driver(AMD_URL)

    def fetch_nvidia_driver(url):
        def parse_product_series():
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

        product_type = gpu_info_arr[1]  # eg. GeForce
        product_series = "{} Series".format(" ".join(parse_product_series()))
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
            print("!")

    def fetch_amd_driver(url):
        gpu_arr = ["AMD", "Radeon", "R5", "430"]
        gpu = " ".join(gpu_arr[1 : len(gpu_arr)])
        # ["AMD", "Radeon", "Pro", "W5500"]
        product_type = (
            "Graphics" if "Pro" not in gpu_arr[1] else "Professional Graphics"
        )  # "Graphics | Professional Graphics"
        product_family = (
            "{} Series".format(gpu)
            if product_type == "Graphics"
            else gpu  # e.g AMD Radeon™ R5 Series | AMD Radeon™ PRO
        )
        product_line = "Radeon™ PRO WX x100 Series"  # AMD Radeon™ R5 400 Series
        product_model = name  # AMD Radeon™ R5 M430

        # TODO: refactor by adding loops
        try:
            driver.get(url)
            if not "AMD" in driver.title:
                print(driver.title)
                raise Exception("could not load page")

            if "PRO" not in name:
                product_type = "Graphics"
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
            # navgiate through site
            driver.find_element(By.ID, "edit-submit").click()
            driver.implicitly_wait(5)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]",
            )
            # driver.implicitly_wait(5)
            driver_url = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]/div/div[1]/div/span/div/div[2]/div[4]/a",
            ).get_attribute("href")

            driver.quit()
            download_driver(driver_url, is_amd=True)
        except:
            print(
                "Graphic card is not supported",
            )

    def download_driver(url, is_amd=False):
        # clear = lambda: system("cls")
        # clear()
        print(f"got the driver\n:", url)
        req = Request(url)
        if is_amd:
            req.add_header("Referer", "https://www.amd.com/")
        with urlopen(req) as file:
            print("downloading to {} ...".format(DOWNLOADS_PATH))
            content = file.read()
        with open("{}\\output2.exe".format(DOWNLOADS_PATH), "wb") as download:
            download.write(content)
        return print("done!")

    # # chrome_options.add_argument("--headless")
    # # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-gpu")

    vendor_url("NVIDIA")


if __name__ == "__main__":
    main()
