# -*- coding: utf-8 -*-

import json
import os
import time
from random import randint
from typing import List

import requests


def generate_http_request_headers() -> dict[str, str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    return headers


def generate_random_password() -> str:
    chars = get_chars()
    password = ''
    length = randint(9, 13)
    for i in range(length):
        password += chars[randint(0, len(chars) - 1)]
    return password


def get_token(address: str, password: str) -> str:
    res = requests.post(f'https://api.mail.tm/token', json={'address': address, 'password': password})
    res = json.loads(res.text)
    token = res['token']
    return token


def get_chars() -> List[str]:
    chars = []
    for i in range(ord('a'), ord('z') + 1):
        chars.append(chr(i))
        chars.append(chr(i).upper())
    chars += [str(x) for x in range(0, 10)]
    return chars


def generate_random_username() -> str:
    chars = get_chars()
    username = ''
    letters_length, digits_length = randint(4, 6), randint(3, 6)
    for _ in range(letters_length):
        username += chars[randint(0, len(chars) - 1)]
    for _ in range(digits_length):
        username += chars[randint(52, len(chars) - 1)]
    return username


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


def send_verification_code_to_email(email: str) -> None:
    link = 'https://pnod.top/api/v1/passport/comm/sendEmailVerify'
    res = requests.post(link, json={'email': email}, headers=generate_http_request_headers())
    print('-' * 50)
    print('sending verification code to email:' + email)
    print('result:', res.text)
    print('-' * 50)


def register_panda_node_account(email: str, verification_code: str, password: str) -> None:
    link = 'https://pnod.top/api/v1/passport/auth/register'
    res = requests.post(
        url=link,
        json={'email': email, 'email_code': verification_code, 'password': password},
        headers=generate_http_request_headers()
    )
    print(res.text)


def login_panda_node_account(email: str, password: str) -> str:
    link = 'https://pnod.top/api/v1/passport/auth/login'
    res = requests.post(url=link, data={'email': email, 'password': password})
    return res.json()['data']['token']


if __name__ == '__main__':
    email_address, email_password = create_mailtm_account()
    print('email_address: ' + email_address, ' email_password: ' + email_password)

    info = 'mail.tm email_address: ' + email_address + ' email_password: ' + email_password
    with open('registration_result.txt', 'w') as f:
        f.write(info)
        f.write('\n')

    send_verification_code_to_email(email_address)
    verification_code = get_verification_code(email_address, email_password)

    print('verification_code: ' + verification_code)

    panda_password = generate_random_password()

    with open('./registration_result.txt', 'a') as f:
        f.write('panda_password: %s\n' % panda_password)

    print('panda_password: ' + panda_password)
    with open('registration_result.txt', 'a') as f:
        f.write(panda_password)
        f.write('\n')
    register_panda_node_account(email_address, verification_code, panda_password)
    token = login_panda_node_account(email_address, panda_password)
    subscription_link = 'https://www.dnod.top/api/v1/client/subscribe?token=' + token
    print('subscription link: ', subscription_link)
    os.system('open %s' % subscription_link)
