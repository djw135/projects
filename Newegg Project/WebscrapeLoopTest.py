import sqlite3
from time import sleep
from random import randint
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

# Creating a db
conn = sqlite3.connect('product.db')
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

# Creating the webscrape funtion
def get_Data(table_name):
# Set start page, ending page, and page increments/steps
    pages = range(1, 4)

    # For loop to iterate through each page
    url = 'https://www.newegg.com/p/pl?d={}&page='.format(table_name)
    for page in pages:
        my_url = url + str(page)
        uClient = uReq(my_url)
        ram_html = uClient.read()
        uClient.close()
        ram_soup = soup(ram_html, "html.parser")
        containers = ram_soup.findAll("div", {"class": "item-container"})
        sleep(randint(3,10))

        # Making a list to store the items
        data_insert = []
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
            
            # Storing information in a list
            data_insert.append((brand, product_name, shipping, price))

    return data_insert

def insert_data(stored_data, table_name):
    for item in stored_data:
        cursor.execute('''INSERT INTO {} VALUES(?, ?, ?, ?)'''.format(table_name), item)

def run():
    table_names = ["ram", "cpu", "ssd", "gpu"]
    for table_name in table_names:
        create_Table(table_name)
        stored_data = get_Data(table_name)
        insert_data(stored_data, table_name)
    print("Complete.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    run()
    
