import wmi
from time import sleep
from urllib.request import urlopen
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

    print(gpu["product_series"])

    def vendorUrl(vendor):
        match vendor:
            case "NVIDIA":
                return fetchNvidiaDriver(NVIDIA_URL)
            case "AMD":
                return fetchAMDDriver(AMD_URL)

    # def fetchDriverUrl(url):

    def fetchNvidiaDriver(url):
        driver = webdriver.Chrome()
        driver.get(url)
        if not "Official" and not "AMD" in driver.title:
            raise Exception("could not load page")
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

        # TODO: figure out how to programmaticly select the first link from the table. Theres prob a method to get an array of link
        searchButton.click()
        sleep(2)
        driver.quit()

    def fetchAMDDriver():
        print()
        # Instantiate headless driver

    # # Windows path
    # ser = Service("./chromedriver_win32/chromedriver.exe")
    # # chrome_options.add_argument("--headless")
    # # chrome_options.add_argument("--no-sandbox")
    # # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-gpu")

    # # chrome_prefs = {"download.default_directory": r"C:/Users/Chris/Downloads"}  # (windows)
    # chrome_options.add_experimental_option(
    #     "prefs",
    #     {
    #         "download.default_directory": "C:/Users/Chris/Downloads/new2",
    #         "download.prompt_for_download": False,
    #     },
    # )

    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # driver = webdriver.Chrome(service=ser, options=chrome_options)
    # Download your file
    # driver.implicitly_wait(4)
    # driver.get("http://www.mockaroo.com/")
    # driver.find_element(
    #     By.XPATH, "//*[@id='__next']/main/div[2]/form/div[3]/div[1]/button"
    # ).click()

    # print(gpu["vendor"])
    url = vendorUrl(gpu["vendor"])
    # url = vendorUrl("AMD")
    # fetchDriverUrl(url)


if __name__ == "__main__":
    main()

# with urlopen() as file:
#     content = file.read()

# with open("C:\\Users\\Chris\\Downloads\\output.exe", "wb") as download:
#     download.write(content)


# time.sleep(10)
# driver.close()
# driver.find_element(By.CLASS_NAME, "MuiButtonGroup-root")
# driver.find_element(By.CSS_SELECTOR, "button").click()

# # computer_info = computer.Win32_ComputerSystem()[0]
# # os_info = computer.Win32_OperatingSystem()[0]
# # proc_info = computer.Win32_Processor()[0]

# # os_name = os_info.Name.encode('utf-8').split(b'|')[0]
# # os_version = ' '.join([os_info.Version, os_info.BuildNumber])
# # system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB

# # print('OS Name: {0}'.format(os_name))
# # print('OS Version: {0}'.format(os_version))
# # print('CPU: {0}'.format(proc_info.Name))
# # print('RAM: {0} GB'.format(system_ram))
# # print('Graphics Card: {0}'.format(gpu_info.Name))
