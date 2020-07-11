API_URL = "http://cdn.feathery.tech/external/"
REQUEST_TIMEOUT = 1
REFRESH_INTERVAL = 60
POLL_FREQ_SECONDS = 3
SDK = "123"
MOCK_ALL_SETTINGS = [
    {
        "value": False,
        "datatype": "boolean",
        "key": "setting",
        "overrides": [
            {"user_key": "user1", "user_value": False},
            {"user_key": "user2", "user_value": False},
            {"user_key": "user3", "user_value": False},
            {"user_key": "user4", "user_value": False},
            {"user_key": "user5", "user_value": False},
            {"user_key": "user6", "user_value": False},
            {"user_key": "user7", "user_value": False},
        ],
    },
    {
        "value": 100,
        "datatype": "int",
        "key": "setting2",
        "overrides": [
            {"user_key": "user1", "user_value": 1},
            {"user_key": "user2", "user_value": 2},
            {"user_key": "user3", "user_value": 3},
        ],
    },
    {"value": "10 4 * * *", "datatype": "string", "key": "setting3", "overrides": []},
    {"value": "5 4 * * 1", "datatype": "string", "key": "setting4", "overrides": []},
    {
        "value": 12,
        "datatype": "int",
        "key": "setting5",
        "overrides": [
            {"user_key": "user1", "user_value": 22},
            {"user_key": "user2", "user_value": 30},
            {"user_key": "user3", "user_value": 30},
            {"user_key": "user4", "user_value": 30},
            {"user_key": "56", "user_value": 30},
        ],
    },
    {
        "value": "000000",
        "datatype": "string",
        "key": "dashboard_color",
        "overrides": [],
    },
]
MOCK_ALL_SETTINGS_PROCESSED = {
    "setting": {
        "value": False,
        "datatype": "boolean",
        "overrides": {
            "user1": False,
            "user2": False,
            "user3": False,
            "user4": False,
            "user5": False,
            "user6": False,
            "user7": False,
        },
    },
    "setting2": {
        "value": 100,
        "datatype": "int",
        "overrides": {"user1": 1, "user2": 2, "user3": 3},
    },
    "setting3": {"value": "10 4 * * *", "datatype": "string", "overrides": {}},
    "setting4": {"value": "5 4 * * 1", "datatype": "string", "overrides": {}},
    "setting5": {
        "value": 12,
        "datatype": "int",
        "overrides": {"user1": 22, "user2": 30, "user3": 30, "user4": 30, "56": 30},
    },
    "dashboard_color": {"value": "000000", "datatype": "string", "overrides": {}},
}
