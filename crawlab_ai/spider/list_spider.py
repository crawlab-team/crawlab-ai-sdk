from typing import Optional, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from concurrent.futures import ThreadPoolExecutor, as_completed
from crawlab_ai.utils.env import get_api_endpoint
from crawlab_ai.utils.logger import logger


class ListSpider(object):
    def __init__(self, url: str, fields: Optional[List[str] | List[dict]] = None):
        self.url = url
        self.fields = fields
        self.data = []
        self._fetch_rules()

    def _fetch_rules(self):
        res = requests.post(get_api_endpoint() + '/list_rules', json={
            'url': self.url,
            'fields': self.fields,
        })
        data = res.json()
        self._list_element_css_selector = data['model_list'][0]['list_model']['list_element_css_selector']
        self._fields = data['model_list'][0]['list_model']['fields']
        self._next_page_element_css_selector = data['model_list'][0]['next_page_element_css_selector']

    def crawl(self, url):
        futures = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures.append(executor.submit(self._fetch_data, url))

            for future in as_completed(futures):
                next_page_url = future.result()
                while next_page_url:
                    future = executor.submit(self._fetch_data, next_page_url)
                    next_page_url = future.result()

    def _fetch_data(self, url):
        logger.info('Crawling URL: ' + url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        list_items = soup.select(self._list_element_css_selector)
        for item in list_items:
            row = {}
            for field in self._fields:
                name = field['name']
                field_element = item.select_one(field['element_css_selector'])
                if not field_element:
                    continue
                if field['is_text']:
                    value = field_element.text.strip()
                else:
                    value = field_element.get(field['attribute'])
                row[name] = value
            self.data.append(row)
        logger.info('Fetched ' + str(len(list_items)) + ' items from URL: ' + url)

        if self._next_page_element_css_selector:
            next_page_element = soup.select_one(self._next_page_element_css_selector)
            if next_page_element:
                logger.info('Next page found: ' + next_page_element.get('href'))
                next_page_href = next_page_element.get('href')
                return urljoin(url, next_page_href)


def read_list(url: str, fields: Optional[List[str] | List[dict]] = None) -> DataFrame:
    spider = ListSpider(url, fields)
    spider.crawl(url)
    return DataFrame(spider.data)


if __name__ == '__main__':
    df = read_list('https://books.toscrape.com', ['product_name', 'product_price', 'product_link'])
    # df = read_list('https://quotes.toscrape.com')
    print(df)
