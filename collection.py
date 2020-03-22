from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from pymongo import MongoClient

i = 0
MONGO_HOST = 'mongodb://localhost:27017/twitter_database' 
FILE_NAME = "tweets_data5.json"

consumer_key="dQtJlDTYY1qrDWD3gThw7WTd3"
consumer_secret="9wo2doXpcs9bGDy7poUrMsaldSgyJ2dUK6SYeLJxbyTH75uKKP"

access_token="1230476879704010752-zLX1QEeGN6HZ2eJpxkUjF2GILtbNQX"
access_token_secret="mlhoO4ZDi1BNN57VL6tyhdsc2oefR0Km4LGAiVkONi8xj"
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
            #db.twitterdb_Excitement.insert(data_json)  # insert the data into the mongodb into a collection
            db.twitterdb_Happy.insert(data_json)
            #db.twitterdb_Pleasant1.insert(data_json)
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
	






