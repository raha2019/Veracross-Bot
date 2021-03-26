# To do
# - Create a progress bar?

import time
import os
import discord

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from datetime import date, timedelta

chrome_driver = os.path.abspath("chromedriver")

def get_homework(username, password, num_days):

    url = 'https://accounts.veracross.com/austinprep/portals/login'


    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_driver, options=chrome_options) 
    driver.get(url)
    driver.find_element_by_id('username').send_keys(str(username))
    driver.find_element_by_id('password').send_keys(str(password))
    driver.find_element_by_id('recaptcha').click()

    driver.get("https://portals.veracross.com/austinprep/student/student/upcoming-assignments")
    
    
    current_date = (date.today() + timedelta(days=num_days)).strftime("%Y-%m-%d")
    embed=discord.Embed(title=current_date + " - " + str(num_days) + " Day(s) Remaining")
    embed.set_author(name="Veracross Bot", url="https://github.com/raha2019/Veracross-Bot", icon_url="https://pbs.twimg.com/profile_images/1323667180299440128/INS15fm1.jpg")
        
    try: 
        current_link = "https://portals.veracross.com/austinprep/student/student/daily-schedule?date=" + current_date
        driver.get(current_link)
        
        classes = []
        for elem in driver.find_elements_by_xpath('.//span[@class = "item-main-description"]'): # Gets the class name
            classes.append(elem.text)
        try:
            for i in range(0,2): # Removes Extra Advisory and Break
                classes.pop(3)
            classes.pop(4) # Removes Cougar Block
        except IndexError:
            pass
        x = 0
        for i in driver.find_elements_by_class_name("assignments"):  
            text = i.text
            if not text:
                text = "Nothing"
            embed.add_field(name=classes[x], value=text, inline=True)
            x += 1
    except NoSuchElementException:
        pass
    time.sleep(1)

    driver.close()
    return embed


def check_credentials_exist(discord_id):
    data = pd.read_csv("data.csv", index_col='discord_id')
    if discord_id in data.index:
        return True
    return False

def update_creds(discord_id, email, password):
    data = pd.read_csv("data.csv", index_col='discord_id', converters={i : str for i in range(100)}) # Change range if there are more than 100 rows
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
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_driver, options=chrome_options) 
    driver.get(url)
    driver.find_element_by_id('username').send_keys(str(username))
    driver.find_element_by_id('password').send_keys(str(password))
    driver.find_element_by_id('recaptcha').click() #vx-MessageBanner warning
    if driver.find_elements_by_class_name("vx-MessageBanner"):
        driver.close()
        return False
    driver.close()
    return True

