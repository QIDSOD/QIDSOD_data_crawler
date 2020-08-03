import tweepy
import time
import pandas as pd
import datetime
import csv
import numpy as np


consumer_key = 'xxx'
consumer_secret = 'xxx'
access_token = 'xxx'
access_token_secret = 'xxx'
#these keys contain personal information. To get these, please apply for twitter developer account

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


with open('xxx.csv', 'r') as csvfile: #open the file of offical account list
    reader = csv.reader(csvfile)
    name_list = [row[1] for row in reader]
print(len(name_list))
print(name_list)
for s_name in name_list: #iterate 4000 followers of each offical account
    print(s_name)
    user = api.get_user(s_name)
    print(user)
    print(user.location)

    ids = []
    location_list = []
    time_list = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=s_name).pages():
        print(len(page))
        for i in page:
            try:
                user = api.get_user(i)
            except tweepy.error.TweepError:
                print("user not found")
                continue

            if user.location != "":
                ids.append(i)
                location_list.append(user.location)
                try:
                    twitter = api.user_timeline(i)
                    l = len(twitter) - 1
                    if l < 0:
                        time_list.append(0)
                        continue
                    d1 = str(twitter[0].created_at)
                    d2 = str(twitter[l - 1].created_at)
                    d1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
                    d2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
                    delta = d1 - d2
                    time_list.append(delta.days / 20)
                except tweepy.TweepError:
                    print("Failed to run the command on that user, Skipping...")
                    time_list.append(-1)

                if len(ids) % 100 == 0:
                    print(len(ids))

                if len(ids) > 4000:
                    break
                    #dataframe = pd.DataFrame({'user_id': ids, 'location': location_list, "Activity": time_list})
                    #dataframe.to_csv("dataset" + s_name + ".csv", index=False, sep=',')

        print(len(ids))
        if len(ids) > 4000:
            break
    dataframe = pd.DataFrame({'user_id': ids, 'location': location_list, "Activity": time_list})
    dataframe.to_csv("dataset" + s_name + ".csv", index=False, sep=',')
