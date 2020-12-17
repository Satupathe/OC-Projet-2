from bs4 import BeautifulSoup
import urllib.parse
from scraping.request import request_site


def caracteristic_list(target_return):
    """scraping of researched caracteristics names
    from the caractéristics list on the html page
    """

    th_list = []
    good_indices = [0, 2, 3, 5]
    ths_find = (
        target_return.find("table", {"class": "table-striped"})
        .findAll("th")
    )

    ths = []

    for i in good_indices:
        ths.append(ths_find[i])
        for th in ths:
            th_list.append(th.text)
    return th_list


def value_list(target_return):
    """scraping of researched values from the caractéristics list
    on the html page
    """

    td_list = []
    good_indices = [0, 2, 3, 5]
    tds_find = (
        target_return.find("table", {"class": "table-striped"})
        .findAll("td")
    )

    tds = []

    for i in good_indices:
        tds.append(tds_find[i])
        for td in tds:
            td_list.append(td.text)
    return td_list


def books_informations(URL, link_list):
    """informations scraping for each book"""

    books_dicts = []

    i = 1

    for link in link_list:

        url_return = BeautifulSoup(request_site(link).content, "lxml")

        book_infos1 = {}

        book_infos1["Book Title"] = url_return.find("h1").get_text()

        book_infos1["Category"] = (
            url_return.find("ul", {"class": "breadcrumb"}).findAll("a")[2]
            .get_text()
        )

        book_infos1["Book URL"] = link

        description = (
            url_return.find("article", "product_page")
            .find("p", recursive=False) or ""
        )
        if description:
            description = description.text
            book_infos1["product description"] = description[:-7]

        book_infos1["Rating"] = (
            url_return.find("p", {"class": "star-rating"})
            .get("class")
        )

        book_infos2 = dict(zip(caracteristic_list(url_return),
                           value_list(url_return))
                           )

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

        books_dicts.append(book_total_infos)

        i += 1

    return books_dicts
