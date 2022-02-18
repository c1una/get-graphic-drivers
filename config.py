from pathlib import Path
from selenium import webdriver

driver = webdriver.Chrome()

# config
DOWNLOADS_PATH = str(Path.home() / "Downloads")
USER_AGENT = driver.execute_script("return navigator.userAgent;")
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{} Safari/537.36"
NVIDIA_URL = "https://www.nvidia.com/Download/Find.aspx"
AMD_URL = "https://www.amd.com/en/support"


driver.close()
