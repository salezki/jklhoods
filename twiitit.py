import sqlite3 as lite
import os
import psycopg2
import urlparse
import sys
from flask import jsonify
import urllib

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ['DATABASE_URL'])
con = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)


def twiits():
	try:
		#con = lite.connect('tweets.db')

		tweets = []
		cur = con.cursor()
		cur.execute('SELECT tweetID FROM twitter_tweets ORDER BY id DESC LIMIT 10')
		#filterointia varten
		#cur.execute('SELECT tweet.id FROM twitter_tweets tweet INNER JOIN twitter_tags tag ON tweet.id = tag.id')
		rows = cur.fetchall()
		for row in rows:
			tweets.append([str(row[0])])
		return jsonify(result=tweets)
	except e:
		print e
		sys.exit(1)


def hae_tagilla(req):
	tagi_encoded = req["tagi"]
	tagi = urllib.unquote(str(tagi_encoded));
	print tagi_encoded
	print tagi.encode('utf-8')
	try:
		tweets = []
		cur = con.cursor()
		cur.execute('SELECT twitter_tweets.tweetid FROM twitter_tweets, twitter_tags WHERE twitter_tweets.tweetid = twitter_tags.tweetid AND twitter_tags.hashtag LIKE %s ORDER BY id DESC LIMIT 10', (tagi)), )
		rows = cur.fetchall()
		for row in rows:
			tweets.append([str(row[0])])
		return jsonify(result=tweets)
	except Exception, e:
		print e
		sys.exit(1)

def haes_tagilla(req):
	tagi = req["tagi"]
	tweetId = req["tweetId"]
	try:
		tweets = []
		cur = con.cursor()
		cur.execute('SELECT twitter_tweets.tweetID FROM twitter_tweets, twitter_tags WHERE twitter_tweets.tweetID = twitter_tags.tweetID AND twitter_tags.hashtag LIKE %s AND twitter_tweets.tweetID < %s ORDER BY id DESC LIMIT 10', (str(tagi),tweetId))
		rows = cur.fetchall()
		for row in rows:
			tweets.append([str(row[0])])
		return jsonify(result=tweets)
	except Exception, e:
		print e
		sys.exit(1)

def fetchTweets(tweetId):
	try:
		data_tweet = []
		cur = con.cursor()
		cur.execute('SELECT tweetID FROM twitter_tweets WHERE tweetID > %s', (tweetId,))
		rows = cur.fetchall()
		for row in rows:
			data_tweet.append([str(row[0])])
		return jsonify(result=data_tweet)
	except Exception, e:
		print e
		sys.exit(1)

def fetchTagTweets(req):
	tagi = req["tagi"]
	tweetId = req["tweetId"]
	try:
		data_tweet = []
		cur = con.cursor()
		cur.execute('SELECT twitter_tweets.tweetID FROM twitter_tweets, twitter_tags WHERE twitter_tweets.tweetID = twitter_tags.tweetID AND twitter_tags.hashtag LIKE %s AND twitter_tweets.tweetID > %s ORDER BY id DESC LIMIT 10', (str(tagi), str(tweetId)) )
		rows = cur.fetchall()
		for row in rows:
			data_tweet.append([str(row[0])])
		return jsonify(result=data_tweet)
	except Exception, e:
		print e
		sys.exit(1)

def haeSeuraavat(tweetId):
	try:
		data_tweet = []
		cur = con.cursor()
		cur.execute('SELECT tweetID FROM twitter_tweets WHERE tweetID < %s ORDER BY id DESC LIMIT 10', (tweetId,))
		rows = cur.fetchall()
		for row in rows:
			data_tweet.append([str(row[0])])
		return jsonify(result=data_tweet)
	except Exception, e:
		print e
		sys.exit(1)
