from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sqlite3 as sql3
import time
import json
import time
from datetime import datetime
import os
#import sys

#consumer key, consumer secret, access token, access secret.

ckey= os.environ.get('TWITTER_CKEY')
csecret= os.environ.get('TWITTER_CSECRET')
atoken= os.environ.get('TWITTER_TOKEN')
asecret= os.environ.get('TWITTER_SECRET')

new = 0

con = sql3.connect("tweets.db")

cur = con.cursor()


def newTweets():
    if new == 0:
        return
    

class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        id = all_data["id_str"]
        timestamp = time.strftime('%Y.%m.%d %H:%M', time.strptime(all_data["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
        name = all_data["user"]["name"]
        screen_name = all_data["user"]["screen_name"]
        tagit = all_data["entities"]["hashtags"]

        cur.execute("INSERT INTO twitter_tweets (tweetID, time, username, screen_name) VALUES (?, ?, ?, ?)",
            (id, timestamp, name, screen_name))

        for text in tagit:
        	cur.execute("INSERT INTO twitter_tags (tweetID, hashtag) VALUES (?, ?)",
        		(id, text["text"]))
		

        con.commit()

        print((id ,screen_name))
        return True


    def on_error(self, status):
    	if status == 420:
    		#returning False in on_data disconnects the stream
    		return False
        print status


def runStream():
    print ckey
    print csecret
    print atoken
    print asecret
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, Listener())
    twitterStream.filter(track=["#jyvaeskylae"])


if __name__ == '__main__':
    runStream()
