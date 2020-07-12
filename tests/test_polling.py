import pytest
import responses
import time

from feathery.polling import PollingThread
from feathery.rwlock import ReadWriteLock
from feathery.utils import fetch_and_return_settings
from testing_constants import (
    API_URL,
    MOCK_ALL_SETTINGS,
    MOCK_ALL_SETTINGS_PROCESSED,
    POLL_FREQ_SECONDS,
    SDK,
)


@pytest.fixture()
def polling_thread():
    responses.add(responses.GET, API_URL, json=MOCK_ALL_SETTINGS, status=200)
    # Start periodic job
    thread_context = {
        "settings": fetch_and_return_settings(SDK),
        "is_initialized": False,
    }
    lock = ReadWriteLock()
    polling_thread = PollingThread(
        context=thread_context, sdk_key=SDK, interval=POLL_FREQ_SECONDS, lock=lock,
    )
    polling_thread.start()
    yield polling_thread
    polling_thread.stop()


@responses.activate
def test_polling_thread_settings(polling_thread):
    time.sleep(1)
    polling_thread.context_lock.lock()
    assert polling_thread.context["settings"] == MOCK_ALL_SETTINGS_PROCESSED
    polling_thread.context_lock.unlock()
