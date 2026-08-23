import requests
import json
from base64 import b64encode

class Savoir:
    def __init__(self, rpcuser, rpcpasswd, rpchost, rpcport, chainname):
        self.rpcuser = rpcuser
        self.rpcpasswd = rpcpasswd
        self.rpchost = rpchost
        self.rpcport = rpcport
        self.chainname = chainname
        self.url = f"http://{rpchost}:{rpcport}"
        auth_str = f"{rpcuser}:{rpcpasswd}"
        self.headers = {
            "Authorization": f"Basic {b64encode(auth_str.encode()).decode()}",
            "Content-Type": "text/plain"
        }

    def __getattr__(self, name):
        def wrapper(*args):
            payload = {
                "method": name,
                "params": list(args),
                "id": 1,
                "chain_name": self.chainname
            }
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
            response.raise_for_status()
            return response.json().get('result')
        return wrapper
