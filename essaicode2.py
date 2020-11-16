"""description générale du module"""
import requests
from bs4 import BeautifulSoup

"""récupérer l'URL de la page ciblée et une réponse de celle-ci"""


"""chercher les données interessantes dans la réponse reçue et ajouter un parser"""
url = "http://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html"
response = requests.get(url)
print (response)
	

