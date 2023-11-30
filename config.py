import os


class AppConfig:
    def __init__(self):
        self.server_host = get_from_environment('0.0.0.0', 'IMAGE_MANAGER_SERVER_HOST')
        self.server_port = int(get_from_environment('8184', 'IMAGE_MANAGER_SERVER_PORT'))
        self.server_version = get_from_environment('1.0.0', 'IMAGE_MANAGER_SERVER_VERSION')
        self.server_api_key = get_from_environment('60445049bbd14058bba6451e4ce91584', 'IMAGE_MANAGER_SERVER_API_KEY')
        self.google_api_key = get_from_environment('', 'IMAGE_MANAGER_GOOGLE_API_KEY')
        self.google_url = get_from_environment('https://vision.googleapis.com/v1/images:annotate', 'IMAGE_MANAGER_GOOGLE_URL')


def get_from_environment(default, environment):
    val = os.environ.get(environment)
    if val is None:
        return default
    else:
        return val
