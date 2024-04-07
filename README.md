# Crawlab AI SDK

This is the Python SDK for [Crawlab AI](https://www.crawlab.cn/ai), an AI-powered web scraping platform maintained
by [Crawlab](https://www.crawlab.cn).

## Installation

```bash
pip install crawlab-ai
```

## Pre-requisites

An API token is required to use this SDK. You can get the API token from
the [Crawlab official website](https://dev.crawlab.io/ai).

## Usage

### Get data from a list page

```python
from crawlab_ai import read_list

# Define the URL and fields
url = "https://example.com"

# Get the data without specifying fields
df = read_list(url=url)
print(df)

# You can also specify fields
fields = ["title", "content"]
df = read_list(url=url, fields=fields)

# You can also return a list of dictionaries instead of a DataFrame
data = read_list(url=url, as_dataframe=False)
print(data)
```

## Usage with Scrapy

Create a Scrapy spider by extending `ScrapyListSpider`:

```python
from crawlab_ai import ScrapyListSpider


class MySpider(ScrapyListSpider):
    name = "my_spider"
    start_urls = ["https://example.com"]
    fields = ["title", "content"]
```

Then run the spider:

```bash
scrapy crawl my_spider
```