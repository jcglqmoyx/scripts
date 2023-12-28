import os
from functools import cache
from random import randint
from typing import List
from urllib.parse import unquote

import requests


@cache
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


def generate_random_password() -> str:
    chars = get_chars()
    password = ''
    length = randint(9, 13)
    for i in range(length):
        password += chars[randint(0, len(chars) - 1)]
    return password


def generate_random_email() -> str:
    domains = ['gmail.com', 'hotmail.com', 'live.com', 'yahoo.com', 'icloud.com', 'outlook.com', 'protonmail.com',
               'tutanota.de', 'tutanota.com', 'tutamail.com', 'tuta.io', 'yandex.com', 'sina.com', 'qq.com',
               'naver.com', '163.com', 'yeah.net', '126.com', 'aliyun.com', 'foxmail.com']
    return generate_random_username() + '@' + domains[randint(0, len(domains) - 1)]


def generate_http_request_headers() -> dict[str, str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    return headers


def download_subscription_configuration_file(link: str) -> None:
    response = requests.get(link)
    save_path = '/Users/hqc/.config/clash'

    if response.status_code == 200:
        # 从Content-Disposition中获取文件名
        content_disposition = response.headers.get('Content-Disposition', '')
        file_name = unquote(content_disposition.split('filename=')[1].strip('\"'))

        # 如果Content-Disposition中没有文件名，则从URL中提取
        if not file_name:
            file_name = os.path.basename(link)

        # 拼接保存路径
        save_file_path = os.path.join(save_path, file_name)

        # 保存文件
        with open(save_file_path, 'wb') as file:
            file.write(response.content)

        print(f"File downloaded: {save_file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None
