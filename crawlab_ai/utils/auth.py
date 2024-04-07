import os


def get_token() -> str:
    # Get token from environment variable
    if 'CRAWLAB_TOKEN' in os.environ:
        return os.environ['CRAWLAB_TOKEN']

    # Prompt user to enter token
    token = input('Please enter your API token for Crawlab AI: ')
    return token


def get_auth_headers() -> dict:
    return {
        'Authorization': f'Bearer {get_token()}'
    }


if __name__ == '__main__':
    print(get_token())
