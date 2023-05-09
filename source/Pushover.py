import http.client
import urllib
import urllib.parse


class Pushover:
    def __init__(self, token: str, user_key: str):
    self.token = token
    self.user_key = user_key

    def send_notification(self, message: str) -> None:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST",
            "/1/messages.json",
            urllib.parse.urlencode(
                {
                    "token": self.token,
                    "user": self.user_key,
                    "message": message,
                }
            ),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        conn.getresponse()
