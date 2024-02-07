import scrapy

from crawlab_ai.utils.env import get_api_endpoint


class BaseSpider(scrapy.Spider):
    _api_endpoint: str = get_api_endpoint()
