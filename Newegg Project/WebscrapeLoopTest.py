import sqlite3
import requests
from typing import List, Tuple, Any, Optional
from time import sleep
from random import randint
from bs4 import BeautifulSoup as soup

# Creating a db
conn = sqlite3.connect('Newegg_Products.db')
cursor = conn.cursor()


# Creating a table function that creates tables for the searched items to be stored in


def create_table(table_name: str):
    """
    A function to create a DB table for storing parsed data
    :param table_name: str, The DB table created for the product data
    :return: Void
    """
    query = """
        CREATE TABLE {} (
        brand TEXT,
        product_name TEXT,
        shipping TEXT,
        price REAL
    )""".format(table_name)
    cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
    cursor.execute(query)


def get_page_data(table_name: str) -> List:
    """
    A function to grab multiple pages of product data form the URL
    :param table_name: str, The DB table created for product data
    :return: List[], the list of product data obtained from the URL
    """
    page_data: List = []
    for page in range(1, 2):
        url: str = 'https://www.newegg.com/p/pl?d={}&page={}'.format(table_name, page)
        page_text = requests.get(url).content
        page_data.append(page_text)
        sleep(randint(3, 10))
    return page_data


def get_brand_name(container) -> Optional[str]:
    brand_container = container.find_all("a", {"class": "item-brand"})
    if len(brand_container) == 0:
        return None
    return brand_container[0].img["title"]


def get_product_name(container) -> str:
    title_container = container.findAll("a", {"class": "item-title"})
    return title_container[0].text


def get_shipping(container) -> str:
    shipping_container = container.findAll("li", {"class": "price-ship"})
    return shipping_container[0].text.strip()


def get_product_price(container) -> str:
    try:
        price_container = container.findAll("li", {"class": "price-current"})
        price: str = price_container[0].strong.text + price_container[0].sup.text
        return price
    except AttributeError:
        return None


def process_page_data(page_data: List[str]) -> List[Tuple[Any]]:
    """
    A function to parse data and store the product data in corresponding containers
    :param page_data: List[str], a list of product data from the URL
    :return: List[Tuple[Any]],
    """
    processed_data: List[Tuple[Any]] = []
    for item in page_data:
        ram_soup = soup(item, "html.parser")
        containers = ram_soup.findAll("div", {"class": "item-container"})
        for container in containers:
            brand: Optional[str] = get_brand_name(container=container)
            product_name: str = get_product_name(container=container)
            shipping: str = get_shipping(container=container)
            product_price: Optional[str] = get_product_price(container=container)
            processed_data.append((brand, product_name, shipping, product_price))
    return processed_data


def insert_data(stored_data, table_name):
    """
    A function to take parsed product data and store into the DB
    :param stored_data:
    :param table_name: The DB table created for the product data
    :return: Void
    """
    for item in stored_data:
        cursor.execute('''INSERT INTO {} VALUES(?, ?, ?, ?)'''.format(table_name), item)


# Run function to call all the functions and print when done
def run():
    table_names = ["ram", "cpu", "ssd", "gpu"]
    for table_name in table_names:
        create_table(table_name)
        page_data: List[str] = get_page_data(table_name=table_name)
        processed_data: List[Tuple] = process_page_data(page_data=page_data)
        insert_data(processed_data, table_name)
    print("Complete.")

    conn.commit()
    conn.close()


# Main
if __name__ == '__main__':
    run()
