import os


def get_api_endpoint():
    return os.getenv('CRAWLAB_AI_API_ENDPOINT') or 'https://crawlab-ai.azurewebsites.net'
