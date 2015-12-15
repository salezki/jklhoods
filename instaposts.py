import sqlite3 as lite
import os
import psycopg2
import urlparse
import sys
from flask import jsonify

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ['DATABASE_URL'])
con = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)

# Hae ensimmaista kertaa postit
def instagramPosts():
	try:

		data = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts ORDER BY id DESC LIMIT 10')
		rows = cur.fetchall()
		for row in rows:
			if row:
				data.append([row[0]])
			else:
				continue
		return jsonify(result=data)
	except e:
		print e
		sys.exit(1)
			
			
# Hakee uusimmat postit
def fetchInstagram(shortcode):
	try:
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id > (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s)', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except e:
		print e
		sys.exit(1)

		
# Hakee uusimmat postit tagilla
def fetchTagInstagram(req):
	tagi = req["tagi"]
	shortcode = req["shortcode"]
	try:
		posts = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaID = instagram_tags.mediaID AND instagram_tags.hashtag LIKE %s AND id > (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s) ORDER BY id DESC LIMIT 10', (str(tagi), str(shortcode) ))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except e:
		print e
		sys.exit(1)

		
# Hakee vanhempia posteja
def fetchNext(shortcode):
	try:
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id < (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s) ORDER BY id DESC LIMIT 10', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except e:
		print e
		sys.exit(1)

		
# Hae ensimmaista kertaa tagilla
def hae_tagilla(req):
	tagi = req["tagi"]

	try:
		post = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaID = instagram_tags.mediaID AND instagram_tags.hashtag LIKE %s ORDER BY id DESC LIMIT 10', (str(tagi), ))
		rows = cur.fetchall()
		for row in rows:
			post.append([str(row[0])])
		return jsonify(result=post)
	except e:
		print e
		sys.exit(1)

		
def haes_tagilla(req):
	tagi = req["tagi"]
	shortcode = req["instacode"]
	try:
		posts = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaID = instagram_tags.mediaID AND instagram_tags.hashtag LIKE %s AND id < (SELECT id FROM instagram_posts WHERE shortcode LIKE  %s) ORDER BY id DESC LIMIT 10', (str(tagi), str(shortcode) ))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except e:
		print e
		sys.exit(1)
