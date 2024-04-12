import requests

from crawlab_ai.spider.base import BaseSpider
from crawlab_ai.utils.auth import get_auth_headers
from crawlab_ai.utils.env import get_api_endpoint
from crawlab_ai.utils.logger import logger


class ArticleSpider(BaseSpider):
    def __init__(self, url: str, get_html=None):
        super().__init__(url, get_html)
        self.rules: dict | None = None
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
        res.raise_for_status()

        self.rules = res.json()
        logger.info("Rules fetched successfully for URL: " + self.url)
        logger.info("Title: %s", self.rules.get("title"))
        logger.info("Author: %s", self.rules.get("author"))
        logger.info("Publish date: %s", self.rules.get("publish_date"))
        logger.info("Content: %s", self.rules.get("content")[:200])
        logger.info("Title CSS selector: %s", self.rules.get("title_css_selector"))
        logger.info("Author CSS selector: %s", self.rules.get("author_css_selector"))
        logger.info(
            "Publish date CSS selector: %s", self.rules.get("publish_date_css_selector")
        )
        logger.info("Content CSS selector: %s", self.rules.get("content_css_selector"))

    def crawl(self):
        logger.info("Crawling URL: " + self.url)
        self.fetch_rules()
        logger.info("Crawling completed for URL: " + self.url)


def read_article(url: str, get_html=None) -> dict:
    """
    Read an article from a URL

    Args:
        url (str): URL of the article
        get_html (function): Function to get HTML content

    Returns:
        dict: Article data
    """
    spider = ArticleSpider(url, get_html)
    spider.crawl()
    return spider.rules


def extract_article_rules(url: str, get_html=None) -> dict:
    """
    Extract article rules from a URL

    Args:
        url (str): URL of the article
        get_html (function): Function to get HTML content

    Returns:
        dict: Article rules
    """
    spider = ArticleSpider(url, get_html)
    spider.fetch_rules()
    return spider.rules


if __name__ == "__main__":
    data = read_article("https://www.36kr.com/p/2601845967059847")
    print(data)
