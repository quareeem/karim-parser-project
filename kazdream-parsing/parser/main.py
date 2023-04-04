from bs4 import BeautifulSoup as BS
import requests
import json
import os

from get_category import retrieve_category
from get_page_content import retrieve_description_text
from sender import send_rabbit

def retrieve_links():
    categories = []
    response = requests.get(baseurl, headers=headers)
    html = BS(response.content, 'html.parser')
    sidebar = html.find('ul', class_='bx-nav-list-1-lvl')
    sidebar_items = sidebar.find_all('li')

    to_clean = lambda x, s: x if x.a['href'].find(s) == -1 else None

    for elem in sidebar_items:
        if to_clean(elem, 'catalog') and to_clean(elem, 'javascript'):
            categories.append(elem.a['href'])
    categories = categories[2:]
    print('categories retrieved -- ok')
    return categories




if __name__ == "__main__":
    baseurl = 'https://shop.kz/'
    headers = requests.utils.default_headers()
    headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )

    cats = retrieve_links()

    for item in cats:
        retrieve_category(item)





