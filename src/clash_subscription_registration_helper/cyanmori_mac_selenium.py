import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from util import get_username, get_email, get_password


def register_cyanmori_account():
    link = 'https://9g21.cccc.gg/auth/register'
    name_xpath = '/html/body/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div[1]/div/input'
    email_xpath = '/html/body/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div[2]/div/input'
    password_xpath = '/html/body/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div[3]/div/input'
    password_confirmation_xpath = '/html/body/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div[4]/div/input'

    register_button_xpath = '/html/body/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/button/span'

    start_using_button_xpath = '/html/body/div[3]/div[7]/div/button'

    driver = webdriver.Chrome()
    driver.get(link)

    username, email, password = get_username(), get_email(), get_password()

    info = 'link: %s username: %s email: %s password: %s\n' % (link, username, email, password)
    print(info)
    f = open('./registration_result.txt', 'a')
    f.write(info)
    f.close()

    time.sleep(1)
    driver.find_element(By.XPATH, name_xpath).send_keys(username)
    time.sleep(0.2)
    driver.find_element(By.XPATH, email_xpath).send_keys(email)
    time.sleep(0.2)
    driver.find_element(By.XPATH, password_xpath).send_keys(password)
    time.sleep(0.2)
    driver.find_element(By.XPATH, password_confirmation_xpath).send_keys(password)

    time.sleep(2)
    driver.find_element(By.XPATH, register_button_xpath).click()
    time.sleep(2)
    driver.find_element(By.XPATH, start_using_button_xpath).click()

    time.sleep(1000)
    driver.quit()


if __name__ == '__main__':
    register_cyanmori_account()
