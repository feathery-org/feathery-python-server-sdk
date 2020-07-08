  
"""
The featheryclient module contains the most common top-level entry points for the SDK.
"""
import requests
from featheryclient.constants import API_URL, REQUEST_TIMEOUT, REFRESH_INTERVAL
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

class FeatheryClient():

    def set_sdk_key(self, sdk_key):
        """Sets the SDK key for the shared SDK client instance and initializes client, starting communication with 
        central Feathery server(s).
        :param string sdk_key: the new SDK key
        """
        
        self.sdk_key = sdk_key
        self.settings = {}  # type: Dict
        self.scheduler = BackgroundScheduler()

        self.api_url = API_URL
        self.refresh_interval = REFRESH_INTERVAL

        fetch_and_load_settings(self.settings, self.sdk_key)

        # Start periodic jobs
        self.scheduler.start()
        self.fl_job = self.scheduler.add_job(fetch_and_load_settings,
                                             trigger=IntervalTrigger(seconds=int(self.refresh_interval)),
                                             kwargs={"features": self.settings, "sdk_key": self.sdk_key})

        self.is_initialized = True

    def variation(self,
                    setting_key,
                    default_value,
                    user_key):
        # TODO should this return a str? If its a bool, it would be "true".
        # TODO Must handle invalid user ids and setting keys somehow
        """
        Checks the setting value for a user.  If the user and setting exist, return variant.
        Notes:
        * If client hasn't been initialized yet or an error occurs, flat will default to false.
        :param setting_key: Name of the setting
        :param default_value: Default value for the setting.
        :param user_key: Unique key belonging to the user.
        :return: Dict with variant and setting status.
        """

        if self.is_initialized:
            try:
                return self.settings[setting_key].overrides[user_key]
                # TODO you are accessing an array like it is a dict.
            except Exception as excep:
                return default_value
        else:
            return default_value

    def destroy(self):
        """
        Gracefully shuts down the Feathery client by stopping jobs, stopping the scheduler, and deleting the cache.
        :return:
        """
        self.fl_job.remove()
        self.scheduler.shutdown()

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