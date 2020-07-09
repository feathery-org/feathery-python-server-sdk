import requests

from feathery.constants import API_URL, REQUEST_TIMEOUT


def fetch_and_return_settings(sdk_key: str) -> dict:
    new_settings = get_settings_json(sdk_key)

    new_dict = {}
    for item in new_settings:
        name = item["key"]
        overrides = {
            override_item["user_key"]: override_item["user_value"]
            for override_item in item["overrides"]
        }
        new_dict[name] = {
            "value": item["value"],
            "datatype": item["datatype"],
            "overrides": overrides,
        }
    return new_dict


def get_settings_json(sdk_key: str) -> dict:
    """
    Retrieves settings from Feathery central server.
    Notes:
    * If unsuccessful (i.e. not HTTP status code 200), exception will be caught and logged.
        This is to allow "safe" error handling if unleash server goes down.
    :return: Configurations if successful, empty dict if not.
    """
    headers = {"Authorization": "Token " + sdk_key}
    resp = requests.get(API_URL, headers={**headers}, timeout=REQUEST_TIMEOUT)
    if resp.status_code != 200:
        return {}
    return resp.json()
