from crawlab_ai.code.article import get_code_article
from crawlab_ai.code.list import get_code_list
from crawlab_ai.utils.auth import get_token


def setup_codegen_parser(subparsers):
    codegen_parser = subparsers.add_parser(
        "gen_code", help="Generate crawler code for a webpage"
    )
    codegen_parser.add_argument("url", help="URL to generate code for")
    codegen_parser.add_argument(
        "-t",
        "--type",
        help="Type of the webpage to generate code for",
        default="list",
        choices=["article", "list"],
    )
    codegen_parser.add_argument("-o", "--output", help="Output file path")
    codegen_parser.set_defaults(func=codegen)


def codegen(args):
    get_token()
    if args.type == "list":
        codegen_list(args)
    elif args.type == "article":
        codegen_article(args)


def codegen_list(args):
    code = get_code_list(args.url)
    if args.output:
        with open(args.output, "w") as f:
            f.write(code)
    else:
        print(code)


def codegen_article(args):
    code = get_code_article(args.url)
    if args.output:
        with open(args.output, "w") as f:
            f.write(code)
    else:
        print(code)
