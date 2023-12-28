from src.clash_subscription_registration_helper.api.mailtm_api import *
from src.clash_subscription_registration_helper.util import *


def register_panda_node_account(email: str, verification_code: str, password: str) -> None:
    link = 'https://pnod.top/api/v1/passport/auth/register'
    res = requests.post(link, json={'email': email, 'email_code': verification_code, 'password': password},
                        headers=generate_http_request_headers())
    print(res.text)


if __name__ == '__main__':
    email_address, email_password = create_mailtm_account()
    print('email_address: ' + email_address, ' email_password: ' + email_password)

    info = 'mail.tm email_address: ' + email_address + ' email_password: ' + email_password
    with open('registration_result', 'w') as f:
        f.write(info)
        f.write('\n')

    send_verification_code_to_email(email_address)
    verification_code = get_verification_code(email_address, email_password)

    print('verification_code: ' + verification_code)

    panda_password = generate_random_password()
    print('panda_password: ' + panda_password)
    with open('registration_result', 'a') as f:
        f.write(panda_password)
        f.write('\n')
    register_panda_node_account(email_address, verification_code, panda_password)
