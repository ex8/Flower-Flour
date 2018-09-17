from django.shortcuts import render, redirect
from django.conf import settings
from clover.models import Clover
import requests
from django.contrib.auth.decorators import user_passes_test

# PROD --> https://www.clover.com
# DEV  --> https://sandbox.dev.clover.com
BASE_URL = 'https://www.clover.com'

HEADERS = {
    'Authorization': 'Client ' + settings.CLOVER_APP_SECRET,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


@user_passes_test(lambda u: u.is_superuser)
def authorize(request):
    url = '{}/oauth/authorize?client_id={}&redirect_uri={}'\
        .format(BASE_URL, settings.CLOVER_APP_ID, settings.CLOVER_REDIRECT_URI)
    return render(request=request, template_name='clover/auth.html', context={
        'url': url,
    })


@user_passes_test(lambda u: u.is_superuser)
def oauth_callback(request):
    token = get_token(request.GET['code'])
    if token:
        Clover(access_token=token['access_token']).save()
        return redirect('main:home')
    else:
        return redirect('menu:list')


def get_token(auth_code):
    r = requests.get(
        url='{}/oauth/'
            'token?client_id={}'
            '&client_secret={}'
            '&code={}'
        .format(BASE_URL, settings.CLOVER_APP_ID, settings.CLOVER_APP_SECRET,
                auth_code)
    )
    return r.json()
