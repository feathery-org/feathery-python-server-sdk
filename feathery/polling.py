import threading

from feathery.utils import fetch_and_return_settings


class PollingThread(threading.Thread):
    def __init__(self, context, sdk_key, interval, lock):
        threading.Thread.__init__(self)
        self._run = True
        self.context = context
        self.sdk_key = sdk_key
        self.interval = interval
        self.context_lock = lock
        self.cv = threading.Condition(threading.Lock())

    def run(self):
        self.cv.acquire()
        while self._run:
            try:
                all_data = fetch_and_return_settings(self.sdk_key)
                self.context_lock.lock()
                self.context["settings"] = all_data
                self.context["is_initialized"] = True
                self.context_lock.unlock()
            except Exception:
                pass
            self.cv.wait(self.interval)
        self.cv.release()

    def stop(self):
        self._run = False
        self.cv.acquire()
        self.cv.notify(1)
        self.cv.release()
        self.join()
