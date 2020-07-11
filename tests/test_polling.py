import pytest
import responses
import time
from feathery.polling import PollingThread
from feathery.rwlock import ReadWriteLock
from feathery.utils import fetch_and_return_settings
from testing_constants import (
    API_URL,
    REQUEST_TIMEOUT,
    POLL_FREQ_SECONDS,
    SDK,
    MOCK_ALL_SETTINGS_PROCESSED,
)


@pytest.fixture()
def test_polling_thread():
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
    polling_thread.run()
    yield polling_thread
    polling_thread.stop()


@pytest.fixture()
def test_polling_thread_nodestroy():
    responses.add(responses.GET, API_URL, json=MOCK_ALL_SETTINGS, status=200)
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
def test_polling_thread_settings(mocker):
    responses.add(responses.GET, API_URL, json=MOCK_ALL_SETTINGS, status=200)
    thread_context = {
        "settings": fetch_and_return_settings(SDK),
        "is_initialized": False,
    }
    lock = ReadWriteLock()
    polling_thread = PollingThread(
        context=thread_context, sdk_key=SDK, interval=POLL_FREQ_SECONDS, lock=lock,
    )

    polling_thread.start()
    time.sleep(1)
    polling_thread.cv.acquire()
    print(polling_thread.context["settings"])
    assert polling_thread.context["settings"] == MOCK_ALL_SETTINGS_PROCESSED
    polling_thread.cv.release()
    polling_thread.stop()
