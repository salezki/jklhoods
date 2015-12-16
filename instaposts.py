import sqlite3 as lite
import os
import psycopg2
import urlparse
import sys
from flask import jsonify
import urllib


# Hae ensimmaista kertaa postit
def instagramPosts():
	try:
		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		data = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts ORDER BY id DESC LIMIT 10')
		rows = cur.fetchall()
		for row in rows:
			if row:
				data.append([row[0]])
			else:
				con.close()
				continue
		return jsonify(result=data)
	except Exception, e:
		print e
		con.close()
		sys.exit(1)
			
		
# Hakee uusimmat postit
def fetchInstagram(shortcode):
	try:
		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id > (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s)', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		con.close()
		return jsonify(result=posts)
	except e:
		print e
		con.close()
		sys.exit(1)

		
# Hakee uusimmat postit tagilla
def fetchTagInstagram(req):
	tagi = req["tagi"]
	shortcode = req["shortcode"]
	try:
		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		posts = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaid = instagram_tags.mediaid AND instagram_tags.hashtag LIKE %s AND id > (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s) ORDER BY id DESC LIMIT 10', (str(tagi), str(shortcode) ))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		con.close()
		return jsonify(result=posts)
	except e:
		print e
		con.close()
		sys.exit(1)

		
# Hakee vanhempia posteja
def fetchNext(shortcode):
	try:
		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id < (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s) ORDER BY id DESC LIMIT 10', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		con.close()
		return jsonify(result=posts)
	except e:
		print e
		con.close()
		sys.exit(1)

		
# Hae ensimmaista kertaa tagilla
def hae_tagilla(req):
	tagi = req["tagi"]
	try:
		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		post = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaid = instagram_tags.mediaid AND instagram_tags.hashtag LIKE %s ORDER BY id DESC LIMIT 10', (str(tagi), ))
		rows = cur.fetchall()
		for row in rows:
			post.append([str(row[0])])
		con.close()
		return jsonify(result=post)
	except Exception, e:
		print e
		con.close()
		sys.exit(1)

		
def haes_tagilla(req):
	tagi = req["tagi"]
	shortcode = req["instacode"]
	try:
		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ['DATABASE_URL'])
		con = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		posts = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaid = instagram_tags.mediaid AND instagram_tags.hashtag LIKE %s AND id < (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s) ORDER BY id DESC LIMIT 10', (str(tagi), str(shortcode) ))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		con.close()
		return jsonify(result=posts)
	except Exception, e:
		print e
		con.close()
		sys.exit(1)
