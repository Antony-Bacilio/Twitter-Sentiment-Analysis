# APPLICATION 1 : is mainly using Python Tweepy to listen to Twitter Streaming API.
# Whenever a relevant Tweet is received it produces this Tweet as a message to a topic on Apache Kafka.
# This was realized with the Pykafka library and editing the Tweepy standard StdOutListener class (see lines 15–27 below).

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
from pykafka import KafkaClient
import json

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        message = json.loads(data)
        if message['place'] is not None:
            client = get_kafka_client()
            topic = client.topics['twitterdata2']
            producer = topic.get_sync_producer()
            producer.produce(data.encode('ascii'))
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    """After authenticating to Twitter (lines 33 & 34) we define a StdOutListener and start the streaming of Tweets (lines 35 & 36). 
    We can set filters to only stream Tweets which contain certain hashtags or keywords (line 37) or from defined locations (settings in line 38 defines worldwide).
    """
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    listener = StdOutListener()
    stream = Stream(auth, listener)
    #stream.filter(track=['codeanddogs'])
    stream.filter(locations=[-180,-90,180,90])
