from distutils.log import error
import wmi
from os import system
from time import sleep
from urllib.request import urlopen, Request
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# config
DOWNLOADS_PATH = str(Path.home() / "Downloads")

options = Options()
options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)


def main():
    computer = wmi.WMI()
    os_info = computer.Win32_OperatingSystem()[0]
    architecture = os_info.OSArchitecture
    os_caption = os_info.Caption.split()
    os = "{} {} {}".format(os_caption[1], os_caption[2], architecture)
    gpu_info = computer.Win32_VideoController()[0].Name.split()
    gpu = {
        # "vendor": gpu_info[0],  # ex. Nvidia
        "vendor": "AMD",
        "product_type": gpu_info[1],  # ex. Geforce
        "product_series": "%s %s %s Series"
        % (gpu_info[1], gpu_info[2], gpu_info[3][0:2]),  # ex. Geforce RTX
        "product": "%s %s %s %s" % (gpu_info[1], gpu_info[2], gpu_info[3], gpu_info[4]),
    }
    # gpu_info : ['NVIDIA', 'GeForce', 'RTX', '2070', 'SUPER']
    print("'{}' detected".format(gpu["product"]))

    def vendor_url(vendor):
        NVIDIA_URL = "https://www.nvidia.com/Download/Find.aspx"
        AMD_URL = "https://www.amd.com/en/support"
        match vendor:
            case "NVIDIA":
                print("getting driver from {}".format(vendor))
                return fetch_nvidia_driver(NVIDIA_URL)
            case "AMD":
                print("getting driver from {}".format(vendor))
                return fetch_amd_driver(AMD_URL)

    def fetch_nvidia_driver(url):
        # TODO: Learn python error handling
        product_series_type = gpu["product_type"]
        product_series = gpu["product_series"]
        product_family = gpu["product"]
        operating_system = os

        # driver = webdriver.Chrome()
        driver.get(url)

        if not "Official" in driver.title:
            raise Exception("could not load page")

        if "quadro" in gpu.values():
            product_series_type = "NVIDIA RTX / Quadro"

        if "11" in os:
            operating_system = "Windows 11"

        try:
            print("fetching link...")
            # populate options
            sel_product_series_type = Select(
                driver.find_element(By.ID, "selProductSeriesType")
            ).select_by_visible_text(product_series_type)
            sel_product_series = Select(
                driver.find_element(By.ID, "selProductSeries")
            ).select_by_visible_text(product_series)
            sel_product_family = Select(
                driver.find_element(By.ID, "selProductFamily")
            ).select_by_visible_text(product_family)
            sel_operating_system = Select(
                driver.find_element(By.ID, "selOperatingSystem")
            ).select_by_visible_text(operating_system)
            # navigate through pages
            driver.find_element(
                By.XPATH, "//*[@id='Table1']/tbody/tr/td/table[2]/tbody/tr/td/a"
            ).click()
            driver.implicitly_wait(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[3]/form/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/b/a",
            ).click()
            driver.find_element(
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
            print("@!")

    def fetch_amd_driver(url):
        print(url)
        # TODO: Clean up code
        driver.get(url)
        driver.delete_all_cookies()
        name = "Radeon™ PRO WX 7100"
        if not "AMD" in driver.title:
            print(driver.title)
            raise Exception("could not load page")

        if "PRO" in name:
            option = "Professional Graphics"
            print(option)
        else:
            option = "Graphics"

        product_type = Select(
            driver.find_element(By.ID, "Producttype")
        ).select_by_visible_text(option)

        product_family = Select(
            driver.find_element(By.ID, "Productfamily")
        ).select_by_visible_text("AMD Radeon™ PRO")

        product_line = Select(
            driver.find_element(By.ID, "Productline")
        ).select_by_visible_text("Radeon™ PRO WX x100 Series")

        product_model = Select(
            driver.find_element(By.ID, "Productmodel")
        ).select_by_visible_text(name)

        driver.find_element(By.ID, "edit-submit").click()
        driver.implicitly_wait(5)
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]",
        )
        # driver.implicitly_wait(5)
        driverURL = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[2]/details[2]/div/div[1]/div/span/div/div[2]/div[4]/a",
        ).get_attribute("href")

        driver.quit()
        download_driver(driverURL)

    def download_driver(url):
        # clear = lambda: system("cls")
        # clear()
        print(f"got the driver\n:", url)
        req = Request(url)
        req.add_header("Referer", "https://www.amd.com/")
        with urlopen(req) as file:
            print("downloading to {} ...".format(DOWNLOADS_PATH))
            content = file.read()
        with open("{}\\output2.exe".format(DOWNLOADS_PATH), "wb") as download:
            download.write(content)
        print("done!")
        sleep(2)
        return

    # # chrome_options.add_argument("--headless")
    # # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-gpu")

    vendor_url(gpu["vendor"])


if __name__ == "__main__":
    main()
