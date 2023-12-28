# -*- coding: utf-8 -*-

import json
import time

import requests

from src.clash_subscription_registration_helper.util import generate_random_username, generate_random_password


def get_domain() -> str:
    res = requests.get('https://api.mail.tm/domains')
    res = json.loads(res.text)
    domain = res['hydra:member'][0]['domain']
    return domain


def create_mailtm_account() -> tuple[str, str]:
    address = f'{generate_random_username().lower()}@{get_domain()}'
    password = generate_random_password()
    requests.post(f'https://api.mail.tm/accounts', json={'address': address, 'password': password})
    print('mail.tm account created, username: ' + address + ', password: ' + password)
    return address, password


def get_token(address: str, password: str) -> str:
    res = requests.post(f'https://api.mail.tm/token', json={'address': address, 'password': password})
    res = json.loads(res.text)
    token = res['token']
    return token


def get_verification_code(address: str, password: str) -> str:
    t = 0
    while True:
        t += 1
        if t > 60:
            return get_verification_code(address, password)
        token = get_token(address, password)
        res = requests.get(f'https://api.mail.tm/messages', headers={'Authorization': f'Bearer {token}'})
        res = json.loads(res.text)
        if len(res['hydra:member']) > 0:
            content = res['hydra:member'][0]['intro']
            code = ''
            i = 0
            while i < len(content):
                if content[i].isdigit():
                    j = i + 1
                    while j < len(content):
                        if content[j].isdigit():
                            j += 1
                        else:
                            break
                    code = content[i:j]
                    break
                i += 1
            return code
        time.sleep(1)
