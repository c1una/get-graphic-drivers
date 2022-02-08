import wmi
from os import system
from time import sleep
from urllib.request import urlopen
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

""" Example:
# Nvidia url driver
https://us.download.nvidia.com/Windows/472.12/472.12-desktop-win10-win11-64bit-international-whql.exe
# AMD url driver
https://drivers.amd.com/drivers/non-whql-radeon-software-adrenalin-2020-22.2.1-win10-win11-64bit-feb3.exe
"""

NVIDIA_URL = "https://www.nvidia.com/Download/Find.aspx"
AMD_URL = "https://www.amd.com/en/support"
DOWNLOADS_PATH = str(Path.home() / "Downloads")


def main():
    # Get graphics card information from Windows
    computer = wmi.WMI()
    # get windows version and architecture
    os_info = computer.Win32_OperatingSystem()[0]
    architecture = os_info.OSArchitecture
    os_caption = os_info.Caption.split()
    os = "{} {} {}".format(os_caption[1], os_caption[2], architecture)
    # get graphics card name
    gpu_info = computer.Win32_VideoController()[0].Name.split()
    # print(os)
    gpu = {
        "vendor": gpu_info[0],
        "product_type": gpu_info[1],
        "product_series": "%s %s %s Series"
        % (gpu_info[1], gpu_info[2], gpu_info[3][0:2]),
        "product": "%s %s %s %s" % (gpu_info[1], gpu_info[2], gpu_info[3], gpu_info[4]),
    }
    # gpu_info : ['NVIDIA', 'GeForce', 'RTX', '2070', 'SUPER']
    print("'{}' detected".format(gpu["product"]))

    def vendorUrl(vendor):
        match vendor:
            case "NVIDIA":
                print("getting driver from {}".format(vendor))
                return fetchNvidiaDriver(NVIDIA_URL)
            case "AMD":
                print("getting driver from {}".format(vendor))
                return fetchAMDDriver(AMD_URL)

    def fetchNvidiaDriver(url):
        driver = webdriver.Chrome()
        driver.get(url)
        if not "Official" and not "AMD" in driver.title:
            raise Exception("could not load page")
        print("fetching link...")
        # TODO: find a better way to do this. Breaking the DRY rule here : select1, select2
        select1 = Select(driver.find_element(By.ID, "selProductSeriesType"))
        option1 = None
        isQuadro = False
        if "quadro" in gpu.values():
            option1 = "NVIDIA RTX / Quadro"
            isQuadro = True
        else:
            option1 = gpu["product_type"]

        # print(option1)
        select1.select_by_visible_text(option1)
        select2 = Select(driver.find_element(By.ID, "selProductSeries"))
        option2 = gpu["product_series"]
        select2.select_by_visible_text(option2)
        select3 = Select(driver.find_element(By.ID, "selProductFamily"))
        option3 = gpu["product"]
        select3.select_by_visible_text(option3)
        select4 = Select(driver.find_element(By.ID, "selOperatingSystem"))
        option4 = os

        if "11" in os:
            option4 = "Windows 11"
        select4.select_by_visible_text(option4)

        searchButton = driver.find_element(
            By.XPATH, "//*[@id='Table1']/tbody/tr/td/table[2]/tbody/tr/td/a"
        )

        searchButton.click()
        driver.implicitly_wait(1)
        driverLink = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[3]/form/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/b/a",
        )

        driverLink.click()
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[3]/table/tbody/tr/td/div/table[1]/tbody/tr[8]/td[1]/a",
        ).click()
        driver.implicitly_wait(1)
        driverURL = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/table/tbody/tr/td/div[3]/div[2]/table/tbody/tr/td/a",
        ).get_attribute("href")

        # print(driverURL)
        driver.quit()
        downloadDriver(driverURL)

    def fetchAMDDriver():
        # TODO:
        print()

    def downloadDriver(url):
        clear = lambda: system("cls")
        clear()
        print(f"got the driver\n: ", url)
        with urlopen(url) as file:
            print("downloading to downloads folder...")
            content = file.read()

        with open("{}\\output2.exe".format(DOWNLOADS_PATH), "wb") as download:
            download.write(content)

        print("done!")
        sleep(2)
        return

    # # Windows path
    # ser = Service("./chromedriver_win32/chromedriver.exe")
    # # chrome_options.add_argument("--headless")
    # # chrome_options.add_argument("--no-sandbox")
    # # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-gpu")

    url = vendorUrl(gpu["vendor"])


if __name__ == "__main__":
    main()
