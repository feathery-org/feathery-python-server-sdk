import threading

from feathery.constants import (
    API_URL,
    REFRESH_INTERVAL,
    REQUEST_TIMEOUT,
    POLL_FREQ_SECONDS,
)
from feathery.polling import PollingThread
from feathery.utils import fetch_and_return_settings


class FeatheryClient:
    def __init__(self, sdk_key):
        """Sets the SDK key and spins up an asynchronous setting polling job.
        :param string sdk_key: the new SDK key
        """

        self.sdk_key = sdk_key
        self.settings = {}

        self.api_url = API_URL
        self.refresh_interval = REFRESH_INTERVAL
        self.request_timeout = REQUEST_TIMEOUT
        self._lock = threading.Lock()

        self.settings = fetch_and_return_settings(self.sdk_key)

        # Start periodic job
        self.scheduler = PollingThread(
            features=self.settings,
            sdk_key=self.sdk_key,
            interval=POLL_FREQ_SECONDS,
            lock=self._lock,
        )
        self.scheduler.start()

        self.is_initialized = True

    def variation(self, setting_key, default_value, user_key):
        """
        Checks the setting value for a user.  If the user and setting exist,
        return variant.
        Notes:
        * If client hasn't been initialized yet or an error occurs, flat will
        default to false.
        :param setting_key: Name of the setting
        :param default_value: Default value for the setting.
        :param user_key: Unique key belonging to the user.
        :return: Dict with variant and setting status.
        """

        variant = default_value

        if self.is_initialized:
            self._lock.acquire()
            if setting_key in self.settings:
                if user_key in self.settings[setting_key]["overrides"]:
                    variant = self.settings[setting_key]["overrides"][user_key]
                else:
                    variant = self.settings[setting_key]["value"]
            self._lock.release()

        return variant

    def destroy(self):
        """
        Gracefully shuts down the Feathery client by stopping jobs, stopping
        the scheduler, and deleting the cache.
        :return:
        """
        self.scheduler.stop()
