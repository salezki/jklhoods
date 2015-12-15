import sqlite3 as lite
import os
import psycopg2
import urlparse
import sys
from flask import jsonify

# Hae ensimmaista kertaa postit
def instagramPosts():
	con = None
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
				continue
		return jsonify(result=data)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()
			
# Hakee uusimmat postit
def fetchInstagram(shortcode):
	con = None
	try:
		con = lite.connect('instagram.db')
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id > (SELECT id FROM instagram_posts WHERE shortcode LIKE  ?)', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

# Hakee uusimmat postit tagilla
def fetchTagInstagram(req):
	con = None
	tagi = req["tagi"]
	shortcode = req["shortcode"]
	try:
		con = lite.connect('instagram.db')
		posts = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaID = instagram_tags.mediaID AND instagram_tags.hashtag LIKE ? AND id > (SELECT id FROM instagram_posts WHERE shortcode LIKE  ?) ORDER BY id DESC LIMIT 10', (str(tagi), str(shortcode) ))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

# Hakee vanhempia posteja
def fetchNext(shortcode):
	con = None
	try:
		con = lite.connect('instagram.db')
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id < (SELECT id FROM instagram_posts WHERE shortcode LIKE  ?) ORDER BY id DESC LIMIT 10', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

# Hae ensimmaista kertaa tagilla
def hae_tagilla(req):
	con = None
	tagi = req["tagi"]

	try:
		con = lite.connect('instagram.db')
		post = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaID = instagram_tags.mediaID AND instagram_tags.hashtag LIKE ? ORDER BY id DESC LIMIT 10', (str(tagi), ))
		rows = cur.fetchall()
		for row in rows:
			post.append([str(row[0])])
		return jsonify(result=post)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

def haes_tagilla(req):
	print req
	con = None
	tagi = req["tagi"]
	shortcode = req["instacode"]
	try:
		con = lite.connect('instagram.db')
		posts = []
		cur = con.cursor()
		cur.execute('SELECT instagram_posts.shortcode FROM instagram_posts, instagram_tags WHERE instagram_posts.mediaID = instagram_tags.mediaID AND instagram_tags.hashtag LIKE ? AND id < (SELECT id FROM instagram_posts WHERE shortcode LIKE  ?) ORDER BY id DESC LIMIT 10', (str(tagi), str(shortcode) ))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()