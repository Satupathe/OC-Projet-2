from bs4 import BeautifulSoup
import requests
import urllib.parse
import csv

url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

def request_site(url):
	response = requests.get(url)
	return response

return_category = request_site(url)
	
if return_category.status_code == 200:

	soup = BeautifulSoup(return_category.content, 'lxml')
	products_infos = soup.findAll('h3')
	products_links = []
	
	for item in products_infos:
		for links in item.findAll('a', href=True):


			products_links.append(urllib.parse.urljoin(str(url), str(links['href'])))

	

	find_page_link = soup.find('li', {'class': 'next'}).find('a').get('href')
	page_link = urllib.parse.urljoin(str(url), str(find_page_link))

	return_next_page = request_site(page_link)


if return_next_page.status_code == 200:

	for x in range(2,15):
		

		r = request_site(f'https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-{x}.html')

		if r.status_code == 200:	
			soup2 = BeautifulSoup(r.content, 'lxml')
			products_infos2 = soup2.findAll('h3')

			for item2 in products_infos2:
				for links2 in item2.findAll('a', href=True):
					products_links.append(urllib.parse.urljoin(str(url), str(links2['href'])))
		
		else:
			break
					


for page in products_links:
	if request_site(page).status_code == 200:
		soup3 = BeautifulSoup(request_site(page).content, 'lxml')
		soup4 = BeautifulSoup(request_site(page).content, 'lxml').find("article", "product_page")

		
		book_infos1 = {}
			

		book_infos1['Book Title'] = soup3.find('h1').get_text()

		book_infos1['Category'] = soup3.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].get_text()

		book_infos1['Book URL'] = page 


		description = soup4.find("p", recursive=False) or ""
		if description:
			description = description.text
			book_infos1["product description"] = description
			 

		book_infos1['Rating'] = soup3.find('p', {'class': 'star-rating'}).get('class')


		def caracteristic_return(target1):
			
			th_list = []
			ths = soup3.find("table", {"class": 'table-striped'}).find_all(target1)
			for target1 in ths:
				th_list.append(target1.text)
			return th_list

		
		def value_return(target2):
		
			td_list = []
			tds = soup3.find("table", {"class": 'table-striped'}).find_all(target2)
			for td in tds:
				td_list.append(td.text)
			return td_list


		book_infos2 = dict(zip(caracteristic_return('th'), value_return('td')))
		 
		
		img_url = soup.find('img').get('src')
		complete_img_url = urllib.parse.urljoin(url, img_url)
		
		book_total_infos = {**book_infos1, **book_infos2}

		book_total_infos.update({"Picture URL": complete_img_url})

		
		print(book_total_infos)