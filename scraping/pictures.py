"""Module to scrape picture from https://books.toscrape.com"""


import os
import urllib.request


def pictures_scraping(list_of_dicts, category_name):
    """scraping and naming of each book picture"""

    img_url_list = []
    img_name = []
    for d in list_of_dicts:
        img_url_list.append(d["Picture URL"])
        img_name.append(d["Picture name"])

    if not os.path.exists("Pictures"):
        os.makedirs("Pictures")

    os.chdir("Pictures")

    i = 0
    for url in img_url_list:

        urllib.request.urlretrieve(url, img_name[i] + ".jpg")

        i += 1

    os.chdir("../../..")
