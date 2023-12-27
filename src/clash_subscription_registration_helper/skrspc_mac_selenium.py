import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from util import get_username, get_email, get_password


def register_skrspc_account():
    link = 'https://board.skrspc.com/#/register?code=r6GgcRIK'
    email_xpath = '/html/body/div/div/main/div[2]/div/div/div/div[1]/div/div/div[2]/div[1]/input'
    password_xpath = '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/input'
    password_confirmation_xpath = '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/div[3]/input'

    register_button_xpath = '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/div[5]/button'

    driver = webdriver.Chrome()
    driver.get(link)

    username, email, password = get_username(), get_email(), get_password()

    info = 'link: %s username: %s email: %s password: %s\n' % (link, username, email, password)
    print(info)
    f = open('./registration_result.txt', 'a')
    f.write(info)
    f.close()

    time.sleep(1)
    driver.find_element(By.XPATH, email_xpath).send_keys(email)
    time.sleep(0.2)
    driver.find_element(By.XPATH, password_xpath).send_keys(password)
    time.sleep(0.2)
    driver.find_element(By.XPATH, password_confirmation_xpath).send_keys(password)

    time.sleep(2)
    driver.find_element(By.XPATH, register_button_xpath).click()

    time.sleep(2)
    email_xpath = '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[2]/input'
    driver.find_element(By.XPATH, email_xpath).send_keys(email)

    time.sleep(2)
    password_xpath = '//*[@id="main-container"]/div[2]/div/div/div/div[1]/div/div/div[3]/input'
    driver.find_element(By.XPATH, password_xpath).send_keys(password)

    time.sleep(1000)
    driver.quit()


if __name__ == '__main__':
    register_skrspc_account()
