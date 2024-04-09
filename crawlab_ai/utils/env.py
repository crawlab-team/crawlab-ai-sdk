import os


def get_api_endpoint():
    if os.getenv("CRAWLAB_AI_API_ENDPOINT"):
        return os.getenv("CRAWLAB_AI_API_ENDPOINT")

    # Try to get the API endpoint from the file
    config_file_path = os.path.join(
        os.path.expanduser("~"), ".crawlab", "api_endpoint.json"
    )
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as f:
            return f.read()

    return "https://crawlab-ai.azurewebsites.net"


def set_api_endpoint(endpoint: str):
    config_file_path = os.path.join(
        os.path.expanduser("~"), ".crawlab", "api_endpoint.json"
    )
    with open(config_file_path, "w") as f:
        f.write(endpoint)
