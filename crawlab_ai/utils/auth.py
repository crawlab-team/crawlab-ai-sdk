import os
import sys


def get_token() -> str:
    # Get token from environment variable
    if "CRAWLAB_TOKEN" in os.environ:
        return os.environ["CRAWLAB_TOKEN"]

    # Get token from file
    token_file_path = os.path.join(os.path.expanduser("~"), ".crawlab", "token")
    if os.path.exists(token_file_path):
        with open(token_file_path, "r") as f:
            return f.read()

    # Token not found
    print("API token not found. Please set the CRAWLAB_TOKEN environment variable.")
    print(
        "If you don't have an API token, please sign up and apply at https://www.crawlab.cn/ai"
    )
    sys.exit(1)


def set_token(token: str):
    token_file_path = os.path.join(os.path.expanduser("~"), ".crawlab", "token")
    with open(token_file_path, "w") as f:
        f.write(token)


def get_auth_headers() -> dict:
    return {"Authorization": f"Bearer {get_token()}"}
