from email import header
from config import DOWNLOADS_PATH
import os
from urllib.request import urlopen, Request

# import requests
# from tqdm.auto import tqdm
# import shutil


def download_driver(url, is_amd=False):
    print("\nDriver found.\n{}".format(url))
    try:
        file_name_arr = list(url.split("/"))
        file_name = file_name_arr[-1]
        # print(file_name)
        req = Request(url)
        if is_amd:
            req.add_header("Referer", "https://www.amd.com/")
        # if is_amd:
        # headers = {"Referer": "https://www.amd.com/"}
        # with requests.get(url, headers=headers) as file:
        with urlopen(req) as file:
            # total_length = int(file.headers.get("Content-Length"))
            print("\nDownloading to -> {} ...".format(DOWNLOADS_PATH))
            content = file.read()
            # with tqdm.wrapattr(file.raw, "read", total=total_length, desc="") as raw:

        with open("{}\\{}".format(DOWNLOADS_PATH, file_name), "wb") as download:
            download.write(content)
            # shutil.copyfileobj(raw, download)
        print(f"\nDone!")
    except Exception as e:
        print(e)

    else:
        input("(\u2713) Press enter to exit: ")
        os.startfile("{}\\{}".format(DOWNLOADS_PATH, file_name))
