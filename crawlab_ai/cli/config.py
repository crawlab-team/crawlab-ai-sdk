from crawlab_ai.utils.auth import set_token
from crawlab_ai.utils.env import set_api_endpoint


def setup_config_parser(subparsers):
    config_parser = subparsers.add_parser("config", help="Configure crawlab")
    # config_parser.add_argument(
    #     "-u", "--url", help="Crawlab API URL", default="http://localhost:8000"
    # )
    config_parser.add_argument("-t", "--token", help="Crawlab API token")
    config_parser.set_defaults(func=config)


def config(args):
    if args.token:
        set_token(args.token)

    if args.url:
        set_api_endpoint(args.url)
