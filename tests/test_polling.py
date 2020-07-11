import time
import json
import pytest
import responses
import feathery
from feathery.polling import PollingThread
from feathery.rwlock import ReadWriteLock

from testing_constants import API_URL, MOCK_ALL_SETTINGS, REQUEST_TIMEOUT, REFRESH_INTERVAL, POLL_FREQ_SECONDS, SDK


@pytest.fixture()
def polling_thread(tmpdir):
    # Start periodic job
    thread_context = {
            "settings": fetch_and_return_settings(sdk_key),
            "is_initialized": False,
        }
    lock = ReadWriteLock()
    polling_thread = PollingThread(
        context=thread_context,
        sdk_key=SDK,
        interval=POLL_FREQ_SECONDS,
        lock=lock,
    )
    polling_thread.run()
    yield polling_thread
    polling_thread.stop()


@pytest.fixture()
def polling_thread_nodestroy(tmpdir):
    thread_context = {
            "settings": fetch_and_return_settings(sdk_key),
            "is_initialized": False,
        }
    lock = ReadWriteLock()
    polling_thread = PollingThread(
        context=thread_context,
        sdk_key=sdk_key,
        interval=POLL_FREQ_SECONDS,
        lock=self.lock,
    )
    polling_thread.run()
    yield polling_thread
    polling_thread.stop()

@responses.activate
def polling_thread():
    mocker.patch('time.sleep', side_effect=Exception('mocked error'))
    thread_context = {
            "settings": fetch_and_return_settings(sdk_key),
            "is_initialized": False,
        }
    lock = ReadWriteLock()
    polling_thread = PollingThread(
        context=thread_context,
        sdk_key=SDK,
        interval=POLL_FREQ_SECONDS,
        lock=lock,
    )
    try:
        polling_thread.run()
    finally:
        assert polling_thread.context["settings"] = MOCK_ALL_SETTINGS

    yield polling_thread
    polling_thread.stop()
