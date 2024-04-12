import argparse

from crawlab_ai.cli.gen_code import setup_gen_code_parser
from crawlab_ai.cli.config import setup_config_parser
from crawlab_ai.cli.crawl import setup_crawl_parser

parser = argparse.ArgumentParser(description="Web scraping tool")
subparsers = parser.add_subparsers(dest="command")

setup_crawl_parser(subparsers)
setup_gen_code_parser(subparsers)
setup_config_parser(subparsers)


def main():
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
