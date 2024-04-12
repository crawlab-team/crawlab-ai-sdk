from typing import Any, List, Iterable

import requests
from scrapy import Request
from scrapy.http import Response

from crawlab_ai.scrapy.base import BaseSpider
from crawlab_ai.utils.auth import get_auth_headers
from crawlab_ai.utils.logger import logger


class ScrapyListSpider(BaseSpider):
    """
    The ScrapyListSpider class is responsible for crawling a given URL and extracting data based on specified fields.
    It fetches rules from an API endpoint, which are used to identify list elements and fields within the webpage.
    The class also supports pagination by identifying the next page element and recursively crawling until no more pages
    are found.

    Attributes:
        fields (List[dict]): A list of fields to be extracted from each list element.

    Methods:
        parse(response: Response, **kwargs: Any) -> Iterable: Parses the response object and extracts data from the list
            elements.

    Usage:
        class MyListSpider(ScrapyListSpider):
            name = 'my_list_spider'
            start_urls = ['https://quotes.toscrape.com']
            fields = [
                {
                    'name': 'author',
                    'element_css_selector': '.author',
                    'is_text': True,
                },
                {
                    'name': 'quote',
                    'element_css_selector': '.text',
                    'is_text': True,
                },
                {
                    'name': 'tags',
                    'element_css_selector': '.tag',
                    'is_text': True,
                },
            ]

    """

    _fields: List[dict] = None
    _list_element_css_selector: str = None
    _next_page_element_css_selector: str = None

    fields: List[dict] = None

    def __init__(self):
        super(ScrapyListSpider, self).__init__()
        self._fetch_rules()

    def start_requests(self) -> Iterable[Request]:
        yield Request(self.start_urls[0], self.parse)

    def _fetch_rules(self):
        logger.info("Fetching rules for URL: " + self.start_urls[0])
        res = requests.post(
            url=self._api_endpoint + "/rules/list",
            headers=get_auth_headers(),
            json={
                "url": self.start_urls[0],
                "fields": self.fields,
            },
        )
        res.raise_for_status()

        data = res.json()
        self._list_element_css_selector = data["model_list"][0]["list_model"][
            "list_element_css_selector"
        ]
        self._fields = data["model_list"][0]["list_model"]["fields"]
        self._next_page_element_css_selector = data["model_list"][0][
            "next_page_element_css_selector"
        ]
        logger.info("Rules fetched.")
        logger.info("List element CSS selector: " + self._list_element_css_selector)
        logger.info("Fields: " + str(self._fields))
        logger.info(
            "Next page element CSS selector: "
            + str(self._next_page_element_css_selector)
        )

    def parse(self, response: Response, **kwargs: Any) -> Any:
        list_items = response.css(self._list_element_css_selector)
        for item in list_items:
            data = {}
            for field in self._fields:
                name = field["name"]
                if field["is_text"]:
                    selector = field["element_css_selector"] + "::text"
                else:
                    selector = (
                        field["element_css_selector"]
                        + "::attr("
                        + field["attribute"]
                        + ")"
                    )
                value = item.css(selector).get()
                data[name] = value
            yield data

        if self._next_page_element_css_selector:
            next_page_element = response.css(self._next_page_element_css_selector)
            next_page_href = next_page_element.css("a::attr(href)").get()
            if next_page_href:
                yield response.follow(next_page_href, self.parse)


if __name__ == "__main__":
    # dry run the scrapy spider
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    class TestScrapyListSpider(ScrapyListSpider):
        name = "list_spider"
        start_urls = ["https://quotes.toscrape.com"]

    process = CrawlerProcess(get_project_settings())
    process.crawl(TestScrapyListSpider)
    process.start()
