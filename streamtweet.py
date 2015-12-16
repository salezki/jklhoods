# -*- coding: UTF-8 -*-
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sqlite3 as sql3
import os
import psycopg2
import urlparse
import time
import json
import time
from datetime import datetime
import os
import sys

#consumer key, consumer secret, access token, access secret.
ckey= os.environ.get('TWITTER_CKEY')
csecret= os.environ.get('TWITTER_CSECRET')
atoken= os.environ.get('TWITTER_TOKEN')
asecret= os.environ.get('TWITTER_SECRET')

new = 0
tags = [u"#jyväskylä", u"#jyvaskyla"]

#con = sql3.connect("tweets.db")

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ['DATABASE_URL'])
con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = con.cursor()


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)   
        id = str(all_data["id_str"])
        timestamp = time.strftime('%Y.%m.%d %H:%M', time.strptime(all_data["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
        name = all_data["user"]["name"]
        screen_name = all_data["user"]["screen_name"]
        tagit = all_data["entities"]["hashtags"]
        cur.execute("SELECT tweetID FROM twitter_tweets WHERE tweetID LIKE %s", (str(id),) )
        row = cur.fetchone()
        print row
        if row:
            return False
        cur.execute("INSERT INTO twitter_tweets (tweetID, time, username, screen_name) VALUES (%s, %s, %s, %s)",
            (id, timestamp, name, screen_name))

        for text in tagit:
        	cur.execute("INSERT INTO twitter_tags (tweetID, hashtag) VALUES (%s, %s)",
        		(id, text["text"]))

        con.commit()
        print((id ,screen_name))
        return True


    def on_error(self, status):
    	if status == 420:
            print "testi"
        print status


def runStream():
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, Listener())
    twitterStream.filter(track=tags)
