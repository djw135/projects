from time import sleep
from random import randint
import numpy as np
import sqlite3
import pandas as pd
import schedule
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


# Creating a db
conn = sqlite3.connect('product.db')
cursor = conn.cursor()

# Deleteing table if one already exists
cursor.execute("DROP TABLE IF EXISTS PRODUCTS")

cursor.execute('''CREATE TABLE products(
    brand TEXT,
    product_name TEXT,
    shipping TEXT,
    price REAL
) ''')

# Creating the webscrape funtion
def getData():
# Set start page, ending page, and page increments/steps
    pages = np.arange(1, 101, 1)

    # For loop to iterate through each page
    for page in pages:
        my_url = 'https://www.newegg.com/p/pl?d=ram&page='+ str(page)
        uClient = uReq(my_url)
        ram_html = uClient.read()
        uClient.close()
        ram_soup = soup(ram_html, "html.parser")
        containers = ram_soup.findAll("div", {"class": "item-container"})
        sleep(randint(3,10))

        # Iterate over each product and grabe the information you want
        for container in containers:
            try:
                brand_container = container.find_all("a", {"class": "item-brand"})
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
            
            # Storing information in the db
            cursor.execute('''INSERT INTO products VALUES(?,?,?,?)''', (brand, product_name, shipping, price))

    return

# Calling the function
getData()

# Printing the results to test db table
conn.commit()
results = pd.read_sql_query("SELECT * FROM products", conn)
print(results)

conn.close()
