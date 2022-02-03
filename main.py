import wmi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# TODO : read this https://chromedriver.chromium.org/home 
# read up on selenium 

    # Instantiate headless driver
chrome_options = Options()
# Windows path
chromedriver_location = 'C:\\path\\to\\chromedriver_win32\\chromedriver.exe'
# Mac path. May have to allow chromedriver developer in os system prefs
'/Users/path/to/chromedriver'
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_prefs = {"download.default_directory": r"C:\path\to\Downloads"} # (windows)
chrome_options.experimental_options["prefs"] = chrome_prefs
driver = webdriver.Chrome(chromedriver_location,options=chrome_options)
# Download your file
driver.get('https://www.mockaroo.com/')
driver.find_element_by_id('download').click()

# NVIDIA_URL = "https://www.nvidia.com/Download/Find.aspx"
# computer = wmi.WMI()
# # computer_info = computer.Win32_ComputerSystem()[0]
# # os_info = computer.Win32_OperatingSystem()[0]
# # proc_info = computer.Win32_Processor()[0]
# gpu_info = computer.Win32_VideoController()[0]

# # os_name = os_info.Name.encode('utf-8').split(b'|')[0]
# # os_version = ' '.join([os_info.Version, os_info.BuildNumber])
# # system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB

# # print('OS Name: {0}'.format(os_name))
# # print('OS Version: {0}'.format(os_version))
# # print('CPU: {0}'.format(proc_info.Name))
# # print('RAM: {0} GB'.format(system_ram))
# # print('Graphics Card: {0}'.format(gpu_info.Name))
# print(gpu_info.Name)