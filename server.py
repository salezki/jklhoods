import socket
import sys
import sqlite3 as lite
from thread import *
 
HOST = 'localhost'   # Symbolic name meaning all available interfaces
PORT = 9999 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for getting tweet data.
def twiits():
	con = None

	try:
		con = lite.connect('tweets.db')

		tweets = []
		cur = con.cursor()
		cur.execute('SELECT id FROM twitter_tweets')
		#filterointia varten
		#cur.execute('SELECT tweet.id FROM twitter_tweets tweet INNER JOIN twitter_tags tag ON tweet.id = tag.id')
		rows = cur.fetchall()
		for row in rows:
			tweets.append([row[0]])
		return tweets
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        tweet_IDs = twiits()
        data = conn.recv(1024)
        if str(data) is 'twitter_IDs':
	        #tweet_IDs = twiits()
	        reply = 'Toimii..' + tweet_IDs[0]
        if not data: 
            break
        else:
        	reply ='OK... ' + tweet_IDs[0]
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
