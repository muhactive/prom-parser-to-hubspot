import requests
from bs4 import BeautifulSoup
from time import sleep
from requests_html import HTMLSession
import json
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0',
    'Accept': '*/*',
    'Accept-Language': 'uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://prom.ua/ua/Kuhonnye-plity',
    'content-type': 'application/json',
    'x-requested-with': 'XMLHttpRequest',
    'x-forwarded-proto': 'https',
    'x-language': 'uk',
    'x-apollo-operation-name': 'AnalyticsQuery',
    'Origin': 'https://prom.ua',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=4',
}

BASE_URL= "https://prom.ua"
#url = "https://prom.ua/ua/Kuhonnye-plity"

def find_href_list(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    list_href = []
    product_gallery = soup.find("div", {"data-qaid": "product_gallery"})
    list_link = product_gallery.find_all("a", {"data-qaid": "product_link"})
    
    for link in list_link:
        href = BASE_URL + link["href"]
        #print(href, "\n")
        list_href.append(href)
    return list_href
    

find_href_list("https://prom.ua/ua/Kuhonnye-plity")

def find_product_info(url):     
# url = https://prom.ua/p1927166823-plita-kombinirovannaya-grifon.html
    r = requests