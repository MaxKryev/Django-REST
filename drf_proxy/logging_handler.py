import logging
import requests


class LokiHandler(logging.Handler):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            "streams": [
                {
                    "stream": {
                        "application": "jwt_manager",
                    },
                    "values": [
                        [str(int(record.created * 1000000000)), log_entry]
                    ]
                }
            ]
        }
        try:
            requests.post(self.url, json=payload)
        except Exception as e:
            print(f"Failed to send log to Loki: {e}")

