
import os
from tqdm import tqdm
from scraping import Request_site, URLs_scraping, Book_information_scraping, CSV_saving, Pictures_scraping


URL = "https://books.toscrape.com/index.html"

return_ok = 200
base_of_url = URL[:-10] 


def main(url):
    """main function to scrap information from all books"""

    category_name = URLs_scraping.get_categories_and_urls(url)[0]
    urls_list = URLs_scraping.get_categories_and_urls(url)[1]

    i = 0
    for category_url in tqdm(urls_list):
        
        book_link_list = URLs_scraping.get_urls_1_category(category_url)
        list_of_books_information_dicts = Book_information_scraping.books_informations(URL, book_link_list)
        CSV_saving.csv_transfer(list_of_books_information_dicts, category_name[i])
        Pictures_scraping.pictures_scraping(list_of_books_information_dicts, category_name[i])
        i += 1

if __name__ == '__main__':
	main(URL)
	print ('Scraping finished')