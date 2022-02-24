from config import DOWNLOADS_PATH
from urllib.request import urlopen, Request


def download_driver(url, is_amd=False):
    print("\nDriver found.\n{}".format(url))
    req = Request(url)
    if is_amd:
        req.add_header("Referer", "https://www.amd.com/")
    with urlopen(req) as file:
        print("\nDownloading to -> {} ...".format(DOWNLOADS_PATH))
        content = file.read()
    with open("{}\\output2.exe".format(DOWNLOADS_PATH), "wb") as download:
        download.write(content)
    return print("\ndone!")
