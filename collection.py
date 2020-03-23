from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from pymongo import MongoClient

i = 0
MONGO_HOST = 'mongodb://localhost:27017/twitter_database' 
FILE_NAME = "tweets_data5.json"

consumer_key="******"
consumer_secret="******"

access_token="*******"
access_token_secret="******"
keywords =" happy"
 #["#happy","#joy","#love"]
 #["#pleasant","#trust","#like","#admiration"]
 #["#Surprise","#sad","#frustration","#sadness","#amazement","#distracting"]
 #["#fear","#disgust","#depression","#shy","#fearful","#terrifies"]
 #["#angry","#anger","#roar","#hormonal","#veryangry","#temper"]
 #["#excitement","#anticipation","#expecting","#interested","#interesting"]

class StdOutListener(StreamListener):
     
        
    	#This function gets called every time a new tweet is received on the stream
    def on_data(self, data):
        
        global i
        try:
            
            with open(FILE_NAME, 'a') as tf:  # write data to file
                tf.write(data)
                
            client = MongoClient(MONGO_HOST)  # connect mongodb
            db = client.twitter_database  # create db
            data_json = json.loads(data)  # Decode the JSON from Twitter
            db.twitterdb.insert(data_json) 
            # insert the data into the mongodb into a collection
            
            db.twitterdb_Excitement.insert(data_json) 
            #db.twitterdb_Happy.insert(data_jso)n)
            #db.twitterdb_Pleasant1.insert(data_json
            #db.twitterdb_ .insert(data_json)
            #db.twitterdb_Fear.insert(data_json)
            #db.twitterdb_Angry.insert(data_json)
            
            #db.twitterdb_Pleasant.insert(data_json)
            #data_json.drop("twitterdb_Pleasant")
            
            text= data_json["text"] #The text of the tweet
            print(text) #Print it out
            print(i)
            print("___________________________________")
            i=i+1;
            if i>=40:
                return False;
            
            
        except Exception as e:
            print(e)
            
    def on_error(self, status):
        print("ERROR")
        print(status)          
	
if __name__ == '__main__':
	try:
		#Create a file to store output. "a" means append (add on to previous file)
		fhOut = open("output.json","a")

		#Create the listener
		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		#Connect to the Twitter stream
		stream = Stream(auth, l)	
		#Terms to track
		stream.filter(track=keywords)
        stream.filter(language=['en'])
		
		
	except KeyboardInterrupt:
		#User pressed ctrl+c -- get ready to exit the program
		pass

	#Close the 
	fhOut.close()
    
    
  






