# Crawlab AI SDK

This is the Python SDK for Crawlab AI.

## Installation

```bash
pip install crawlab-ai
```

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

# You can also return a list of dictionaries
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