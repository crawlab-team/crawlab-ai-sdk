from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from concurrent.futures import ThreadPoolExecutor, as_completed

from crawlab_ai.spider.base import BaseSpider
from crawlab_ai.utils.auth import get_auth_headers
from crawlab_ai.utils.env import get_api_endpoint
from crawlab_ai.utils.logger import logger


class ListSpider(BaseSpider):
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
        super().__init__(url, get_html)
        self.rules = None
        self.url = url
        self.fields = fields
        self.data = []

    @property
    def list_element_css_selector(self):
        return self.rules["list_model"]["list_element_css_selector"]

    @property
    def item_fields(self):
        return self.rules["list_model"]["fields"]

    @property
    def next_page_element_css_selector(self):
        return self.rules["next_page_element_css_selector"]

    def fetch_rules(self):
        logger.info("Fetching rules for URL: " + self.url)
        res = requests.post(
            url=get_api_endpoint() + "/rules/list",
            headers=get_auth_headers(),
            json={
                "url": self.url,
                "fields": self.fields,
            },
        )
        res.raise_for_status()

        data = res.json()
        self.rules = data["model_list"][0]
        logger.info("Rules fetched successfully for URL: " + self.url)
        logger.info("List element CSS selector: " + self.list_element_css_selector)
        logger.info("Fields: " + str(self.item_fields))
        logger.info(
            "Next page element CSS selector: "
            + str(self.next_page_element_css_selector)
        )

    def crawl(self):
        self.fetch_rules()
        futures = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures.append(executor.submit(self._fetch_data, self.url))

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
        logger.info("Crawling URL: " + url)
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        list_items = soup.select(self.list_element_css_selector)
        for item in list_items:
            row = {}
            for field in self.item_fields:
                name = field["name"]
                field_element = item.select_one(field["element_css_selector"])
                if not field_element:
                    continue
                if field["type"] == "text":
                    value = field_element.text.strip()
                else:
                    value = field_element.get(field["attribute"])
                row[name] = value
            self.data.append(row)
        logger.info("Fetched " + str(len(list_items)) + " items from URL: " + url)

        if self.next_page_element_css_selector:
            next_page_element = soup.select_one(self.next_page_element_css_selector)
            if next_page_element:
                logger.info("Next page found: " + next_page_element.get("href"))
                next_page_href = next_page_element.get("href")
                return urljoin(url, next_page_href)


def _get_fields(fields: List[str] | dict = None) -> Optional[List[str] | List[dict]]:
    if isinstance(fields, list):
        return fields
    elif isinstance(fields, dict):
        return [{"name": k, "description": v} for k, v in fields.items()]
    else:
        return None


def read_list(
    url: str,
    fields: List[str] | dict = None,
    get_html=None,
    as_dataframe=True,
    return_rules=False,
) -> DataFrame | List[dict] | tuple[DataFrame | List[dict], dict]:
    """
    Reads a list of items from a webpage and returns a DataFrame.

    Args:
        url (str): The URL to be crawled.
        fields (List[str] | dict): A list of fields to be extracted from each list element.
        get_html (function): A function to fetch the HTML content of a webpage. Defaults to the requests library.
        as_dataframe (bool): Whether to return the extracted data as a DataFrame. Defaults to True.
        return_rules (bool): Whether to return the rules used for extraction. Defaults to False.

    Returns:
        DataFrame | List[dict] | tuple[DataFrame | List[dict], dict]: The extracted data as a DataFrame or a list of
        dictionaries. If return_rules is True, a tuple containing the data and the rules used for extraction is
        returned.

    """
    spider = ListSpider(url=url, fields=_get_fields(fields), get_html=get_html)
    spider.crawl()
    if as_dataframe:
        return_data = DataFrame(spider.data)
    else:
        return_data = spider.data
    if return_rules:
        return return_data, spider.rules
    return return_data


def extract_list_rules(url: str, fields: List[str] | dict = None) -> dict:
    spider = ListSpider(url=url, fields=_get_fields(fields))
    spider.fetch_rules()
    return spider.rules


if __name__ == "__main__":
    df = read_list("https://quotes.toscrape.com")
    print(df)
    # df = read_list('https://36kr.com/', [
    #     'title',
    #     'author',
    #     'url',
    # ])
    # print(df)
