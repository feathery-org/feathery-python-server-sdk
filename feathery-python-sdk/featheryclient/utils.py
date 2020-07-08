import requests

def fetch_and_load_settings(features: dict, sdk_key: str) -> None:
    new_settings = get_settings_json(sdk_key)

    # TODO: Ensure atomicity?
    features = new_settings

def get_settings_json(sdk_key: str) -> dict:
    """
    Retrieves Configurations from unleash central server.
    Notes:
    * If unsuccessful (i.e. not HTTP status code 200), exception will be caught and logged.
        This is to allow "safe" error handling if unleash server goes down.
    :return: Configurations if successful, empty dict if not.
    """
    headers = { "Authorization": "Token " + sdk_key}

    resp = requests.get(API_URL,
                        headers={**headers},
                        timeout=REQUEST_TIMEOUT)

    if resp.status_code != 200:
        return {}

    return resp.json()