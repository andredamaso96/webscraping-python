import requests
from requests_html import HTMLSession
from selenium import webdriver
import pandas as pd
import time
import os
import urllib
import urllib.request
from bs4 import BeautifulSoup

testLink = 'https://motoxpert.pt/shop/category/pecas-escapes-21?category=21&search=&attrib=22-221'
subcategory = "Escapes Pitbikes / Mini-ATV's (4T)"
baseUrl = 'https://motoxpert.pt'


headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

#product_info = {}

driver = webdriver.Chrome()
driver.get(testLink)
time.sleep(60)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html,'html.parser')

trs = soup.find_all('tr', class_="sgeede-infinite-get")

products = soup.find_all('td', class_="oe_product oe_grid te_t_image")

s = HTMLSession()

productList = []
productLinks = []
referenceList = []

for item in products:
    for link in item.find_all('a', itemprop='url'):
        
            #print(baseUrl + link['href'])
        productLinks.append(baseUrl + link['href'])

    badges = item.find('div', attrs={'class': 'pull-left referencia_deff'})
    ref = badges.span.text

    referenceList.append(ref)


    

def parse(products):

    print('Getting beerwulf info..')

    i = 1
    
    for item in products:

        r = requests.get(item, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')

        name = soup.find('h1', class_='te_product_name').text
         
        try:
            priceTag = soup.find('span', class_='price_ppr').text
            price = priceTag.split()[0]
        except:
            price = '0'

        img = soup.find('img', class_='product_detail_img')
        temp= img.get('src')
        image = baseUrl + temp

        # nametemp = img.get('alt')
        # if len(nametemp) == 0:
        #     filename=str(i)
        #     i = i+1

        # else:
        #     filename=nametemp 
        filename = 'img' + str(i)
        i = i+1
        
        path = r'C:\Users\Noble Strategy\Desktop\André\extracao-python\\' +  subcategory 
        

        imagefile = open(path + '\\' + filename + ".jpeg", 'wb')
        imagefile.write(urllib.request.urlopen(image).read())
        imagefile.close()

        ref = referenceList[products.index(item)]
        #print(ref)
        filepath = r'C:\Users\Noble Strategy\Desktop\André\extracao-python\\' +  subcategory + '\\' + filename + ".jpeg"
      
        product_info = {
            'Referencia' : ref,
            'Nome' : name,
            'Categoria' : subcategory,
            'Preco' : price,
            'Imagem' : filepath
        }



        productList.append(product_info)

        # try:
        #     priceTag = soup.find('span', class_='price_ppr').text
        #     typeProduct = priceTag.split()[0]
        # except:
        #     typeProduct = ''
        # for t in soup.find_all('option', attribute_name='Tipo de Veículo'):
        #     try:
        #         typeProduct = t['data-value_name']
        #     except:
        #         typeProduct = ''



def output():
    df = pd.DataFrame(productList)
    print('Saved to .xls')
    df.to_excel('escapes_teste.xls', index=False)

# def output():
#     df = pd.DataFrame(productList)
#     df.to_csv('escape1.csv', index=False)
#     print('Saved to CSV file.')


parse(productLinks)
output()


print(len(products))


