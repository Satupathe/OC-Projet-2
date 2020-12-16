from bs4 import BeautifulSoup
import requests
import urllib.parse
from scraping.Request_site import request_site


def get_categories_and_urls(url):
    """scraping names and urls of each book category"""

    soup = (
        BeautifulSoup(request_site(url).content, "lxml")
        .find("ul", {"class": "nav nav-list"})
        .findAll("li")[1:]
    )
    urls_list = []
    category_name = []

    for item in soup:
        for links in item.findAll("a", href=True):
            urls_list.append(urllib.parse.urljoin(str(url), str(links["href"])))

    for item in soup:
        for name in item.select("a"):
            for specific in name:
                category_name.append(specific.strip())

    name_and_urls = []
    name_and_urls.append(category_name)
    name_and_urls.append(urls_list)
    return name_and_urls


def get_urls_1_category(category_url):
    """ url scraping of each book from 1 category"""

    products_links = []
    base_of_url = category_url[:-10]

    response = BeautifulSoup(request_site(category_url).content, "lxml")
    is_next_page = response.find("li", {"class": "next"}) is not None

    products_url = response.findAll("h3")
    for item in products_url:
        for links in item.findAll("a", href=True):
            products_links.append(
                urllib.parse.urljoin(str(category_url), str(links["href"]))
            )

    if is_next_page:

        request_page_2 = BeautifulSoup(
            request_site(f"{base_of_url}page-2.html").content, "lxml"
        )

        products_url = request_page_2.findAll("h3")
        for item in products_url:
            for links in item.findAll("a", href=True):
                products_links.append(
                    urllib.parse.urljoin(str(category_url), str(links["href"]))
                )

        i = 2

        while (
            BeautifulSoup(
                request_site(f"{base_of_url}page-{i}.html").content, "lxml"
            ).find("li", {"class": "next"})
            is not None
        ):

            i += 1

            products_url = BeautifulSoup(
                request_site(f"{base_of_url}page-{i}.html").content, "lxml"
            ).findAll("h3")
            for item in products_url:
                for links in item.findAll("a", href=True):
                    products_links.append(
                        urllib.parse.urljoin(str(category_url), str(links["href"]))
                    )

    return products_links
