import requests

from crawlab_ai.spider.base import BaseSpider
from crawlab_ai.utils.auth import get_auth_headers
from crawlab_ai.utils.env import get_api_endpoint
from crawlab_ai.utils.logger import logger


class ArticleSpider(BaseSpider):
    def __init__(self, url: str, get_html=None):
        super().__init__(url, get_html)
        self.data: dict | None = None
        self.url = url
        self.get_html = get_html or self.crawl

    def fetch_rules(self):
        logger.info("Fetching rules for URL: " + self.url)
        res = requests.post(
            url=get_api_endpoint() + "/rules/article",
            headers=get_auth_headers(),
            json={
                "url": self.url,
            },
        )
        if res.status_code != 200:
            raise Exception("Failed to fetch rules for URL: " + self.url)

        self.data = res.json()
        logger.info("Rules fetched successfully for URL: " + self.url)
        logger.info("Title: %s", self.data.get("title"))
        logger.info("Author: %s", self.data.get("author"))
        logger.info("Publish date: %s", self.data.get("publish_date"))
        logger.info("Content: %s", self.data.get("content")[:200])
        logger.info("Title CSS selector: %s", self.data.get("title_css_selector"))
        logger.info("Author CSS selector: %s", self.data.get("author_css_selector"))
        logger.info(
            "Publish date CSS selector: %s", self.data.get("publish_date_css_selector")
        )
        logger.info("Content CSS selector: %s", self.data.get("content_css_selector"))

    def crawl(self):
        logger.info("Crawling URL: " + self.url)
        self.fetch_rules()
        logger.info("Crawling completed for URL: " + self.url)


def read_article(url: str, get_html=None):
    spider = ArticleSpider(url, get_html)
    spider.crawl()
    return spider.data


if __name__ == "__main__":
    data = read_article("https://www.36kr.com/p/2601845967059847")
    print(data)
