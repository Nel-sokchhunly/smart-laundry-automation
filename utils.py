import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def login(driver: webdriver.Chrome, admin_email: str, admin_password: str):
    driver.find_element(By.ID, 'email').send_keys(admin_email)
    driver.find_element(By.ID, 'password').send_keys(admin_password)
    driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    # wait for the page to load
    driver.implicitly_wait(10)


def search_user(driver: webdriver.Chrome, username: str):
    input_el = driver.find_element(By.XPATH, '//input[@placeholder="Search your name here"]')
    input_el.clear()
    input_el.send_keys(f'{username} {username.split(" ")[1]} {username.split(" ")[0]}')
    input_el.send_keys(Keys.ENTER)

    # wait for the page to load
    driver.implicitly_wait(10)

    # get the first user by data attribute
    try:
        user_el = driver.find_element(By.XPATH, '//tbody/tr[1]')
        email = user_el.get_attribute('data-user-email')

        return email
    except Exception:
        # if the user is not found, return None
        return None


def suspend_user(driver:  webdriver.Chrome, inactive_user_id: list, dashboard_url: str):
    print('Suspending users...')
    for user in inactive_user_id:
        print(f'Suspending {user}...')
        driver.get(f'{dashboard_url}/admin/user/{user}')

        try:
            status_switch = driver.find_element(By.XPATH, '//button[@aria-checked="true"]')

            driver.find_element(By.XPATH, '//button[text()="Edit"]').click()
            status_switch.click()
            driver.find_element(By.XPATH, '//button[text()="Save"]').click()
            time.sleep(1)
        except Exception:
            print(f'{user} is already suspended')
            continue

    print('Done suspending users')


def unsuspend_user(driver:  webdriver.Chrome, active_user_id: list, dashboard_url: str):
    print('Unsuspending users...')
    for user in active_user_id:
        print(f'Unsuspending {user}...')
        driver.get(f'{dashboard_url}/admin/user/{user}')

        try:
            status_switch = driver.find_element(By.XPATH, '//button[@aria-checked="false"]')
            driver.find_element(By.XPATH, '//button[text()="Edit"]').click()
            status_switch.click()
            driver.find_element(By.XPATH, '//button[text()="Save"]').click()
            time.sleep(1)
        except Exception:
            print(f'{user} is already unsuspended')
            continue

    print('Done unsuspending users')