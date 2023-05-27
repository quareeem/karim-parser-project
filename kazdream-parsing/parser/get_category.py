import logging
import time
from bs4 import BeautifulSoup as BS
import requests
import json

from get_page_content import retrieve_page, retrieve_products
from custom_exceptions import ParsingError
from sender import send_rabbit



logging.basicConfig(
    filename='logs.txt',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

headers = {
    'User-Agent': 'My User Agent 1.0',
}



def page_range(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the status code is not 200
    except requests.exceptions.RequestException as e:
        raise ParsingError(f"Error: Failed to retrieve content from URL '{url}': {e}")

    try:
        html = BS(response.content, 'html.parser')
        page = html.find(class_='bx-pagination-container row')
        if page is None:
            return 1
        pages_lst = page.text.strip().replace('\n', ',').split(',')
        if '...' in pages_lst:
            pages_lst.remove('...')
        print('page range is parsed -- ok')
        return max(int(x) for x in pages_lst)
    except Exception as e:
        raise ParsingError(f"Error: Failed to parse content from URL '{url}': {e}")    



def retrieve_category(category):
    url = 'https://shop.kz' + requests.utils.quote(category)
    print(url)

    # cat = ''.join(c if c.isalpha() else '_' for c in category[1:-1])
    url_list = (f'{url}?PAGEN_1={item}' for item in range(1, page_range(url) + 1))

    data = retrieve_products(url_list, category)
    print('content from a category has been retrieved -- ok')
    print(f' [-] Sending ...')
    data_json = json.dumps(data, indent=4, ensure_ascii=False)
    send_rabbit(data_json)


# if __name__ == 'main':
#     start = time.time()
#     print('STARTING PARSING ...')
#     retrieve_category('/smart-chasy')
#     print('FINISHED')
#     print(f'elapsed time: {time.time() - start}')
