# Execution with TweePy version 3 (StreamListener), otherwise version 4 with Stream.

# APPLICATION 1 : is mainly using Python Tweepy to listen to Twitter Streaming API. Whenever a relevant Tweet is
# received it produces this Tweet as a message to a topic on Apache Kafka. This was realized with the Pykafka library
# and editing the Tweepy standard StdOutListener class (see lines 15–27 below).

from tweepy.streaming import Stream as stm
from tweepy import OAuthHandler
import credentials
from pykafka import KafkaClient
import json


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


# Classe Listener.
class StdOutListener(stm):
    def on_data(self, data):
        # print(data)  # It's in Binary/bytes.
        message = json.loads(data)
        if message['place'] is not None:
            print(message)  # with one quote - type Dict.
            client = get_kafka_client()
            topic = client.topics['twitterdata1']  # List of Topics and take one (twitterdata1).
            # Create a Producer for Topic (twitterdata1) in order to produce Events (records/messages)
            producer_1 = topic.get_sync_producer()

            # Decode UTF-8 bytes to Unicode (with double quotes)
            # json_string = data.decode('utf8')
            # print(json_string)
            # print(type(json_string))  # type Str.

            # Load the JSON to a Python list & dump it back out as formatted JSON
            # json_dict = json.loads(json_string)
            # print(json_dict)  # Display in one line and with one quote.
            # print(type(json_dict))  # type Dict.

            # s = json.dumps(json_dict, indent=4, sort_keys=True)
            # print(s)  # Custom display (well separated with line breaks)
            # print(type(s))  # type Str.

            # 'data' in binary
            producer_1.produce(data)  # V3 : producer_1.produce(bytes(data, encoding='utf-8'))
            # To read these Events, go to a terminal and
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    """After authenticating to Twitter (lines 55 & 56) we define a StdOutListener and start the streaming of Tweets (lines 57 & 58). 
    We can set filters to only stream Tweets which contain certain hashtags or keywords (line 63, 64 and 65) 
    or from defined locations (settings in line 66 defines worldwide).
    """
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    listener = StdOutListener(credentials.API_KEY, credentials.API_SECRET_KEY, credentials.ACCESS_TOKEN,
                              credentials.ACCESS_TOKEN_SECRET)
    # stream = Stream(auth, listener)

    # FILTERS
    # stream.filter(track=['codeanddogs'])
    # stream.filter(track=['#Brexit', '#COVID'])  # track: key words for 'filter' tweets (like '#' hashtags for example)
    # stream.filter(track=['#COVID', '#covid','#india'])
    # stream.filter(follow=["244632800"])
    listener.filter(locations=[-180, -90, 180, 90])
