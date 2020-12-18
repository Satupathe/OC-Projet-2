<<<<<<< HEAD
"""main function calling for every modules useful to extract
informations from https://books.toscrape.com
"""

=======
>>>>>>> 737bb1a9778918260ea22cc57438a23b779e7f15
from tqdm import tqdm
from scraping import urls, books, save, pictures


URL = "https://books.toscrape.com/index.html"


def main(url):
    """main function to scrap information from all books"""

    category_name = urls.get_categories(url)[0]
    urls_list = urls.get_categories(url)[1]

    i = 0
    

    for category_url in tqdm(urls_list, desc='loading categories', bar_format='{l_bar}'):

        book_links = urls.get_1_category(category_url)
        books_dicts = books.books_informations(URL, book_links)
        save.csv_transfer(books_dicts, category_name[i])
        pictures.pictures_scraping(books_dicts, category_name[i])
        i += 1


if __name__ == '__main__':
    main(URL)
    print('Scraping finished')
