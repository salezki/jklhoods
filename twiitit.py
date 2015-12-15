import sqlite3 as lite
import os
import psycopg2
import urlparse
import sys
from flask import jsonify

def twiits():
	con = None

	try:
		#con = lite.connect('tweets.db')

		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)


		tweets = []
		cur = con.cursor()
		cur.execute('SELECT tweetID FROM twitter_tweets ORDER BY id DESC LIMIT 10')
		#filterointia varten
		#cur.execute('SELECT tweet.id FROM twitter_tweets tweet INNER JOIN twitter_tags tag ON tweet.id = tag.id')
		rows = cur.fetchall()
		for row in rows:
			tweets.append([str(row[0])])
		return jsonify(result=tweets)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

def hae_tagilla(req):
	con = None
	tagi = req["tagi"]

	try:
		con = lite.connect('tweets.db')

		tweets = []
		cur = con.cursor()
		cur.execute('SELECT twitter_tweets.tweetID FROM twitter_tweets, twitter_tags WHERE twitter_tweets.tweetID = twitter_tags.tweetID AND twitter_tags.hashtag LIKE ? ORDER BY id DESC LIMIT 10', (str(tagi), ))
		rows = cur.fetchall()
		for row in rows:
			tweets.append([str(row[0])])
		return jsonify(result=tweets)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

def haes_tagilla(req):
	con = None
	tagi = req["tagi"]
	tweetId = req["tweetId"]

	try:
		con = lite.connect('tweets.db')

		tweets = []
		cur = con.cursor()
		cur.execute('SELECT twitter_tweets.tweetID FROM twitter_tweets, twitter_tags WHERE twitter_tweets.tweetID = twitter_tags.tweetID AND twitter_tags.hashtag LIKE ? AND twitter_tweets.tweetID < ? ORDER BY id DESC LIMIT 10', (str(tagi),tweetId))
		rows = cur.fetchall()
		for row in rows:
			tweets.append([str(row[0])])
		return jsonify(result=tweets)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

def fetchTweets(tweetId):
	con = None
	try:
		con = lite.connect('tweets.db')
		data_tweet = []
		cur = con.cursor()
		cur.execute('SELECT tweetID FROM twitter_tweets WHERE tweetID > ?', (tweetId,))
		rows = cur.fetchall()
		for row in rows:
			data_tweet.append([str(row[0])])
		return jsonify(result=data_tweet)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

def fetchTagTweets(req):
	con = None
	tagi = req["tagi"]
	tweetId = req["tweetId"]
	try:
		con = lite.connect('tweets.db')
		data_tweet = []
		cur = con.cursor()
		cur.execute('SELECT twitter_tweets.tweetID FROM twitter_tweets, twitter_tags WHERE twitter_tweets.tweetID = twitter_tags.tweetID AND twitter_tags.hashtag LIKE ? AND twitter_tweets.tweetID > ? ORDER BY id DESC LIMIT 10', (str(tagi), str(tweetId)) )
		rows = cur.fetchall()
		for row in rows:
			data_tweet.append([str(row[0])])
		return jsonify(result=data_tweet)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

def haeSeuraavat(tweetId):
	con = None
	try:
		con = lite.connect('tweets.db')
		data_tweet = []
		cur = con.cursor()
		cur.execute('SELECT tweetID FROM twitter_tweets WHERE tweetID < ? LIMIT 10', (tweetId,))
		rows = cur.fetchall()
		for row in rows:
			data_tweet.append([str(row[0])])
		return jsonify(result=data_tweet)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()