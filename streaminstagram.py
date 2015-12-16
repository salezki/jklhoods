#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,request, Response,redirect,url_for
from instagram import client, subscriptions
from twisted.internet import reactor
import json
import sys, logging
import time
import multiprocessing
import sqlite3 as sql3
import os
import psycopg2
import urlparse
from datetime import datetime
import os

CLIENT_ID= os.environ.get('INST_CLIENTID')
CLIENT_SECRET= os.environ.get('INST_SECRET')
ACCESS_TOKEN= os.environ.get('INST_TOKEN') 

COUNT = 1
CALLBACK_HEROKU = 'https://jklhoods.herokuapp.com/realtime'
#CALLBACK_LOCAL = 'http://localhost:5000/oauth_callback'
#CALLBACK_TUNNEL = 'https://nzmpqlpmhe.localtunnel.me/realtime' #lt --port 8000 --subdomain nzmpqlpmhe

tag = 'jyväskylä'
subID = 0
reactor = None


def subscribeToTag(topic):
	r = api.create_subscription(object = 'tag',
	object_id = topic,
	aspect = 'media',
	callback_url = CALLBACK_HEROKU,
	client_id = CLIENT_ID,
	client_secret = CLIENT_SECRET)
 	global subID
 	subID = r['data']['id']


#hakee uuden paivityksen ja paivittaa sen tietokantaan
def fetchNewUpdate(amount=1):
	global tag
	print 'uusi instagram posti'
	tagged_media, next_ = api.tag_recent_media(tag_name=tag, count=amount)
	for media in tagged_media:
		id = media.id
		user = media.user.username
		userID = media.user.id
		comment = media.caption
		timestamp = media.created_time
		media_link = media.link #linkki paivitykseen
		shortcode = media_link.split("/")[4]
		if (savetoDataBase(id,userID,user,timestamp,shortcode)):
			print 'yksi instagram media tallennettu'
			saveInstagramTags(id,str(comment))
		return True


def savetoDataBase(id,userID,user,timestamp,shortcode):
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
		cur = con.cursor()
		cur.execute("SELECT shortcode FROM instagram_posts WHERE shortcode LIKE %s", (str(shortcode),))
		row = cur.fetchone()
		if row:
			return False
		cur.execute("INSERT INTO instagram_posts (mediaid, userid, username, time, shortcode) VALUES (%s, %s, %s, %s, %s)",
			(str(id), str(userID), str(user), str(timestamp.strftime("%d.%m.%Y %H:%M")), str(shortcode)))
		con.commit()
		con.close()
	except Exception, e:
		print "errori" 
		print e
		if con:
			con.close()
		return False
	return True


def saveInstagramTags(id,caption):
	tags = hashtaglist(caption)
	print tags
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
		print 'vaihe 1'
		#con.text_factory = str
		cur = con.cursor()
		for tag in tags:
			cur.execute("INSERT INTO instagram_tags (mediaid, hashtag) VALUES (%s, %s)", (id, tag))
		print 'vaihe 2'
		con.commit()
		con.close()
	except Exception, e:
		print e
		if con:
			con.close()


# http://stackoverflow.com/questions/6331497/an-elegant-way-to-get-hashtags-out-of-a-string-in-python
def hashtaglist(string):
    lst = []
    s=''
    hashtag = False
    for char in string:
        if char=='#':
            hashtag = True
            if s:
                lst.append(s)
                s=''           
            continue

        if hashtag and char in [' ','.',',','(',')',':','{','}'] and s:
            lst.append(s)
            s=''
            hashtag=False 
        if hashtag:
            s+=char

    if s:
        lst.append(s)

    return set(lst)


def callback(): 
	global reactor
	if request.method == 'GET':
		mode         = request.values.get('hub.mode')
		challenge    = request.values.get('hub.challenge')
		verify_token = request.values.get('hub.verify_token')
		if challenge:
	 		return Response(challenge)
	else: #POST
			print 'post viesti'
	 		x_hub_signature = request.headers.get('X-Hub-Signature')
			raw_response    = request.data
			if raw_response:
				fetchNewUpdate()
			try:
				reactor.process(CLIENT_SECRET, raw_response, x_hub_signature)
	 		except subscriptions.SubscriptionVerifyError:
				logging.error('Instagram signature mismatch')
	return Response("") #ei tarvitse vastausta.

#tekee subscription-toiminnon flask-sovelluksen kaynnistyttya
def doSubscribe():
	print "Subscription process starting"
	time.sleep(25)
	global tag
	subscribeToTag(tag)
	print 'Subscription process ended'


def stop_subscription():
	api.delete_subscriptions(id=subID, client_secret=CLIENT_SECRET)


def list_subscriptions():
	api.list_subscriptions(callback_url=CALLBACK_TUNNEL)

api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN) 
reactor = subscriptions.SubscriptionsReactor()


class SubscriptionProcess(multiprocessing.Process):

	def __init__(self, ):
		multiprocessing.Process.__init__(self)
		self.exit = multiprocessing.Event()

	def run(self):
		try:
			doSubscribe()
		except Exception, e:
			print "Error during subscription process"
			print e

	def terminate(self):
		self.exit.set()


def startSubscription():
	 #if (list_subscriptions() == None):
	 subProcess = SubscriptionProcess()
	 subProcess.start()
