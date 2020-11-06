from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


# Creating the url to be scraped
my_url = 'https://www.newegg.com/Desktop-Memory/SubCategory/ID-147?Tid=7611'

# Grabbing the URL
uClient = uReq(my_url)

# Assign html client to variable
ram_html = uClient.read()

# Close the client
uClient.close()

# Parsing the html, and closing the client connection
ram_soup = soup(ram_html, "html.parser")

# Grabbing each product
containers = ram_soup.findAll("div",{"class":"item-container"})

# Creating the csv file
out_filename = "Newegg_RAM.csv"

# Creating the headers for the csv file
headers = "brand, product_name, shipping, price\n"

# Opening the file and write to it
f = open(out_filename, "w")
f.write(headers)

# Iterate over each product and grabe the information you want
for container in containers:

    # Create a container to scrape the brand from the html and assign it to a variable
    try:
        brand_container = container.find_all("a", {"class": "item-brand"})
        brand = brand_container[0].img["title"]
    except IndexError:
        continue

    # Create a container to scrape the product name from the html and assign it to a variable
    title_container = container.findAll("a",{"class":"item-title"})
    product_name = title_container[0].text

    # Create a container to scrape the shipping cost from the html and assign it to a variable
    shipping_container = container.findAll("li", {"class":"price-ship"})
    shipping = shipping_container[0].text.strip()

    # Create a container to scrape the price of the RAM from the html and assign it to a variable
    try:
        price_container = container.findAll("li", {"class":"price-current"})
        price = price_container[0].strong.text + price_container[0].sup.text
    except AttributeError:
        continue

    # Write the products to the csv file 
    f.write(product_name.replace(",", " ") + "," + brand.replace(",", "") + "," + shipping + "," + price.replace(",", "") + "\n")

# Close the file
f.close()


