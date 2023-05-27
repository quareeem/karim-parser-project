import json
import time
import requests
import logging
import concurrent.futures
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry



logging.basicConfig(
    filename='logs.txt',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

headers = {
    'User-Agent': 'My User Agent 1.0',
}

retry_strategy = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[ 500, 502, 503, 504 ]
)

adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retry_strategy)
session = requests.Session()
session.mount('http://', adapter)
session.mount('https://', adapter)
session.headers.update(headers)
session.timeout = 30



def retrieve_description_text(url):
    url = f'https://shop.kz/{url}'
    with session.get(url, headers=headers) as response:
        try:
            html = BeautifulSoup(response.content, 'html.parser')
            text = html.find('div', class_='item_info_section')
            text = text.find('div', class_='bx_item_description').text.replace('\n', '')
            text = text.replace('Описание', '').strip()
            text = text.replace('\r', '').replace('\t', '')
        except Exception as e:
            logging.error(f'Error while retrieving {url}: {e}')
            logging.error(f'{html.text}')
        return text


def parse_product(prod):
    dict_info = {}
    dict_info['name'] = prod.find(class_='bx_catalog_item_title_text').string.strip()
    # print(dict_info['name'])
    dict_info['articul'] = prod.find(class_='bx_catalog_item_XML_articul').string.replace('Артикул:', '').strip()
    try:
        dict_info['price'] = prod.find(class_='bx-more-price-text').string.strip()
    except AttributeError:
        dict_info['price'] = 'Нет в наличии'

    desc_href = prod.find('div', class_='bx_catalog_item_title').find('a')['href'][1:]
    dict_info['description'] = retrieve_description_text(desc_href)
    dict_info['photo_urls'] = prod.find('img')['data-src']
    return dict_info


def retrieve_page(url):
    with session.get(url, headers=headers) as response:
        html = BeautifulSoup(response.content, 'html.parser')
        products = html.find('div', class_='bx_catalog_list_home col1 bx_blue')
        prods_str = products.find_all('div', class_='bx_catalog_item')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # divide the list of products into chunks of size 10
            chunks = [prod for prod in prods_str]
            # process each chunk in parallel and flatten the results
            results = list(executor.map(parse_product, chunks))
        return results


def retrieve_products(url_list, cat_name):
    all_products = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(retrieve_page, url_list)
        for pgnum, products in enumerate(results):
            values = {f'{cat_name[1:-1]}: {pgnum + 1}-{idx + 1}': prod for idx, prod in enumerate(products)}
            all_products.update(values)
    return all_products


