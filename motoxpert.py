import requests
from requests_html import HTMLSession
from selenium import webdriver
import pandas as pd
import time
import os
import urllib
import urllib.request
import errno
from bs4 import BeautifulSoup

# testLink = 'https://motoxpert.pt/shop/category/pecas-escapes-21?category=21&search=&attrib=22-221'
# subcategory = "Escapes Pitbikes / Mini-ATV's (4T)"
baseUrl = 'https://motoxpert.pt'
url = 'https://motoxpert.pt/loja-online'


headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

productList = []
productLinks = []
referenceList = []
subCategoryList = []
categoryNameList = []


# def inputUser():
#     global testLink, subcategory

#     testLink = input("Insira o link da categoria: ")
#     subcategory = input("Insita o nome da categoria: ")

#buscar as categorias e os respetivos links
def render_categories(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')


    categoryList = soup.find_all('div', class_='pt32 pb32 col-lg-3')
    
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
                    # product = {
                    #     'Category' : name.text
                    # }
    
    return subCategoryLink

# buscar os produtos de cada categoria
def render_products(links):

    for url in links:

        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)

        html = driver.page_source

        soup = BeautifulSoup(html,'html.parser')

        trs = soup.find_all('tr', class_="sgeede-infinite-get")

        products = soup.find_all('td', class_="oe_product oe_grid te_t_image")

        s = HTMLSession()


        for item in products:
            for link in item.find_all('a', itemprop='url'):
                productLinks.append(baseUrl + link['href'])

                #for category in subCategoryList:
                categoryNameList.append(subCategoryList[links.index(url)])

            badges = item.find('div', attrs={'class': 'pull-left referencia_deff'})
            try:
                ref = badges.span.text
            except:
                ref = ''

            referenceList.append(ref)

            # categoryNameList.append(subCategoryList.get)

    # for c in categoryNameList:
    #     print(c)



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


        filename = 'img' + str(i)
        i = i+1
        
        #path = f'C:\\Users\\Noble Strategy\\Desktop\\André\\extracao-python\\{subcategory}\\'
        # path = "/"+subcategory+"/"
        # if not os.path.exists(path):
    	#     os.makedirs(path)
        # if not os.path.exists(os.path.dirname(subcategory)):
        #     try:
        #         os.makedirs(os.path.dirname(subcategory))
        #     except OSError as exc: # Guard against race condition
        #         if exc.errno != errno.EEXIST:
        #             raise
  

        # imagefile = open(path + '\\' + filename + ".jpeg", 'wb')
        # imagefile.write(urllib.request.urlopen(image).read())
        # imagefile.close()

        ref = referenceList[products.index(item)]
        subcategory = categoryNameList[products.index(item)]
        #print(ref)
        # filepath = path + '\\' + filename + ".jpeg"
        #priceFinal = float(price) * 1.23
      
        product_info = {
            'Referencia' : ref,
            'Nome' : name,
            'Categoria' : subcategory,
            'Preco' : price,
            'Imagem' : image
        }

        productList.append(product_info)




def output():
    df = pd.DataFrame(productList)
    print('Saved to .xls')
    #name = subcategory.split()[0] + ' ' + subcategory.split()[1]
    df.to_excel('motoxpert.xls', index=False)



if __name__ == '__main__':
    #inputUser()
    #render_products(testLink)
    render_products(render_categories(url))
    #for subcategory in subCategoryList:
    parse(productLinks)
    output()





