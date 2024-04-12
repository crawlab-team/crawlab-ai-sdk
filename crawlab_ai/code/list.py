from typing import List

import requests
from crawlab_ai.spider.list_spider import extract_list_rules
from crawlab_ai.utils.auth import get_auth_headers
from crawlab_ai.utils.env import get_api_endpoint


def get_code_list(url: str, fields: List[str] | dict = None):
    rules = extract_list_rules(url, fields)
    res = requests.post(
        url=get_api_endpoint() + "/code/list",
        headers=get_auth_headers(),
        json={"url": url, "rules": rules},
    )
    res.raise_for_status()
    data = res.json()
    return data["source_code"]


if __name__ == "__main__":
    print(get_code_list("https://quotes.toscrape.com"))
