import requests
import logging
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry



logging.basicConfig(filename='log.txt', level=logging.ERROR)
start = time.time()
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
# executor = concurrent.futures.ThreadPoolExecutor()



def retrieve_description_text(url):
    url = f'https://shop.kz/{url}'
    response = session.get(url, headers=headers)
    try:
        html = BeautifulSoup(response.content, 'html.parser')
        text = html.find('div', class_='item_info_section')
        text = text.find('div', class_='bx_item_description').text.replace('\n', '')
        text = text.replace('Описание', '').strip()
    except Exception as e:
        logging.error(f'Error retrieving description for URL: {url}. Error message: {e}')
        logging.error(f'{html.text}')
        return ''
    return text



def parse_product(prod):
    dict_info = {}
    dict_info['name'] = prod.find(class_='bx_catalog_item_title_text').string.strip()
    print(dict_info['name'])
    dict_info['articul'] = prod.find(class_='bx_catalog_item_XML_articul').string.replace('Артикул:', '').strip()
    try:
        dict_info['price'] = prod.find(class_='bx-more-price-text').string.strip()
    except AttributeError:
        dict_info['price'] = 'Нет в наличии'

    desc_href = prod.find('div', class_='bx_catalog_item_title').find('a')['href'][1:]
    dict_info['description'] = retrieve_description_text(desc_href)
    dict_info['photo_urls'] = prod.find('img')['data-src']
    return dict_info


# def r_etrieve_products(url_queue):
#     all_products = {}
#     futures = []
#     while not url_queue.empty():
#         url = url_queue.get()
#         future = executor.submit(retrieve_page, url)
#         futures.append(future)

#     for future in concurrent.futures.as_completed(futures):
#         page_url, products = future.result()
#         all_products[page_url] = products
#         print(f'page {page_url} parsed - ok')
#     return all_products


def retrieve_products(url_queue):
    all_products = {}
    futures = []
    with ThreadPoolExecutor() as executor:
        while not url_queue.empty():
            url = url_queue.get()
            future = executor.submit(retrieve_page, url)
            futures.append(future)

    for future in as_completed(futures):
        page_url, products = future.result()
        all_products[page_url] = products
    return all_products




def retrieve_page(url):
    try:
        response = session.get(url)
        response.raise_for_status()
        html = BeautifulSoup(response.content, 'html.parser')
        products = html.find('div', class_='bx_catalog_list_home col1 bx_blue')
        prods_str = products.find_all('div', class_='bx_catalog_item')
    except Exception as e:
        logging.error(f'Error retrieving page {url}. Error message: {e}')
        return url, []
    return url, [parse_product(prod) for prod in prods_str]



if __name__ == '__main__':
    url_queue = queue.Queue()
    for item in range(1, 10):
        url = f'https://shop.kz/smartfony/?PAGEN_1={item}'
        url_queue.put(url)
    if url_queue.empty():
        logging.warning('No URLs found in queue.')
    result = retrieve_products(url_queue)
    end = time.time()
    print(f'Time taken: {end - start:.2f} seconds.')

