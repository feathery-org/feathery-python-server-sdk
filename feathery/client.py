from feathery.constants import POLL_FREQ_SECONDS
from feathery.polling import PollingThread
from feathery.rwlock import ReadWriteLock
from feathery.utils import fetch_and_return_settings


class FeatheryClient:
    def __init__(self, sdk_key):
        """Sets the SDK key and spins up an asynchronous setting polling job.
        :param string sdk_key: the new SDK key
        """

        self.lock = ReadWriteLock()
        self.thread_context = {
            "settings": fetch_and_return_settings(sdk_key),
            "is_initialized": False,
        }

        # Start periodic job
        self.scheduler = PollingThread(
            context=self.thread_context,
            sdk_key=sdk_key,
            interval=POLL_FREQ_SECONDS,
            lock=self.lock,
        )
        self.scheduler.start()

    def variation(self, setting_key, default_value, user_key):
        """
        Return the setting value for a user.
        :param setting_key: Name of the setting
        :param default_value: Default value for the setting.
        :param user_key: Unique key belonging to the user.
        :return: Dict with variant and setting status.
        """

        variant = default_value

        self.lock.rlock()
        if self.thread_context["is_initialized"]:
            settings = self.thread_context["settings"]
            if setting_key in settings:
                setting = settings[setting_key]
                if user_key in setting["overrides"]:
                    variant = setting["overrides"][user_key]
                else:
                    variant = setting["value"]
        self.lock.runlock()

        return variant

    def halt(self):
        """
        Gracefully shuts down the Feathery client by halting the scheduler.
        :return:
        """
        self.scheduler.stop()
