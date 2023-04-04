from bs4 import BeautifulSoup
import requests

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

session = requests.Session()


def retrieve_description_text(url):
    url = f'https://shop.kz/{url}'
    response = session.get(url, headers=headers)
    html = BeautifulSoup(response.content, 'html.parser')
    text = html.find('div', class_='item_info_section')
    text = text.find('div', class_='bx_item_description').text.replace('\n', '')
    text = text.replace('Описание', '').strip()
    return text


def parse_product(prod):
    dict_info = {}
    dict_info['name'] = prod.find(class_='bx_catalog_item_title_text').string.strip()
    dict_info['articul'] = prod.find(class_='bx_catalog_item_XML_articul').string.replace('Артикул:', '').strip()
    try:
        dict_info['price'] = prod.find(class_='bx-more-price-text').string.strip()
    except AttributeError:
        dict_info['price'] = 'Нет в наличии'
    
    desc_href = prod.find('div', class_='bx_catalog_item_title').find('a')['href'][1:]
    dict_info['description'] = retrieve_description_text(desc_href)
    dict_info['photo_urls'] = prod.find('img')['data-src']
    return dict_info


def retrieve_page(url, pagenum):
    response = session.get(url, headers=headers)
    html = BeautifulSoup(response.content, 'html.parser')
    products = html.find('div', class_='bx_catalog_list_home col1 bx_blue')
    prods_str = products.find_all('div', class_='bx_catalog_item')

    all_products = {}

    for idx, prod in enumerate(prods_str, start=1):
        all_products[f'{pagenum} - {idx}'] = parse_product(prod)
    
    print('page parsed - ok')
    return all_products
