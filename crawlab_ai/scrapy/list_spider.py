from typing import Any, List, Iterable

import requests
from scrapy import Request
from scrapy.http import Response

from crawlab_ai.scrapy.base_spider import BaseSpider
from crawlab_ai.utils.logger import logger


class ScrapyListSpider(BaseSpider):
    _fields: List[dict] = None
    _list_element_css_selector: str = None
    _next_page_element_css_selector: str = None

    fields: List[dict] = None

    def __init__(self):
        super(ScrapyListSpider, self).__init__()
        self._fetch_rules()

    def _fetch_rules(self):
        logger.info('Fetching rules for URL: ' + self.start_urls[0])
        res = requests.post(self._api_endpoint + '/list_rules', json={
            'url': self.start_urls[0],
            'fields': self.fields,
        })
        data = res.json()
        self._list_element_css_selector = data['model_list'][0]['list_model']['list_element_css_selector']
        self._fields = data['model_list'][0]['list_model']['fields']
        self._next_page_element_css_selector = data['model_list'][0]['next_page_element_css_selector']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        list_items = response.css(self._list_element_css_selector)
        for item in list_items:
            data = {}
            for field in self._fields:
                name = field['name']
                if field['is_text']:
                    selector = field['element_css_selector'] + '::text'
                else:
                    selector = field['element_css_selector'] + '::attr(' + field['attribute'] + ')'
                value = item.css(selector).get()
                data[name] = value
            yield data

        if self._next_page_element_css_selector:
            next_page_element = response.css(self._next_page_element_css_selector)
            next_page_href = next_page_element.css('a::attr(href)').get()
            if next_page_href:
                yield response.follow(next_page_href, self.parse)


if __name__ == '__main__':
    # dry run the scrapy spider
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings


    class TestScrapyListSpider(ScrapyListSpider):
        name = 'list_spider'
        start_urls = ['https://quotes.toscrape.com']


    process = CrawlerProcess(get_project_settings())
    process.crawl(TestScrapyListSpider)
