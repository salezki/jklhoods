import sqlite3 as sql3
from apscheduler.schedulers.blocking import BlockingScheduler	#pip install apscheduler==3.0.0
from datetime import datetime,timedelta
import time
import logging

LIMIT = 400

sched = BlockingScheduler()

@sched.scheduled_job('interval', days=1)
def doCleanUp():
	count1 = getInstagramCount()
	count2 = getTweetsCount()

	if getInstagramCount() > LIMIT:
		deleteOldestInstagram(findInstagramThreshold())
		if getInstagramCount() < count1:
			print "Successfully deleted %d rows from Instagram database" % count1
		
	else:
		print "No deletions were made to instagram database"
	if getTweetsCount() > LIMIT:
		deleteOldestTweets(findTwitterThreshold())
		if getTweetsCount() < count2:
			print "Successfully deleted %d rows from Twitter database" % count2
	else:
		print "No deletions were made to twitter database"
	print('Database deletion process was run')


def getInstagramCount():
	row = None
	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(*) as count FROM instagram_posts")
		row = cur.fetchone()
		con.close()
	except Exception, e:
		con.close()
	return row


def getTweetsCount():
	row = None
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(*) as count FROM twitter_tweets")
		row = cur.fetchone()
		con.close()
	except Exception, e:
		con.close()
	return row


def getTagsCount():
	row = None
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(*) as count FROM twitter_tags")
		row = cur.fetchone()
		con.close()
	except Exception, e:
		con.close()
	return row


#Poistaa vanhimmat tietokannan rivit
def deleteOldestInstagram(week_old_id):
	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("SELECT mediaID FROM instagram_posts WHERE id < ?", (week_old_id,) )
		rows = cur.fetchall()
		tag_deletion = 'DELETE FROM instagram_tags WHERE mediaID IN (' + ','.join(str(r[0]) for r in rows) + ')'
		cur.execute(tag_deletion)

		cur.execute("DELETE FROM instagram_posts WHERE id < ?", (week_old_id,) )
		con.commit()
		con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()


def deleteOldestTweets(week_old_id):
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		
		#tagien poisto
		cur.execute("SELECT tweetID FROM twitter_tweets WHERE id < ?", (week_old_id,) )
		rows = cur.fetchall()
		tag_deletion = 'DELETE FROM twitter_tags WHERE tweetID IN (' + ','.join(str(r[0]) for r in rows) + ')'
		cur.execute(tag_deletion)
		#tweettien poisto
		cur.execute("DELETE FROM twitter_tweets WHERE id < ?", (week_old_id,) )
		con.commit()
		con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()


#etsii tietokannasta ensimmaisen rivin, joka on viikon vanha
def findInstagramThreshold():
	today = datetime.now()
	weekAgo = today - timedelta(days=7)
	month = weekAgo.month
	day = weekAgo.day
	query = '%' + '%02d' % day + '.' + '%02d' % month + '%'


	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("SELECT id FROM instagram_posts WHERE time LIKE ? LIMIT 1", (query,) )
		try:		
			row = cur.fetchone()
			con.close()
			return row[0]
		except:
			print "No 1 week old rows found from instagram database"
			con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()
		return None


def findTwitterThreshold():	
	today = datetime.now()
	weekAgo = today - timedelta(days=7)
	month = weekAgo.month
	day = weekAgo.day
	query = '%' + '%02d' % day + '.' + '%02d' % month + '%'

	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		cur.execute("SELECT id FROM twitter_tweets WHERE time LIKE ? LIMIT 1", (query,) )
		try:		
			row = cur.fetchone()
			con.close()
			return row[0]
		except:
			print "No 1 week old rows found from twitter database"
			con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()
		return None		


sched.start()
