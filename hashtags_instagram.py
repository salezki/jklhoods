#!/usr/bin/python
import sqlite3 as lite
import os
import psycopg2
import urlparse
import sys
from flask import jsonify

def tagit_instagram():
	con = None
	try:
		#con = lite.connect('instagram.db')
		#url = urlparse.urlparse(os.environ['DATABASE_URL'])

		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)

		top_hashtags = []
		cur = con.cursor()
		cur.execute('SELECT hashtag, COUNT(*) FROM instagram_tags GROUP BY hashtag ORDER BY 2 DESC LIMIT 7')
		#filterointia varten
		#cur.execute('SELECT tweet.id FROM twitter_tweets tweet INNER JOIN twitter_tags tag ON tweet.id = tag.id')
		rows = cur.fetchall()
		rows = rows[2:]
		for row in rows:
			top_hashtags.append([row[0]])
		return jsonify(result=top_hashtags)
	except Exception, e:
		print e
		sys.exit(1)
	finally:
		if con:
			con.close()

#juu = tagit_twitter()
#return jsonify(result=juu)
