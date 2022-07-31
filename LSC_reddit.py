#!/usr/bin/python3

import os
import json
import praw

output_dir = '/home/pi/docker/homeassistant/api_calls/'
submission_count = 20

def redditConnect():
    try:
#Client ID, secret, and user agent values that are be passed into the API. The credentials are stored as environment variables on my own device.
        connection = praw.Reddit(
            client_id = os.environ.get('REDDIT_CLIENT_ID'),
            client_secret = os.environ.get('REDDIT_CLIENT_SECRET'),
            user_agent = os.environ.get('REDDIT_USER_AGENT') )
    except ConnectionError as err:
        print(err)

    return connection

def createDictKeys():

    keys = []
    
    for num in range(0,submission_count):
        keys.append(num)

    return keys

def getPosts(reddit):
    
    dict_keys = createDictKeys()
    json_data = dict.fromkeys(dict_keys)
    posts = {'posts': ''}
    with open('LSC_Group_Data.json', 'w') as file:
        for count,submission in enumerate(reddit.subreddit("LondonSocialClub").hot(limit=submission_count)):
            values_for_json = []
            values_for_json.append({'title':submission.title, 'shortlink':submission.shortlink, 'ratio':submission.upvote_ratio})
            json_data[count] = values_for_json

        posts['posts']= json_data
        json.dump(posts, file, ensure_ascii=False, indent=4)


def main():
    reddit = redditConnect()
    getPosts(reddit)


main()