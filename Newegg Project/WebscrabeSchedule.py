import numpy as np
import sqlite3
# import schedule
import time
import pandas as pd
from time import sleep
from random import randint
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


# Creating a database
conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

# Dropping duplicate table
cursor.execute("DROP TABLE IF EXISTS PRODUCTS")

# Creating database table
cursor.execute('''CREATE TABLE products(
    brand TEXT,
    product_name TEXT,
    shipping TEXT,
    price REAL
) ''')

# Creating a funtion to handle the webscraping
def getData(url):

    # Setting up URL to be scrape data from
    my_url = url
    uClient = uReq(my_url)
    ram_html = uClient.read()
    uClient.close()
    ram_soup = soup(ram_html, "html.parser")
    containers = ram_soup.findAll("div", {"class": "item-container"})

    # Iterating over the products on the page and scraping the information requested
    for container in containers:

        try:
            brand_container = container.findAll("a", {"class": "item-brand"})
            brand = brand_container[0].img["title"]
        except IndexError:
            continue

        title_container = container.findAll("a", {"class": "item-title"})
        product_name = title_container[0].text

        shipping_container = container.findAll("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip()

        try:
            price_container = container.findAll("li", {"class": "price-current"})
            price = price_container[0].strong.text + price_container[0].sup.text
        except AttributeError:
            continue
        
        # Storing information into a database
        cursor.execute('''INSERT INTO products VALUES(?,?,?,?)''',
                   (brand, product_name, shipping, price))
    
    return


# Calling the function
getData('https://www.newegg.com/p/pl?d=ram+&page=33')

conn.commit()
results = pd.read_sql_query("SELECT * FROM products", conn)
print(results)

# schedule.every().friday.at('14:20').do(getData)
# 
# while True:
#     schedule.run_pending()
#     time.sleep(1)
    
conn.close()
