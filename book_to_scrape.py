from bs4 import BeautifulSoup
import requests
import urllib.parse
import urllib.request
import csv
import os


URL = "https://books.toscrape.com/index.html"

return_ok = 200
base_of_url = URL[:-10]


def request_site(url):
    """request from the home page of the website"""

    response = requests.get(url)
    response.encoding = "utf-8"
    return response


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


def caracteristic_list(target_return):
    """scraping of researched caracteristics names 
    from the caractéristics list on the html page
    """

    th_list = []
    good_indices = [0, 2, 3, 5]
    ths_find = target_return.find("table", {"class": "table-striped"}).findAll("th")
    ths = []

    for i in good_indices:
        ths.append(ths_find[i])
        for th in ths:
            th_list.append(th.text)
    return th_list


def value_list(target_return):
    """scraping of researched values from the caractéristics list on the html page"""

    td_list = []
    good_indices = [0, 2, 3, 5]
    tds_find = target_return.find("table", {"class": "table-striped"}).findAll("td")
    tds = []

    for i in good_indices:
        tds.append(tds_find[i])
        for td in tds:
            td_list.append(td.text)
    return td_list


def books_informations(link_list):
    """informations scraping for each book"""

    list_of_books_information_dicts = []

    i = 1

    for link in link_list:

        url_return = BeautifulSoup(request_site(link).content, "lxml")

        book_infos1 = {}

        book_infos1["Book Title"] = url_return.find("h1").get_text()

        book_infos1["Category"] = (
            url_return.find("ul", {"class": "breadcrumb"}).findAll("a")[2].get_text()
        )

        book_infos1["Book URL"] = link

        description = (
            url_return.find("article", "product_page").find("p", recursive=False) or ""
        )
        if description:
            description = description.text
            book_infos1["product description"] = description[:-7]

        book_infos1["Rating"] = url_return.find("p", {"class": "star-rating"}).get(
            "class"
        )

        book_infos2 = dict(zip(caracteristic_list(url_return), value_list(url_return)))

        img_url = url_return.find("img").get("src")
        complete_img_url = urllib.parse.urljoin(URL, img_url)

        book_total_infos = {**book_infos1, **book_infos2}

        book_total_infos.update({"Picture URL": complete_img_url})

        img_name = url_return.find("img").get("alt")
        final_img_name = (
            str(book_total_infos["Category"])
            + " picture "
            + str({i})
            + " - "
            + str(img_name)
            .replace(":", "")
            .replace("\\", "")
            .replace("?", "")
            .replace("/", "")
            .replace('"', "")
            .replace(";", "")
            .replace("*", "")
        )
        book_total_infos.update({"Picture name": final_img_name})

        list_of_books_information_dicts.append(book_total_infos)

        i += 1

    return list_of_books_information_dicts


def csv_transfer(dictionary_list, category_name):
    """transfert of book informations to a csv file"""

    first_dictionary = dictionary_list[0]
    columns_header = []
    for k in first_dictionary:
        columns_header.append(k)

    data_dict = []
    for d in dictionary_list:
        data_dict.append(d.values())

    if not os.path.exists("category files"):
        os.makedirs("category files")

    os.chdir("category files")

    if not os.path.exists(category_name):
        os.makedirs(category_name)

    os.chdir(category_name)

    with open(
        category_name + " category.csv", "w", encoding="utf-8-sig", newline=""
    ) as essai:
        writer = csv.writer(essai)
        dict_writer = csv.DictWriter(essai, fieldnames=columns_header)
        dict_writer.writeheader()

        for i in data_dict:
            writer.writerow(i)

    essai.close()


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


def main(url):
    """main function to scrap information from all books"""

    category_name = get_categories_and_urls(url)[0]
    urls_list = get_categories_and_urls(url)[1]

    i = 0
    for category_url in urls_list:
        
        book_link_list = get_urls_1_category(category_url)
        list_of_books_information_dicts = books_informations(book_link_list)
        csv_transfer(list_of_books_information_dicts, category_name[i])
        pictures_scraping(list_of_books_information_dicts, category_name[i])

        i += 1


main(URL)
