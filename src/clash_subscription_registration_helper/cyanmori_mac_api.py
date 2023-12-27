# -*- coding: utf-8 -*-

import os
from urllib.parse import unquote

import requests

from util import get_http_request_headers, get_username, get_email, get_password


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


def register() -> tuple[str, str]:
    registration_api = 'https://pslc.cccc.gg/auth/register'
    username, email, password = get_username(), get_email(), get_password()

    info = 'link: %s username: %s email: %s password: %s\n' % (registration_api, username, email, password)
    print(info)
    f = open('./registration_result.txt', 'a')
    f.write(info)
    f.close()

    res = requests.post(url=registration_api, headers=get_http_request_headers(), json={
        'name': username,
        'email': email,
        'passwd': password,
        'repasswd': password,
    })
    print(res.headers["Content-Type"])
    s = res.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    print('-' * 100)
    print(s)
    print('-' * 100)
    return email, password


def parse_dict_cookies(cookies):
    res = {}
    for item in cookies:
        s = str(item).split(' ')[1]
        ss = s.split('=')
        res[ss[0]] = ss[1]
    return res


def main() -> None:
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
    main()
