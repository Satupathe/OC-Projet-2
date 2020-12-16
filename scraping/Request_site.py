import requests

def request_site(url):
    """request from the home page of the website"""

    response = requests.get(url)
    response.encoding = "utf-8"
    return response