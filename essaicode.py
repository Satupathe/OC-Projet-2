#requests.get et beautifulsoup pour extraire le texte de l'URL
from bs4 import BeautifulSoup
import requests
import urllib.parse


url = 'http://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html'


def request_site(url):
    response = requests.get(url)
    return response

return_book1 = request_site(url)
    
if return_book1.status_code == 200:
    soup = BeautifulSoup(return_book1.content, 'lxml')
    book_infos = dict()
    
    
    book_infos['titre'] = soup.find('h1').text
    print(book_infos['titre'])

    
    description = soup.find("p", recursive=False) or ""
    if description:
        description = description.text
        book_infos["product_description"] = 'description'
        print(description)


    book_infos['url de la page'] = url 
    print(book_infos['url de la page'])


    ths = soup.findAll('th')
    tds = soup.findAll('td')
    print('caracteristiques')
    [print(th.text) for th in ths]
    print('valeurs associees')
    [print(td.text) for td in tds]

    
    """def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True


    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)"""
   

     
    book_categories = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].get_text()
    book_infos['catégorie du livre'] = book_categories
    print('catégorie du livre: \n' + str(book_infos['catégorie du livre']) + '\n')

    book_infos['note du livre'] = soup.find('p', {'class': 'star-rating'}).get('class')
    print('note du livre: \n' + str(book_infos['note du livre']) + '\n')

    img_url = soup.find('img').get('src')
    complete_img_url = urllib.parse.urljoin(url, img_url)
    book_infos["url de l'image"] = complete_img_url
    print("Url de l'image: \n" + str(book_infos["url de l'image"]) + '\n')