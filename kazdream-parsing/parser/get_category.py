from bs4 import BeautifulSoup as BS
import requests
import json
from pika import connection

from get_page_content import retrieve_page
from sender import send_rabbit

headers = requests.utils.default_headers()
headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )




def page_range(url):
    response = requests.get(url, headers=headers)
    html = BS(response.content, 'html.parser')
    page = html.find(class_='bx-pagination-container row')
    if page is None:
        return 1
    pages_lst = page.text.strip().replace('\n', ',').split(',')
    if '...' in pages_lst:
        pages_lst.remove('...')
    
    print('page range is parsed -- ok')
    return max(int(x) for x in pages_lst)





def retrieve_category(category):
    url = 'https://shop.kz' + str(category)

    data = {}
    cat = ''.join(c if c.isalpha() else '_' for c in category[1:-1])

    for item in range(1, page_range(url) + 1):
        name = cat+str(item)
        data[name] = retrieve_page(f'{url}?PAGEN_1={item}', item)
    

    print('content from a category has been retrieved -- ok')
    print(f' [-] Sending {cat}...')
    data_json = json.dumps(data, indent=4, ensure_ascii=False)
    send_rabbit(data_json)





