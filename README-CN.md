# Crawlab AI SDK

这是由[Crawlab](https://www.crawlab.cn)维护的AI驱动的网页抓取平台[Crawlab AI](https://www.crawlab.cn/ai)的Python SDK。

## 安装

```bash
pip install crawlab-ai

## 先决条件
使用此SDK需要API令牌。您可以从[Crawlab官方网站](https://dev.crawlab.io/ai)获取API令牌。
## 使用方法
### 从列表页面获取数据
```python
from crawlab_ai import read_list
# 定义URL和字段
url = "https://example.com"
# 获取数据而不指定字段
df = read_list(url=url)
print(df)
# 您也可以指定字段
fields = ["title", "content"]
df = read_list(url=url, fields=fields)
# 您还可以返回字典列表而不是DataFrame
data = read_list(url=url, as_dataframe=False)
print(data)
```
## 与Scrapy一起使用
通过扩展`ScrapyListSpider`创建一个Scrapy爬虫：
```python
from crawlab_ai import ScrapyListSpider
class MySpider(ScrapyListSpider):
    name = "my_spider"
    start_urls = ["https://example.com"]
    fields = ["title", "content"]
```
然后运行爬虫：
```bash
scrapy crawl my_spider
```
```
