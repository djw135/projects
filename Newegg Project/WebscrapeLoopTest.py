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
    A function to grab multiple pages of product data form the URLs
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
    """
    A function that grabs the brand name from the HTML
    :param container: The container holds specific product data from the HTML
    :return: List[], The List of tag elements corresponding from the HTML
    """
    brand_container = container.find_all("a", {"class": "item-brand"})
    # product_brand: List[] = brand_container[0].img["title"]
    if len(brand_container) == 0:
        return None
    return brand_container[0].img["title"]


def get_product_name(container) -> str:
    """
    A function that grabs the product name from the HTML
    :param container: The container holds specific product data from the HTML
    :return: List[], The List of tag elements corresponding from the HTML
    """
    title_container = container.findAll("a", {"class": "item-title"})
    # product_title: List[] = title_container[0].text
    return title_container[0].text


def get_shipping(container) -> str:
    """
    A function that grabs the product shipping cost from the HTML
    :param container: The container holds specific product data from the HTML
    :return: List[], The List of tag elements corresponding from the HTML
    """
    shipping_container = container.findAll("li", {"class": "price-ship"})
    # product_shipping: List[] = shipping_container[0].text.strip()
    return shipping_container[0].text.strip()


def get_product_price(container) -> str:
    """
    A function that grabs the product price from the HTML
    :param container: The container holds specific product data from the HTML
    :return: str, The str of numbers corresponding to the price in the HTML
    """
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
    :return: List[Tuple[Any]], List that contains the containers with product data
    """
    processed_data: List[Tuple[Any]] = []
    for item in page_data:
        ram_soup = soup(item, "html.parser")
        list_wrap = ram_soup.find("div", {"class": "list-wrap"})
        containers = list_wrap.findAll("div", {"class": "item-container"})
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
    :param stored_data: The data being iterated through and stored in the DB
    :param table_name: The DB table created for the product data
    :return: Void
    """
    for item in stored_data:
        cursor.execute('''INSERT INTO {} VALUES(?, ?, ?, ?)'''.format(table_name), item)


def run():
    """
    Main function to set table names, parse product data, store the parsed product data into the DB, and print when
    done
    :return: Void
    """
    table_names = ["ram", "cpu", "ssd", "gpu"]
    for table_name in table_names:
        create_table(table_name)
        page_data: List[str] = get_page_data(table_name=table_name)
        processed_data: List[Tuple] = process_page_data(page_data=page_data)
        insert_data(processed_data, table_name)
    print("Complete.")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    run()
