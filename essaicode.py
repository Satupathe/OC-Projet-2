#requests.get et beautifulsoup pour extraire le texte de l'URL
from bs4 import BeautifulSoup
import requests
import urllib.parse
import csv


url = 'http://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html'


def request_site(url):
    response = requests.get(url)
    return response

return_book1 = request_site(url)
    
if return_book1.status_code == 200:
    soup = BeautifulSoup(return_book1.content, 'lxml')
    soup2 = BeautifulSoup(return_book1.content, 'lxml').find("article", "product_page")
    book_infos1 = dict()
    

    
    book_infos1['Book Title'] = soup.find('h1').get_text()
    
    book_infos1['Category'] = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].get_text()

    book_infos1['Book URL'] = url 
    

    description = soup2.find("p", recursive=False) or ""
    if description:
        description = description.text
        book_infos1["product description"] = description
         

    book_infos1['Rating'] = soup.find('p', {'class': 'star-rating'}).get('class')


    def caracteristic_return(target1):
        
        th_list = []
        ths = soup.find("table", {"class": 'table-striped'}).find_all(target1)
        for target1 in ths:
            th_list.append(target1.text)
        return th_list

    
    def value_return(target2):
    
        td_list = []
        tds = soup.find("table", {"class": 'table-striped'}).find_all(target2)
        for td in tds:
            td_list.append(td.text)
        return td_list


    book_infos2 = dict(zip(caracteristic_return('th'), value_return('td')))
     
    
    img_url = soup.find('img').get('src')
    complete_img_url = urllib.parse.urljoin(url, img_url)
    
    book_total_infos = {**book_infos1, **book_infos2}

    book_total_infos.update({"Picture URL": complete_img_url})

    
    print(book_total_infos)


    data_dict = book_total_infos.values()

    columns_header = book_total_infos.keys()
    

    with open('filetest.csv', 'w') as essai:
        writer = csv.writer(essai)
        dict_writer = csv.DictWriter(essai, fieldnames=columns_header)
        dict_writer.writeheader()

        writer.writerow(data_dict)

    essai.close()




    

    


