# Execution with TweePy version 3 (StreamListener), otherwise version 4 with Stream.

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


# Classe Listener.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        message = json.loads(data)
        if message['place'] is not None:
            client = get_kafka_client()
            topic = client.topics['twitterdata1']  # List of Topics and take one (twitterdata2)
            # Create a Producer for Topic (twitterdata2) in order to produce Events (records/messages)
            producer = topic.get_sync_producer()
            producer.produce(data.encode('ascii'))
            # To read these Events, go to a terminal and
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    """After authenticating to Twitter (lines 41 & 42) 
    we define a StdOutListener and start the streaming of Tweets (lines 43 & 44). 
    We can set filters to only stream Tweets which contain certain hashtags or keywords (line 48, 49 et 50) or 
    from defined locations (settings in line 52 defines worldwide).
    """
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    listener = StdOutListener()
    stream = Stream(auth, listener)

    # FILTERS:
    # stream.filter(track=['codeanddogs'])
    # stream.filter(track=['#Brexit', '#COVID'])  # track: key words for 'filter' tweets (like '#' hashtags for example)
    # stream.filter(track=['#COVID', '#covid', '#india'])
    # stream.filter(follow=["244632800"])
    stream.filter(locations=[-180, -90, 180, 90])
