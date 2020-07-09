import copy
import threading 
import time

from feathery.utils import fetch_and_load_settings 

class PollingThread(Thread):
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
                    self.lock.aquire()
                    self.features = copy.deepcopy(fetch_and_load_settings(self.features, self.sdk_key))
                    self.features = all_data
                    self.lock.release()
                except Exception as e:
                    # TODO what to do here? Would just log.

                elapsed = time.time() - start_time
                if elapsed < self.interval:
                    time.sleep(self.interval - elapsed)
