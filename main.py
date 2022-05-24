import tweepy
import configparser
import re
import requests
import urlexpander as ue
import sqlite3
import time
import os

class1 = ('contents-3ca1mk')
xpath1 = ('/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input')
xpath2 = ('/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input')
xpath3 = ('/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]')
username = input("Enter username: ")
timer = float(input("Enter time between requests (in seconds): "))
time.sleep(0.5)
os.system('cls')
print('Script is running')

# Config
config = configparser.ConfigParser()
config.read("config.ini")
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Authorization
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Browser
browser = uc.Chrome(use_subprocess=True)
browser.get('https://discord.com/login')
time.sleep(10)
wait = WebDriverWait(browser, 15)

# Getting tweets
user = username
limit = 5


# Creating database
db = sqlite3.connect('invitelinks.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS tweets (
    user TEXT,
    link TEXT
)""")
db.commit()

# Cycle
while True:
    result = None
    if result is None:
        result = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')
        time.sleep(timer)
        print('Waiting for link')
    for tweet in result:
        url_pattern = r'http(?:s)?://\S+'  # Finding link in tweet
        urls = re.findall(url_pattern, tweet.full_text)
        link = ue.expand(urls)
        linkds = "".join(link)
        if "discord" in linkds:
            sql.execute(f"SELECT link FROM tweets WHERE link = '{linkds}'")
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO tweets VALUES (?, ?)", (tweet.user.screen_name, linkds))
                db.commit()
                browser.get(linkds)
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'contents-3ca1mk')))
                browser.find_element_by_class_name(class1).click()
                print('Success')
            else:
                None
        else:
            None
