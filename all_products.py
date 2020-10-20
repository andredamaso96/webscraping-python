import requests
from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import pandas as pd

baseUrl = 'https://motoxpert.pt'
url = 'https://motoxpert.pt/loja-online'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

product = {}
productList = []

def render_categories(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    #productList = soup.find_all('td', class_='oe_product oe_grid te_t_image')

    categoryList = soup.find_all('div', class_='pt32 pb32 col-lg-3')
    subCategoryList = []
    subCategoryLink = []

    for item in categoryList:

        for link in item.find_all('a', href=True):
            #subCategoryLink.append(baseUrl + link['href'])
            linkItem = link['href']
            if(not '#' in linkItem):
                subCategoryLink.append(baseUrl + link['href'])
                for name in link.find_all('div', class_='indexmenu'):
                    subCategoryList.append(name.text)
                    #print(name.text)
                    product = {
                        'Category' : name.text
                    }
    
    return subCategoryLink

def render_products(links):
    productLink = []

    for url in links:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(60)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)

        html = driver.page_source

        soup = BeautifulSoup(html,'html.parser')

        for link in soup.find_all('a', itemprop='url'):
            productLink.append(url + link['href'])


    
    print(len(productLink))

        #trs = soup.find_all('tr', class_="sgeede-infinite-get")

        #products = soup.find_all('td', class_="oe_product oe_grid te_t_image")




def output():
    df = pd.DataFrame(productList)
    print('Saved to .xls')
    df.to_excel('motoxpert.xls', index=False)

if __name__ == '__main__':
    render_products(render_categories(url))
