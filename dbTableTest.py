# Purpose of this script is to test things before pushing them onto the Looped version
import numpy as np
import sqlite3
import time
import pandas as pd
from time import sleep
from random import randint
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Creating a database and connection
conn = sqlite3.connect('tester.db')
cursor = conn.cursor()

def create_Table(table_name: str):
    
    info = '''CREATE TABLE {} (
        brand TEXT,
        product_name TEXT,
        shipping TEXT,
        price REAL
    )'''.format(table_name)
    cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
    cursor.execute(info)
    return info

def get_Data(url, table_name):

    # Setting up URL to be scrape data from
    my_url = url
    uClient = uReq(my_url)
    ram_html = uClient.read()
    uClient.close()
    ram_soup = soup(ram_html, "html.parser")
    containers = ram_soup.findAll("div", {"class": "item-container"})

    data_insert = []
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
            price_container = container.findAll(
                "li", {"class": "price-current"})
            price = price_container[0].strong.text + price_container[0].sup.text
        except AttributeError:
            continue

        # Storing information into a database
        data_insert.append((brand, product_name, shipping, price))

    return data_insert

def insert_data(stored_data, table_name):
    for item in stored_data:
        cursor.execute('''INSERT INTO {} VALUES(?, ?, ?, ?)'''.format(table_name), item)

def run():
    table_name = "RAM"
    create_Table(table_name)

    # Calling the function
    stored_data = get_Data('https://www.newegg.com/p/pl?d=ram+&page=33', table_name)
    insert_data(stored_data, table_name)
    print("Complete.")

    conn.commit()
    # results = pd.read_sql_query("SELECT * FROM products", conn)
    # print(results)

    conn.close()

if __name__ == '__main__':
    run()
    