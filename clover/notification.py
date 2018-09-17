from requests.auth import AuthBase
import requests


class CloverApiNotifyAuth(AuthBase):
    def __init__(self, app_secret):
        self.app_secret = app_secret

    def __call__(self, request):
        request.headers.update(get_auth_headers(self.app_secret))
        return request


def get_auth_headers(app_secret):
    return {
        'Content-Type': 'Application/JSON',
        'Authorization': 'Bearer ' + app_secret
    }


class NotifyService:
    def __init__(self, url, auth, mId):
        self.url = url
        self.auth = CloverApiNotifyAuth(auth)
        self.mId = mId

    def notify_device(self, device_id, app_id, payload):
        r = requests.post(
            self.url + '/v3/apps/' + app_id + '/devices/' + device_id + '/notifications/',
            auth=self.auth,
            timeout=30,
            json=payload
        )
        return r.json()
