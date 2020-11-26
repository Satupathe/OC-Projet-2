from bs4 import BeautifulSoup
import requests
import urllib.parse
import csv
import os
import io

url = 'https://books.toscrape.com/index.html'

return_ok = 200
base_of_url = url[:-10]


def request_site(url): # intérroger le site internet
	response = requests.get(url)
	response.encoding = 'utf-8'
	return response


def get_categories_and_urls(url): # obtenir les nom des différents catégories et les URLs associées
	soup = BeautifulSoup(request_site(url).content, 'lxml').find('ul', {'class': 'nav nav-list'}).findAll('li')[1:]
	urls_list = []
	category_name = []
	
	for item in soup:
		for links in item.findAll('a', href=True):
			urls_list.append(urllib.parse.urljoin(str(url), str(links['href'])))
	
	for item in soup:
		for name in item.select('a'):
			for specific in name:
				category_name.append(specific.strip())

	"""zip_iterator = zip(category_name, urls_list)
	category_name_and_urls = dict(zip_iterator)"""

	name_and_urls = []
	name_and_urls.append(category_name)
	name_and_urls.append(urls_list)
	return name_and_urls


def get_urls_1_category (base_url, url): # obtenir dans une liste les URLs pour une catégorie

	soup = BeautifulSoup(request_site(url).content, 'lxml')
	products_links = []
		
	if soup.find('li', {'class': 'next'}) == None: #si il n'y a qu'une seule page (donc pas de bouton next) on récupère les infos sur la page
		
		products_url = soup.findAll('h3')
		for item in products_url:
			for links in item.findAll('a', href=True):
				products_links.append(urllib.parse.urljoin(str(url), str(links['href'])))

	else: #s'il y a un bouton suivant il y a aussi une page 'page-1.html' identique à la page index.html
		i=1
		
		while BeautifulSoup(request_site(f'{base_url}page-{i}.html').content, 'lxml').find('div', {'class': 'page-header action'}) is not None:
			
			products_url = BeautifulSoup(request_site(f'{base_url}page-{i}.html').content, 'lxml').findAll('h3')

			for item in products_url:
				for links in item.findAll('a', href=True):
					products_links.append(urllib.parse.urljoin(str(url), str(links['href'])))
			
			i= i+1

	return products_links #retourner la liste des URLs obtenues


def caracteristic_list(target_return):# trouver le nom des caractéristiques pour un livre (en excluant celles non demandée dans le projet 2)
			
	th_list = []
	good_indices =[0, 2, 3, 5] 
	ths_find = target_return.find("table", {"class": 'table-striped'}).findAll('th')
	ths = []
	
	for i in good_indices:
		ths.append(ths_find[i])
		for th in ths:
			th_list.append(th.text)
	return th_list

		
def value_list(target_return): #trouver les valeurs associées aux caractéristiques d'un livre (en excluant celles non demandée dans le projet 2)

	td_list = []
	good_indices =[0, 2, 3, 5] 
	tds_find = target_return.find("table", {"class": 'table-striped'}).findAll('td')
	tds = []
	
	for i in good_indices:
		tds.append(tds_find[i])
		for td in tds:
			td_list.append(td.text)
	return td_list


def books_informations(link_list): # récupération des informations d'un livre

	list_of_books_information_dicts = [] # liste globale contenant le dictionnaire généré de chaque livre

	for link in link_list:

		url_return = BeautifulSoup(request_site(link).content, 'lxml')

		book_infos1 = {}
			

		book_infos1['Book Title'] = url_return.find('h1').get_text()

		book_infos1['Category'] = url_return.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].get_text()

		book_infos1['Book URL'] = link 


		description = url_return.find('article', 'product_page').find("p", recursive=False) or ""
		if description:
			description = description.text
			book_infos1["product description"] = description[:-7] 


		book_infos1['Rating'] = url_return.find('p', {'class': 'star-rating'}).get('class')

		book_infos2 = dict(zip(caracteristic_list(url_return), value_list(url_return)))
		

		img_url = url_return.find('img').get('src')
		complete_img_url = urllib.parse.urljoin(url, img_url)
		
		
		book_total_infos = {**book_infos1, **book_infos2}

		book_total_infos.update({"Picture URL": complete_img_url})

		list_of_books_information_dicts.append(book_total_infos)		

	return list_of_books_information_dicts # retour de la liste des dictionnaires



def csv_transfer(dictionary_list, category_name): # transfert des informations issues de la liste globale des dictionnaires dans un fichier.csv

	first_dictionary = dictionary_list[0]
	columns_header = []
	for k in first_dictionary:
		columns_header.append(k)

	data_dict = []
	for d in dictionary_list:
		data_dict.append(d.values()) 

	
	with open(category_name + ' category.csv' , 'w', encoding="utf-8") as essai:
		writer = csv.writer(essai)
		dict_writer = csv.DictWriter(essai, fieldnames=columns_header)
		dict_writer.writeheader()

		for i in data_dict:
			writer.writerow(i)

	essai.close()


def take_all_informations_of_all_books(url):
	#pour chaque url dans urls_list appliquer au reste du code
	category_name = get_categories_and_urls(url)[0]
	urls_list = get_categories_and_urls(url)[1]


	i = 0
	for category_url in urls_list:
		url_base = category_url[:-10]
		book_link_list = get_urls_1_category(url_base, category_url)
		list_of_books_information_dicts = books_informations(book_link_list)
		csv_transfer(list_of_books_information_dicts, category_name[i])

		i += 1


take_all_informations_of_all_books(url)


