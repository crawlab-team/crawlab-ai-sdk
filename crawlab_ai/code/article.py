import requests
from crawlab_ai.spider.article_spider import extract_article_rules
from crawlab_ai.utils.auth import get_auth_headers
from crawlab_ai.utils.env import get_api_endpoint


def get_code_article(url: str):
    rules = extract_article_rules(url)
    res = requests.post(
        url=get_api_endpoint() + "/code/article",
        headers=get_auth_headers(),
        json={"url": url, "rules": rules},
    )
    res.raise_for_status()
    data = res.json()
    return data["source_code"]


if __name__ == "__main__":
    print(get_code_article("https://www.36kr.com/p/2601845967059847"))
