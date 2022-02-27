from config import DOWNLOADS_PATH
from urllib.request import urlopen, Request
import os


def download_driver(url, is_amd=False):
    print("\nDriver found.\n{}".format(url))
    try:
        file_name_arr = list(url.split("/"))
        file_name = file_name_arr[-1]
        req = Request(url)
        if is_amd:
            req.add_header("Referer", "https://www.amd.com/")
        with urlopen(req) as file:
            print("\nDownloading to -> {} ...".format(DOWNLOADS_PATH))
            content = file.read()

        with open("{}\\{}".format(DOWNLOADS_PATH, file_name), "wb") as download:
            download.write(content)
        print(f"\nDone!")
    except Exception as e:
        print(e)

    else:
        input("(\u2713) Press enter to exit: ")
        os.startfile("{}\\{}".format(DOWNLOADS_PATH, file_name))
