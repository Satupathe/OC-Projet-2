#requests.get et beautifulsoup pour extraire le texte de l'URL
from bs4 import BeautifulSoup
import requests

url = 'http://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html'

retour = requests.get (url)

if retour.ok:
	soup = BeautifulSoup(retour.content, 'lxml')
	titre = soup.find('title')
	print("titre du livre: " + str(titre.text) + '\n')
	
	print('url de la page: \n' + url + '\n')
	
	description = soup.findAll('p')
	print('Description du produit: \n' + str(description[3].text) + '\n')

	ths = soup.findAll('th')
	tds = soup.findAll('td')
	print('caracteristiques')
	[print(th.text) for th in ths]
	print('valeurs associees')
	[print(td.text) for td in tds]

	categorie = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')
	print('catégorie du livre: \n' + str(categorie) + '\n')

	note = soup.find('p', {'class': 'star-rating Three'})
	print('note du livre: \n' + str(note) + '\n')

	url_image = soup.find('img')
	print("Url de l'image: \n" + str(url_image) + '\n')
	
	

	
