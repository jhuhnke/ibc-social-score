import requests
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

## Import Twitter API Keys From .env file 
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

## Twitter OAuth2
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

## Function To Get Followers
def get_followers(user_name):
    api = tweepy.API(auth)
    followers = []
    for page in tweepy.Cursor(api.get_followers, screen_name=user_name, count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(10)
        return followers
    
## Save Followers to .csv
def save_followers_to_csv(user_name, data):
    HEADERS = ["name", "screen_name", "description", "followers_count", "followers_count",
               'friends_count', "listed_count", "favourites_count", "created_at"]
    with open(user_name + "_followers.csv", 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(HEADERS)
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
            csv_writer.writerow(profile)

## Main Accounts - Broken Up To Prevent Rate Limiting
accounts = ["Cryptocito", "youssef_amrani"] 
accounts1= ["gregosuri", "sunnya97", "zmanian"] 
accounts2 = ["jackzampolin", "JoeAbbey", "buchmanster"]

## Get followers and save to csv
for i in range(len(accounts)):
    followers = get_followers(accounts[i])
    save_followers_to_csv(accounts[i], followers)
