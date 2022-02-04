import wmi
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Instantiate headless driver
chrome_options = Options()

# Windows path
ser = Service("C:/Users/Chris/Downloads/chromedriver_win32/chromedriver.exe")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# chrome_prefs = {"download.default_directory": r"C:/Users/Chris/Downloads"}  # (windows)
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "C:/Users/Chris/Downloads",
        "download.prompt_for_download": False,
    },
)


# chrome_options.experimental_options["prefs"] = chrome_prefs
driver = webdriver.Chrome(service=ser, options=chrome_options)
driver.command_executor._commands["send_command"] = (
    "POST",
    "/session/$sessionId/chromium/send_command",
)
params = {
    "cmd": "Page.setDownloadBehavior",
    "params": {"behavior": "allow", "downloadPath": "C:/Users/Chris/Downloads"},
}
command_result = driver.execute("send_command", params)
# Download your file
driver.get("https://www.mockaroo.com/")
driver.find_element(By.CLASS_NAME, "MuiButtonGroup-root")
driver.find_element(By.CSS_SELECTOR, "button").click()

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
