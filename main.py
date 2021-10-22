from db import client
from util import no_of_pages, get_data

# Database creation
db = client.product

# name the product to be queried
product_type = 'television'

total_pages = no_of_pages(product_type)

data = get_data(product_type, total_pages)

# name the collection in which data is to be stored
collection_name = 'electronic'

db[collection_name].insert_many(data)