# -*- coding: utf-8 -*-
import requests

from util import *


def download_subscription_configuration_file(link: str) -> None:
    res = requests.get(link, headers=get_http_request_headers())
    with open('/Users/hqc/.config/clash/Cyanmori.yaml', 'w') as f:
        f.write(res.text)


def register() -> tuple[str, str]:
    registration_api = 'https://pslc.cccc.gg/auth/register'
    username, email, password = get_username(), get_email(), get_password()

    info = 'link: %s username: %s email: %s password: %s\n' % (registration_api, username, email, password)
    print(info)
    f = open('./registration_result.txt', 'a')
    f.write(info)
    f.close()

    requests.post(url=registration_api, headers=get_http_request_headers(), json={
        'name': username,
        'email': email,
        'passwd': password,
        'repasswd': password,
    })
    return email, password


def parse_dict_cookies(cookies):
    res = {}
    for item in cookies:
        s = str(item).split(' ')[1]
        ss = s.split('=')
        res[ss[0]] = ss[1]
    return res


def login() -> None:
    login_api = 'https://dd52.cccc.gg/auth/login'
    email, password = register()
    res = requests.post(url=login_api, headers=get_http_request_headers(), json={
        'email': email,
        'passwd': password,
    })

    user_profile_api = 'https://dd52.cccc.gg/user'

    res = requests.get(
        url=user_profile_api,
        headers=get_http_request_headers(),
        cookies=parse_dict_cookies(res.cookies)
    )

    sub = 'index.oneclickImport(\'clash\',\''
    idx = res.text.find(sub)

    subscription_link = res.text[idx + len(sub): res.text.find('\'', idx + len(sub))]
    download_subscription_configuration_file(subscription_link)


if __name__ == '__main__':
    login()
