from cloverapi.cloverapi_auth import CloverApiAuth
import requests


class CloverPay(object):
    def __init__(self, api_key, merchant_id, api_url):
        self.url = api_url.rstrip('/')
        self.merchant_id = merchant_id
        self.auth = CloverApiAuth(api_key=api_key)

    def get_secrets(self):
        r = requests.get(
            self.url + '/v2/merchant/' + self.merchant_id + '/pay/key/',
            auth=self.auth,
            timeout=30,
            params={}
        )
        return r.json()

    def send_payment(self, pay):
        payload = pay
        r = requests.post(
            self.url + '/v2/merchant/' + self.merchant_id + '/pay',
            auth=self.auth,
            timeout=30,
            json=payload
        )
        return r.json()
