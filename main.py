import os
import json
import time
import string
import random
import datetime
import traceback
import threading
import urllib.request
from flask import Flask, jsonify

app = Flask(__name__)
app.config['TOTAL'] = 0
referrerID = os.environ.get("REFERRER_ID")


class WarpyAPI:
    @staticmethod
    def __gen_random_string(n):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

    @property
    def api_url(self):
        return 'https://api.cloudflareclient.com/v0a{}/reg'.format(random.randint(100, 999))

    def get_data(self):
        install_id = self.__gen_random_string(11)

        body = json.dumps(
            {
                'key': '{}='.format(self.__gen_random_string(43)),
                'install_id': install_id,
                'fcm_token': '{}:{}'.format(install_id, self.__gen_random_string(140)),
                'referrer': referrerID,
                'warp_enabled': False,
                'tos': datetime.datetime.now().astimezone().isoformat(),
                'type': 'Android',
            }
        ).encode('UTF-8')

        headers = {
            'Host': 'api.cloudflareclient.com',
            'User-Agent': 'okhttp/3.12.1',
            'Content-Type': 'application/json',
        }

        try:
            req = urllib.request.Request(self.api_url, headers=headers, data=body)
            response = urllib.request.urlopen(req)
            con = response.read().decode('UTF-8')
            if response.getcode() == 200 and referrerID in con:
                app.config['TOTAL'] += 1
                print('Total: {}GB... Earned 1GB.'.format(app.config['TOTAL']))

        except Exception:
            traceback.print_exc()

    def start(self):
        while True:
            self.get_data()
            time.sleep(int(os.environ.get("WAIT_TIME", 20)))


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            "status": "ok",
            "sended": app.config['TOTAL']
        }
    )

thread = threading.Thread(target=WarpyAPI().start, daemon=True)
thread.start()

if __name__ == '__main__':
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=os.environ.get("PORT", 5000)
    )
