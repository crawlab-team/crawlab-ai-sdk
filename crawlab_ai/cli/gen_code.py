from crawlab_ai.utils.auth import get_token


def setup_gen_code_parser(subparsers):
    gen_code_parser = subparsers.add_parser(
        "gen_code", help="Generate crawler code for a webpage"
    )
    gen_code_parser.set_defaults(func=gen_code)


def gen_code(args):
    get_token()
