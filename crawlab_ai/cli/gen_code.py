from crawlab_ai.code.article import get_code_article
from crawlab_ai.code.list import get_code_list
from crawlab_ai.utils.auth import get_token


def setup_gen_code_parser(subparsers):
    gen_code_parser = subparsers.add_parser(
        "gen_code", help="Generate crawler code for a webpage"
    )
    gen_code_parser.add_argument("url", help="URL to generate code for")
    gen_code_parser.add_argument(
        "-t",
        "--type",
        help="Type of the webpage to generate code for",
        default="list",
        choices=["article", "list"],
    )
    gen_code_parser.add_argument("-o", "--output", help="Output file path")
    gen_code_parser.set_defaults(func=gen_code)


def gen_code(args):
    get_token()
    if args.type == "list":
        gen_code_list(args)
    elif args.type == "article":
        gen_code_article(args)


def gen_code_list(args):
    code = get_code_list(args.url)
    if args.output:
        with open(args.output, "w") as f:
            f.write(code)
    else:
        print(code)


def gen_code_article(args):
    code = get_code_article(args.url)
    if args.output:
        with open(args.output, "w") as f:
            f.write(code)
    else:
        print(code)
