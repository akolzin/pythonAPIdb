import requests


class RestfulBookerClient:

    _s = requests.session()
    host = None

    def __init__(self, host):
        self.host = host

    def login(self, username, password):
        data = {"username": username, "password": password}
        return self._s.post(self.host + "/auth", json=data)

    def authorize(self, username, password):
        res = self.login(username, password)
        if res.status_code != 200:
            raise Exception("Unable to authorize using given credentials")
        session_token = res.json().get("token")
        cookie = requests.cookies.create_cookie("token", session_token)
        self._s.cookies.set_cookie(cookie)

    def create_booking(self, data: dict):
        return self._s.post(self.host + "/booking", json=data)

    def update_booking(self, uid: int, data: dict):
        return self._s.put(self.host + f"/booking/{uid}", json=data)

    def get_booking(self, uid: int):
        return self._s.get(self.host + f"/booking/{uid}")