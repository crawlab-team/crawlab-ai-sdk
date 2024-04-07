from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from concurrent.futures import ThreadPoolExecutor, as_completed

from crawlab_ai.utils.auth import get_auth_headers
from crawlab_ai.utils.env import get_api_endpoint
from crawlab_ai.utils.logger import logger


class ListSpider(object):
    """
    The ListSpider class is responsible for crawling a given URL and extracting data based on specified fields.
    It fetches rules from an API endpoint, which are used to identify list elements and fields within the webpage.
    The class also supports pagination by identifying the next page element and recursively crawling until no more pages
     are found.

    Attributes:
        url (str): The URL to be crawled.
        fields (List[dict]): A list of fields to be extracted from each list element.
        data (List[dict]): A list to store the extracted data from each list element.
        get_html (function): A function to fetch the HTML content of a webpage. Defaults to the _get_html method.

    Methods:
        crawl(url: str): Starts the crawling process for the given URL.
    """

    def __init__(self, url: str, fields: List[dict] = None, get_html=None):
        self.url = url
        self.fields = fields
        self.data = []
        self.get_html = get_html or self._get_html
        self._fetch_rules()

    def _fetch_rules(self):
        logger.info('Fetching rules for URL: ' + self.url)
        res = requests.post(
            url=get_api_endpoint() + '/list_rules',
            headers=get_auth_headers(),
            json={
                'url': self.url,
                'fields': self.fields,
            },
        )
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

    @staticmethod
    def _get_html(url):
        res = requests.get(url)
        return res.text

    def _fetch_data(self, url):
        logger.info('Crawling URL: ' + url)
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
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


def _get_fields(fields: List[str] | dict = None) -> Optional[List[str] | List[dict]]:
    if isinstance(fields, list):
        return fields
    elif isinstance(fields, dict):
        return [{'name': k, 'description': v} for k, v in fields.items()]
    else:
        return None


def read_list(url: str, fields: List[str] | dict = None, get_html=None, as_dataframe=True) -> DataFrame | List[dict]:
    """
    Reads a list of items from a webpage and returns a DataFrame.

    Args:
        url (str): The URL to be crawled.
        fields (List[str] | dict): A list of fields to be extracted from each list element.
        get_html (function): A function to fetch the HTML content of a webpage. Defaults to the requests library.
        as_dataframe (bool): Whether to return the extracted data as a DataFrame. Defaults to True.

    Returns:
        DataFrame: A DataFrame containing the extracted data.

    """
    spider = ListSpider(url=url, fields=_get_fields(fields), get_html=get_html)
    spider.crawl(url)
    if as_dataframe:
        return DataFrame(spider.data)
    else:
        return spider.data


if __name__ == '__main__':
    df = read_list('https://quotes.toscrape.com')
    print(df)
    # df = read_list('https://36kr.com/', [
    #     'title',
    #     'author',
    #     'url',
    # ])
    # print(df)
