# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import multiprocessing
import streaminstagram
import streamtweet
import time, sys
import instaposts, twiitit, hashtags_twitter, hashtags_instagram
import os

"""

lt --port 8000 --subdomain nzmpqlpmhe

"""

app = Flask(__name__)
app.add_url_rule('/realtime', methods = ['GET', 'POST'], view_func=streaminstagram.callback)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/twitter')
def twitter():
    return 'Twitter is here'

@app.route('/about')
def about():
    return 'The about page'    

@app.route('/alustaTweets', methods = ['POST'])
def alustaTweets():
    return twiitit.twiits()

@app.route('/alustaInstagrams', methods = ['POST'])
def alustaInstagrams():
	return instaposts.instagramPosts()

@app.route('/hashtags',methods = ['POST'])
def hashtags():
    return hashtags_twitter.tagit_twitter() 

@app.route('/hashtags_insta',methods = ['POST'])
def hashtags_insta():
    return hashtags_instagram.tagit_instagram() 

@app.route('/hae_twitter_tagilla',methods = ['POST'])
def hae_twitter_tagilla():
	print request.get_json()
    return twiitit.hae_tagilla(request.get_json())

@app.route('/hae_instagram_tagilla',methods = ['POST'])
def hae_instagram_tagilla():
    return instaposts.hae_tagilla(request.get_json())

@app.route('/haes_instagram_tagilla', methods = ['POST'])
def haes_instagram_tagilla():
	return instaposts.haes_tagilla(request.get_json())

@app.route('/haes_twitter_tagilla',methods = ['POST'])
def haes_twitter_tagilla():
    return twiitit.haes_tagilla(request.get_json())

@app.route('/fetchTweets', methods = ['POST'])
def fetchTweets():
    return twiitit.fetchTweets(request.get_json())

@app.route('/fetchTagTweets', methods = ['POST'])
def fetchTagTweets():
    return twiitit.fetchTagTweets(request.get_json())

@app.route('/fetchTagInstagram', methods = ['POST'])
def fetchTagInstagram():
	return instaposts.fetchTagInstagram(request.get_json())
	
@app.route('/fetchInstagram', methods = ['POST'])
def fetchInstagram():
    return instaposts.fetchInstagram(request.get_json())

@app.route('/haeSeuraavat_tweet', methods = ['POST'])
def haeSeuraavat_tweet():
    return twiitit.haeSeuraavat(request.get_json())
	
@app.route('/haeSeuraavat_instagram', methods = ['POST'])
def haeSeuraavat_instagram():
	return instaposts.fetchNext(request.get_json())
    
class ApplicationProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        try:
            startApp()
        except (KeyboardInterrupt, SystemExit):
            print "Exiting..."

    def terminate(self):
        print "Flask application shutdown initiated"
        self.exit.set()
    
    
def startApp():
    global app
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT')), use_reloader=False)
    #app.run(host='localhost', port=8000, use_reloader=True, debug=True)


def initializeInstagram():
    streaminstagram.startSubscription()    

    
if __name__ == '__main__':
    flaskapp = ApplicationProcess()
    flaskapp.start()
    tweetStream = multiprocessing.Process(target=streamtweet.runStream)
    tweetStream.start()
    instagramSubscription = multiprocessing.Process(target=initializeInstagram)
    instagramSubscription.start()
   
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt, SystemExit:
            instagramSubscription.terminate()
            flaskapp.terminate()
            sys.exit(0)