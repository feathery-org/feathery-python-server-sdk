import threading

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

from feathery.constants import API_URL, REFRESH_INTERVAL, REQUEST_TIMEOUT, POLL_FREQ_SECONDS
from feathery.utils import fetch_and_load_settings
from feathery.polling import PollingThread

class FeatheryClient:
    def __init__(self, sdk_key):
        """Sets the SDK key and spins up an asynchronous setting polling job.
        :param string sdk_key: the new SDK key
        """

        self.sdk_key = sdk_key
        self.settings = {}
        self.scheduler = BackgroundScheduler()

        self.api_url = API_URL
        self.refresh_interval = REFRESH_INTERVAL
        self.request_timeout = REQUEST_TIMEOUT
        self._lock = threading.Lock()

        fetch_and_load_settings(self.settings, self.sdk_key)

        # Start periodic job
        self.scheduler = PollingThread(features=self.settings sdk_key=self.sdk_key interval=POLL_FREQ_SECONDS, lock=self._lock)
        self.scheduler.start()

        self.is_initialized = True

    def variation(self, setting_key, default_value, user_key):
        # TODO Must handle invalid user ids and setting keys somehow
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

        if self.is_initialized:
            try:
                self._lock().aquire()
                variant = self.settings[setting_key].overrides[user_key]
                self._lock().release()
                return variant
            except Exception:
                return default_value
        else:
            return default_value

    def destroy(self):
        """
        Gracefully shuts down the Feathery client by stopping jobs, stopping
        the scheduler, and deleting the cache.
        :return:
        """
        self.scheduler.stop()
