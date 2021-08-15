import os
import json
import time
import string
import random
import datetime
import traceback
import urllib.error
import urllib.request
from urllib.parse import parse_qs, urlparse

config = {"TOTAL": 0}
referrerID = os.environ.get("REFERRER_ID")


class RedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return


class WarpyAPI:
    def __init__(self) -> None:
        self.referrerID = referrerID or self.get_refferID()

    @staticmethod
    def __gen_random_string(n):
        return "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(n)
        )

    @property
    def api_url(self):
        return "https://api.cloudflareclient.com/v0a{}/reg".format(
            random.randint(100, 999)
        )

    def get_refferID(self) -> str:
        opener = urllib.request.build_opener(RedirectHandler)
        urllib.request.install_opener(opener)
        try:
            resp = urllib.request.urlopen(
                os.environ.get("REFERRER_URL", "https://warp.plus/FRs9d")
            )
        except urllib.error.HTTPError as e:
            resp = e
        url = resp.headers.get("location")
        return parse_qs(urlparse(url).query)["referrer"][0]

    def get_data(self):
        install_id = self.__gen_random_string(11)

        body = json.dumps(
            {
                "key": "{}=".format(self.__gen_random_string(43)),
                "install_id": install_id,
                "fcm_token": "{}:{}".format(
                    install_id, self.__gen_random_string(140)
                ),
                "referrer": self.referrerID,
                "warp_enabled": False,
                "tos": datetime.datetime.now().astimezone().isoformat(),
                "type": "Android",
            }
        ).encode("UTF-8")

        headers = {
            "Host": "api.cloudflareclient.com",
            "User-Agent": "okhttp/3.12.1",
            "Content-Type": "application/json",
        }

        try:
            req = urllib.request.Request(
                self.api_url, headers=headers, data=body
            )
            response = urllib.request.urlopen(req)
            con = response.read().decode("UTF-8")
            if response.getcode() == 200 and self.referrerID in con:
                config["TOTAL"] += 1
                print("Total: {}GB... Earned 1GB.".format(config["TOTAL"]))

        except Exception:
            traceback.print_exc()

    def start(self):
        while True:
            self.get_data()
            time.sleep(int(os.environ.get("WAIT_TIME", 20)))


if __name__ == "__main__":
    WarpyAPI().start()
