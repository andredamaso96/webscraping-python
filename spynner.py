from requests_html import HTMLSession
import pandas as pd
from selenium import webdriver
import time

url = 'https://motoxpert.pt/shop/category/pecas-escapes-21?category=21&search=&attrib=22-221'
producList = []

def render_page(url):
    print('Rendering Page.')
    s = HTMLSession()
    r = s.get(url)


    
    r.html.render(sleep=1) # sleep=1 is important - sleeps for x seconds after the render
    products = r.html.xpath('//*[@id="products_grid"]/a')
    #products = r.html.xpath('//*[@id="products_grid"]', first=True)
    return products



def parse(products):
    print('Getting beerwulf info..')
    for item in products:
        name  = item.find('h1', first=True).text


        # if item.search('Temporarily sold out'):
        #     stock = 'out of stock'
        # else:
        #     stock = 'in stock'

        product_info = {
            'Name': name
        }
        producList.append(product_info)

        print(f'Found {len(producList)} item(s)')


def output():
    df = pd.DataFrame(producList)
    print('Saved to .xls')
    df.to_excel('products.xls', index=False)


html = render_page(url)
parse(html)
output()

