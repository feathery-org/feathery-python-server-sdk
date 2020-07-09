import copy
import threading
import time

from feathery.utils import fetch_and_return_settings


class PollingThread(threading.Thread):
    def __init__(self, features, sdk_key, interval, lock):
        threading.Thread.__init__(self)
        self._running = False
        self.features = features
        self.sdk_key = sdk_key
        self.interval = interval
        self.lock = lock

    def run(self):
        if not self._running:
            self._running = True
            while self._running:
                start_time = time.time()
                try:
                    all_data = fetch_and_return_settings(self.sdk_key)
                    self.lock.aquire()
                    self.features = copy.deepcopy(all_data)
                    self.lock.release()
                except Exception:
                    pass

                elapsed = time.time() - start_time
                if elapsed < self.interval:
                    time.sleep(self.interval - elapsed)

    def stop(self):
        self._running = False
