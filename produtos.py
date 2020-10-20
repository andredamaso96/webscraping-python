import requests
from bs4 import BeautifulSoup
from collections import Counter
import time
from selenium import webdriver
import pandas as pd
import os

baseUrl = 'https://motoxpert.pt'

#url = 'https://motoxpert.pt/shop/category/pecas-sistema-de-travagem-63?category=63&search=&attrib=23-229&attrib='
shopUrl = 'https://motoxpert.pt/loja-online'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

#r = requests.get('https://motoxpert.pt/shop/category/pecas-sistema-de-travagem-63')
r = requests.get(shopUrl)
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


# print(len(subCategoryList))
# print(len(subCategoryLink))

testLink = 'https://motoxpert.pt/shop/category/pecas-escapes-21?category=21&search=&attrib=22-224'

# for link in subCategoryLink:
#     print(link)

# testLink = 'https://motoxpert.pt/shop/category/pecas-escapes-21?category=21&search=&attrib=22-221'

# #for testLink in subCategoryLink:


r = requests.get(testLink, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')

productList = soup.find_all('td', class_="oe_product oe_grid te_t_image")
productLink = []


# productBlock = soup.find_all('div', id="products_grid")

trs = soup.find_all('tr', class_="sgeede-infinite-get")

print(len(trs))


# for product in productBlock:
#     for link in product.find_all('a', itemprop='url'):
#         productLink.append(testLink + link['href'])


# for product in productList:
      
#     for link in product.find_all('a', itemprop='url'):
#         productLink.append(testLink + link['href'])
 


#print(len(productLink))

#/shop/product/yc110-140-01-bk-escape-completo-racing-ycf-bigy-pitbike-9620