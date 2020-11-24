from bs4 import BeautifulSoup
import requests
import urllib.parse
import csv

url = 'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html'
url2 = 'https://books.toscrape.com/index.html'

return_ok = 200
base_of_url = url[:-10]

def request_site(url): # intérroger le site internet
	response = requests.get(url)
	return response

def get_urls_categories(url): # obtenir les URLs des différentes catégories
	soup = BeautifulSoup(requests_site(url).content, 'lxml').find('ul', {'class': 'nav nav-list'}).findAll('li')[:1]
	category_urls_list = []
	for item in soup:
		for links in item.findAll('a', href=True):
			category_urls_list.append(urllib.parse.urljoin(str(url), str(links['href'])))

def get_urls_1_category (base_url, url): # obtenir dnas une liste les URLs pour une catégorie

	return_category = request_site(url)
	soup = BeautifulSoup(return_category.content, 'lxml')
	products_links = []
	i=0
	
	if soup.find('li', {'class': 'next'}) != 'none':
		i+=1
		response_page = request_site(f'{base_url}page-{i}.html')
		# BOUCLE INFINIE IL FAUT METTRE A JOUR LE SOUP A CHAQUE TOUR POUR NE PAS ETRE BLOQUE, VERIFIER LA CONDITION WHILE
		if response_page.status_code == return_ok:
			products_infos = BeautifulSoup(response_page.content, 'lxml').findAll('h3')

			for item in products_infos:
				for links in item.findAll('a', href=True):
					products_links.append(urllib.parse.urljoin(str(url), str(links['href'])))

		requests.get

	print(products_links)
	return products_links

"""get_urls_1_category(base_of_url, url)""" # appliquer la formule de recherche des liens d'un catégorie


def caracteristic_list(target_return):# trouver le nom des caractéristiques pour un livre
			
	th_list = []
	ths = target_return.find("table", {"class": 'table-striped'}).find_all('th')
	for target1 in ths:
		th_list.append(th.text)
	return th_list

		
def value_list(target_return): #trouver les valeurs associées aux caractéristiques d'un livre

	td_list = []
	tds = target_return.find("table", {"class": 'table-striped'}).find_all('td')
	for td in tds:
		td_list.append(td.text)
	return td_list


def books_informations(link_list): # récupérations des informations d'un livre

	picture_link_list = []

	for link in link_list:

		url_return = BeautifulSoup(requests.get(link).content, 'lxml').encode('utf-8')

		book_infos1 = {}
			

		book_infos1['Book Title'] = url_return.find('h1').get_text()

		book_infos1['Category'] = url_return.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].get_text()

		book_infos1['Book URL'] = link 


		description = url_return.find('article', 'product_page').find("p", recursive=False) or ""
		if description:
			description = description.text
			book_infos1["product description"] = description 


		book_infos1['Rating'] = url_return.find('p', {'class': 'star-rating'}).get('class')

		book_infos2 = dict(zip(caracteristic_list(url_return), value_list(url_return)))
		

		img_url = soup.find('img').get('src')
		complete_img_url = urllib.parse.urljoin(url, img_url)
		
		
		ook_total_infos = {**book_infos1, **book_infos2}

		book_total_infos.update({"Picture URL": complete_img_url})

	
	print(book_total_infos)
	return book_total_infos


def csv_transfer (dictionary): #fonction à terminer ou à réorganiser pour transférer les informations obtenues dans un fichier csv

	data_dict = dictionary.values()

    columns_header = dictionary.keys()
    

    with open('filetest.csv', 'w') as essai:
        writer = csv.writer(essai)
        dict_writer = csv.DictWriter(essai, fieldnames=columns_header)
        dict_writer.writeheader()

        writer.writerow(data_dict)

    essai.close()