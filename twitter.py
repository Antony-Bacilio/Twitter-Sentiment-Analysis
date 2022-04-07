# Available with tweepy v3.10.

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
# Kafka client for Python.
from pykafka import KafkaClient
import credentials


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


# Classe Listener.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        client = get_kafka_client()
        topic = client.topics['twitterdata1']  # List of topics.
        # Create a producer for this topic in order to produce messages.
        producer = topic.get_sync_producer()
        producer.produce(data.encode('ascii'))
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

    listener = StdOutListener()
    Stream = Stream(auth, listener)
    # follow : User ID of twitter account.
    # track : key words for 'filter' tweets (like '#' hashtags for example)
    Stream.filter(follow=["244632800"], track=['#Brexit', '#COVID'])
