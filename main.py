import os

from dotenv import load_dotenv
from selenium.webdriver.remote.webelement import WebElement

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from read_pdf_file import read_pdf_file
from utils import login, search_user, suspend_user, unsuspend_user

load_dotenv()

dashboard_url = os.environ.get('DASHBOARD_URL')
admin_email = os.environ.get('ADMIN_EMAIL')
admin_password = os.environ.get('ADMIN_PASSWORD')

pdf_url = 'Shuttle bus request (Responses) - Mar-27_23.pdf'


# main function
def main(name_list):
    print('Initializing the headless browser...')
    # create a new Chrome session
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(f'{dashboard_url}/admin?page=users_schedule')

    # login
    print('Logging in...')
    login(driver, admin_email, admin_password)

    # navigate to the users page
    print('Navigating to the users page...')
    driver.find_element(By.XPATH, '//button[text()="Schedule"]').click()

    # loop through inactive users
    # print('Searching for to_be_active users email...')
    active_user_id = []
    for user in name_list['to_be_active']:
        user_email = search_user(driver, user)
        if user_email is not None:
            active_user_id.append(user_email)
    print('Done searching for to_be_active users email')

    # loop through active users
    print('Searching for to_be_inactive users email...')
    inactive_user_id = []
    for user in name_list['to_be_inactive']:
        user_email = search_user(driver, user)
        if user_email is not None:
            inactive_user_id.append(user_email)
    print('Done searching for to_be_inactive users email')

    # navigate to the users page
    print('Navigating to the users page...')
    suspend_user(driver, inactive_user_id, dashboard_url)
    unsuspend_user(driver, active_user_id, dashboard_url)

    # close the browser window
    driver.close()
    # while True:
    #     pass


# call main function
if __name__ == '__main__':

    # read the pdf file
    # TODO: this can convert into an endpoint where the admin can upload the pdf file
    # and will receive the list of users to be active and inactive
    # currently the pdf is locally stored in the same directory
    # but we can change it to be stored in the cloud storage like firebase storage when user upload the pdf file
    # and the server will download the pdf file and read it and delete it from the storage
    print('Reading the pdf file...')
    data = read_pdf_file(pdf_url)

    # TODO: this can be converted into an endpoint where the admin can input the list of users thru params
    # where the admin is already confirmed that the users that are to be active or inactive is correct
    print('Starting the main script...')
    main({
        'to_be_active': ['Nel Sokchhunly'],
        'to_be_inactive': ['Nel Sokchhunly']
    })

