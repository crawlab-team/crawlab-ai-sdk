import json

from tabulate import tabulate

from crawlab_ai import read_list, read_article
from crawlab_ai.utils.auth import get_token


def setup_crawl_parser(subparsers):
    crawl_parser = subparsers.add_parser("crawl", help="Crawl a website")
    crawl_parser.add_argument("url", help="URL to crawl")
    crawl_parser.add_argument(
        "-t",
        "--type",
        help="Type of the website to crawl",
        default="list",
        choices=["article", "list"],
    )
    crawl_parser.add_argument("-o", "--output", help="Output file path")
    crawl_parser.set_defaults(func=crawl)


def crawl(args):
    get_token()
    if args.type == "list":
        crawl_list(args)
    elif args.type == "article":
        crawl_article(args)


def crawl_list(args):
    df = read_list(args.url)
    if args.output:
        df.to_csv(args.output)
    else:
        print(tabulate(df, headers='keys', tablefmt='psql'))


def crawl_article(args):
    data = read_article(args.url)
    with open(args.output, "w") as f:
        f.write(json.dumps(data))
