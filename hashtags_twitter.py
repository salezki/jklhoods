#!/usr/bin/python
import sqlite3 as lite
import sys
from flask import jsonify

def tagit_twitter():
	con = None
	try:
		con = lite.connect('tweets.db')

		top_hashtags = []
		cur = con.cursor()
		cur.execute('SELECT hashtag, COUNT(*) FROM twitter_tags GROUP BY hashtag ORDER BY 2 DESC LIMIT 6')
		#filterointia varten
		#cur.execute('SELECT tweet.id FROM twitter_tweets tweet INNER JOIN twitter_tags tag ON tweet.id = tag.id')
		rows = cur.fetchall()
		for row in rows:
			top_hashtags.append([row[0]])
		return jsonify(result=top_hashtags)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

#juu = tagit_twitter()
#return jsonify(result=juu)
