"""
SDK public entry points are contained here. This design enforces the singleton
model -- only one instance of `feathery` can exist at any time.
"""
from feathery.client import FeatheryClient

__client = None


def set_sdk_key(sdk_key):
    """Sets the SDK auth key and initializes the shared client instance.
    If the shared client instance is already initialized, this function no-ops.
    :param string sdk_key: the new SDK key
    """
    global __client
    if __client is None:
        __client = FeatheryClient(sdk_key)


def get():
    """Returns the shared SDK client instance. To use the SDK as a singleton,
    first make sure you have called :func:`feathery.set_sdk_key()` at
    startup time. Then ``get()`` will then return the same shared
    :class:`feathery.client.FeatheryClient` instance each time. If
    :func:`feathery.set_sdk_key()` has not been called, `None` will be
    returned.
    :rtype: feathery.client.FeatheryClient
    """
    global __client
    return __client
