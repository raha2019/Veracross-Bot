# To do
# - Check Credentials otherwise
# Create a progress bar?


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from datetime import date, timedelta



def get_homework(username, password):

    url = 'https://accounts.veracross.com/austinprep/portals/login'


    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome('/Users/rahulgupta/Desktop/chromedriver', options=chrome_options) # Change to be dynamic?
    driver.get(url)
    driver.find_element_by_id('username').send_keys(str(username))
    driver.find_element_by_id('password').send_keys(str(password))
    driver.find_element_by_id('recaptcha').click()

    driver.get("https://portals.veracross.com/austinprep/student/student/upcoming-assignments")
    # print(driver.title)


    # message = "```"
    message = ""
    for i in range(0, 7):
        current_date = (date.today() + timedelta(days=i)).strftime("%Y-%m-%d")
        message += '\n**' + current_date + '**'
        try: 
            current_link = "https://portals.veracross.com/austinprep/student/student/daily-schedule?date=" + current_date
            driver.get(current_link)
            time.sleep(5) # maybe change?
            
            classes = []
            for elem in driver.find_elements_by_xpath('.//span[@class = "item-main-description"]'): # Gets the class name
                classes.append(elem.text)
            try:
                for i in range(0,2): # Removes Extra Advisory and Break
                    classes.pop(3)
                classes.pop(4) # Removes Cougar Block
            except IndexError:
                message += "\n There is no homework on this day"
            
            x = 0
            for i in driver.find_elements_by_class_name("assignments"):    
                message += '\n' + classes[x] 
                message += '\n' + i.text + '\n'
                x += 1
        except NoSuchElementException:
            message += "\n There is no homework on this day"
        message += "\n"
    time.sleep(1)

    driver.close()

    # message += '```'
    return message

# print(get_homework('rahul.gupta@austinprep.org', 'R@h@2213'))


def check_credentials_exist(discord_id):
    data = pd.read_csv("data.csv", index_col='discord_id')
    if discord_id in data.index:
        return True
    return False

def update_creds(discord_id, email, password):
    data = pd.read_csv("data.csv", index_col='discord_id')
    if not discord_id in data.index:
        data.loc[discord_id] = [email, password]
    else:
        data.at[discord_id, 'email'] = email
        data.at[discord_id, 'password'] = password
    data.to_csv("data.csv")

def get_creds(discord_id):
    data = pd.read_csv("data.csv", index_col='discord_id')
    return str(data.loc[discord_id, 'email']), str(data.loc[discord_id, 'password'])

def check_valid_credentials(discord_id):
    # Check if it logs into veracross
    username, password = get_creds(discord_id)
    url = 'https://accounts.veracross.com/austinprep/portals/login'


    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome('/Users/rahulgupta/Desktop/chromedriver', options=chrome_options) # Change to be dynamic?
    driver.get(url)
    driver.find_element_by_id('username').send_keys(str(username))
    driver.find_element_by_id('password').send_keys(str(password))
    driver.find_element_by_id('recaptcha').click() #vx-MessageBanner warning
    if driver.find_elements_by_class_name("vx-MessageBanner"):
        driver.close()
        return False
    driver.close()
    return True

    # driver.get("https://portals.veracross.com/austinprep/student/student/upcoming-assignments")

