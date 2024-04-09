from abc import abstractmethod

import requests


class BaseSpider(object):
    def __init__(self, url: str, get_html=None):
        self.url = url
        self.get_html = get_html or self._get_html

    @staticmethod
    def _get_html(url):
        res = requests.get(url)
        return res.text

    @abstractmethod
    def crawl(self): ...

    @abstractmethod
    def fetch_rules(self): ...
