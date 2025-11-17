import requests
from bs4 import BeautifulSoup
from time import sleep


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
URL = "https://prom.ua/ua/Kuhonnye-plity"

def find_page():
    
    page = 1
    
    while True:
        url_page = f"{URL};{page}"
        
        r = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        
        yield url_page
        print(f"Parsing {page} page \n")
        
        pogination = soup.find("div", {"data-qaid": "pagination"})
        
        if pogination:
            button = pogination.find("a", {"data-qaid": "next_page"})

        else:
            button = None
            
        if button:
            page += 1
            
        else:
            break
       

def find_href_list():
    for link_url in find_page():
        r = requests.get(link_url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        product_gallery = soup.find("div", {"data-qaid": "product_gallery"})
        list_link = product_gallery.find_all("a", {"data-qaid": "product_link"})
            
        for link in list_link:
            href = BASE_URL + link["href"]
            yield href
    



def find_product_info(): 
    prod = 1
        
    for url in find_href_list():

        response = requests.get(url, headers=headers)
        bs = BeautifulSoup(response.text, "lxml")
    
        # Имя товара
        try:
            div_product_name = bs.find("div", {"data-qaid": "main_product_info"})
            name = div_product_name.find("h1", {"data-qaid": "product_name"}).text
        except:
            name = None
            
        # Code product
        try:
            id_product = bs.find("span", {"data-qaid": "product-sku"}).text.replace("Код: ", "")
        except:
            id_product = None
            
        #Nali4ie
        try:
            presense = bs.find("span", {"data-qaid": "product_presence"}).text
        except:
            presense = None
        
        #Price
        try:
            price_div = div_product_name.find("div", {"data-qaid": "product_price"})
            price = price_div.find("span").text.replace(" ", "")
        except:
            price = None
            
        # Link store
        try:
            store = bs.find("a", {"data-qaid": "company_name"})["href"]
            store_link = BASE_URL + store
        except:
            store_link = None
            
        # Link image product
        try:
            div_image_product = bs.find("div", {"data-qaid": "image_block"})
            image_product = div_image_product.find("img")["src"]
        except:
            image_product = None
                
        yield {"Название товара": name,
                "Код товара": id_product,
                "Наличие товара": presense,
                "Цена": price,
                "Линк на магазин": store_link,
                "Картинка товара": image_product}
        print(f"PArsing {prod} product \n")
        prod += 1
        sleep(1)
