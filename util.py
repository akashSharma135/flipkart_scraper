import requests
from bs4 import BeautifulSoup


# find the total number of pages
def no_of_pages(product_type):

    """
        gets the number of pages for a particular product.
        params:
            product_type (str): takes the product name

        returns:
            pages (int): number of pages
    """

    URL = f'https://www.flipkart.com/search?q={product_type}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    container = soup.find('div', attrs={'class': '_36fx1h _6t1WkM _3HqJxg'})
    page_div = container.find('div', {'class': '_2MImiq'})

    # Total number of pages
    pages = int(page_div.span.text.split(" ")[-1].replace(',', ''))
    return pages



def get_data(product_type, pages):

    """
        gets all products from all the pages.
        params:
            product_type (str): takes the product name
            pages (int): number of pages

        returns:
            data (list): list of all data fetched
    """

    data = []

    for page in range(1, pages + 1):
        print(f'pages: {page}')
        URL = f'https://www.flipkart.com/search?q={product_type}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}'
        r = requests.get(URL)

        soup = BeautifulSoup(r.content, 'html5lib')

        container = soup.find('div', attrs={'class': '_36fx1h _6t1WkM _3HqJxg'})

        div = container.find_all('div', attrs={'class': '_1YokD2 _3Mn1Gg'})
        print(len(div))
        divs = div[1].find_all('div', attrs={'class': '_1AtVbE col-12-12'})
        # print()
        if len(divs) == 0:
            break

        for div in divs:
            a_tag = div.find('a', {'class': '_1fQZEK'})
            if a_tag != None:
                detail = {}

                # init detail_list to list all features
                detail_list = []


                try:
                    name = a_tag.find('div', {'class': '_4rR01T'})
                    price = a_tag.find('div', {'class': '_30jeq3 _1_WHN1'})
                    image = a_tag.find('div', {'class': 'CXW8mj'}).img['src']
                    rating = a_tag.find('div', {'class': '_3LWZlK'})
                    parent = a_tag.find("div", {'class': 'fMghEO'}).find('ul')

                    # listing all li elements
                    text = list(parent.descendants)
                    for i in range(2, len(text), 2):
                        detail_list.append(text[i].text)
                except AttributeError:
                    print(AttributeError)
                    pass

                # Product detail
                detail = {
                    'name': name.text,
                    'price': price.text if price else None,
                    'rating': rating.text if rating else None,
                    'features': detail_list,
                    'image': image,
                    'product_type': product_type
                }

                data.append(detail)

    return data

