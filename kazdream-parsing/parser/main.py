from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as BS
import requests

from get_category import retrieve_category

baseurl = 'https://shop.kz/'
headers = {
    'User-Agent': 'My User Agent 1.0',
    }



def retrieve_links():
    categories = []
    with requests.Session() as session:
        response = session.get(baseurl, headers=headers)
        html = BS(response.content, 'html.parser')
        sidebar = html.find('ul', class_='bx-nav-list-1-lvl')
        sidebar_items = sidebar.find_all('li')
        to_clean = lambda x, s: x if x.a['href'].find(s) == -1 else None
        for elem in sidebar_items:
            if to_clean(elem, 'catalog') and to_clean(elem, 'javascript'):
                categories.append(elem.a['href'])
    categories = categories[2:]
    print('list of categories retrieved -- ok')
    return categories


if __name__ == "__main__":
    print('parsing has started ...')
    cats = retrieve_links()
    load = cats[1:5]
    print(load)
    for item in load:
        retrieve_category(item)





