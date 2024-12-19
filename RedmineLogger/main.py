from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import time
import datetime as dt

chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")
driver = webdriver.Chrome(chrome_options)
redmine_login_url = ''
redmine_new_working_day_entry_url = ''
redmine_new_holiday_entry_url = ''


def start():
    driver.get(redmine_login_url)

    login()

    start_date = assemble_date(input('The first day you want to log (format: yyyyMMdd): '))

    duration = input('How many days do you want to log? ')

    end_date = start_date + dt.timedelta(days=int(duration) - 1)

    print("So you want to log {} days started from {} to {}?".format(duration, start_date, end_date))

    logged_days_type = input('Log working days (w) or holidays (h)? ')

    confirmation = input('Are you sure (y/n)? ')

    if confirmation == 'y':
        if logged_days_type == 'w':
            log_working_days(start_date, duration)
        else:
            log_holidays(start_date, duration)
    else:
        print('Exiting')
        SystemExit()


def assemble_date(first_date):
    y = int(first_date[:4])
    m = int(first_date[4:6])
    d = int(first_date[6:])
    return dt.date(year=y, month=m, day=d)


def login():
    username = input('Enter your username: ')
    password = getpass(prompt='and your password: ')

    print('Entering the user info...')

    user_field = driver.find_element(By.XPATH, '//*[@id="username"]')
    user_field.send_keys(username)
    pw_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    pw_field.send_keys(password)
    login_but = driver.find_element(By.XPATH, '//*[@id="login-submit"]')
    login_but.send_keys(Keys.RETURN)


def log_working_days(start_date, duration):
    for i in range(int(duration)):

        driver.get(redmine_new_working_day_entry_url)
        entered_date = start_date + dt.timedelta(days=i)

        if entered_date.weekday() == 5 or entered_date.weekday() == 6:

            print('{} is weekend, Pass'.format(entered_date))

        else:

            print('Entered date -> {}'.format(entered_date))

            date_box = driver.find_element(By.XPATH, '//*[@id="time_entry_spent_on"]')
            date_box.clear()
            date_box.send_keys(str(entered_date.strftime('%Y')))
            date_box.send_keys(Keys.TAB)
            date_box.send_keys(str(entered_date.strftime('%m')))
            date_box.send_keys(str(entered_date.strftime('%d')))

            driver.find_element(By.XPATH, '//*[@id="time_entry_hours"]').send_keys('8')

            driver.find_element(By.XPATH, '//*[@id="time_entry_comments"]').send_keys('fejlesztés')

            Select(driver.find_element(By.XPATH, '//*[@id="time_entry_activity_id"]')).select_by_visible_text(
                'Development')

            driver.find_element(By.XPATH, '//*[@id="new_time_entry"]/input[3]').send_keys(Keys.ENTER)

            print('Completed logging day {}/{}'.format(i + 1, duration))

            time.sleep(2)

        print('---------------------------------------')

    print('Logging time completed')


def log_holidays(start_date, duration):
    for i in range(int(duration)):

        driver.get(redmine_new_holiday_entry_url)
        entered_date = start_date + dt.timedelta(days=i)

        if entered_date.weekday() == 5 or entered_date.weekday() == 6:

            print('{} is weekend, Pass'.format(entered_date))

        else:

            print('Entered date -> {}'.format(entered_date))

            date_box = driver.find_element(By.XPATH, '//*[@id="time_entry_spent_on"]')
            date_box.clear()
            date_box.send_keys(str(entered_date.strftime('%Y')))
            date_box.send_keys(Keys.TAB)
            date_box.send_keys(str(entered_date.strftime('%m')))
            date_box.send_keys(str(entered_date.strftime('%d')))

            driver.find_element(By.XPATH, '//*[@id="time_entry_hours"]').send_keys('8')

            driver.find_element(By.XPATH, '//*[@id="time_entry_comments"]').send_keys('szabadság')

            Select(driver.find_element(By.XPATH, '//*[@id="time_entry_activity_id"]')).select_by_visible_text(
                'Administration')

            driver.find_element(By.XPATH, '//*[@id="new_time_entry"]/input[3]').send_keys(Keys.ENTER)

            print('Completed logging day {}/{}'.format(i + 1, duration))

            time.sleep(2)

        print('---------------------------------------')

    print('Logging time completed')


start()
