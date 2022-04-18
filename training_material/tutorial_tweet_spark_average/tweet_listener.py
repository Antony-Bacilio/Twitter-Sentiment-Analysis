import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import Stream
import json
import credentials
import pykafka
from afinn import Afinn
import sys


def get_kafka_client():
    return pykafka.KafkaClient(hosts='127.0.0.1:9092')


class TweetListener(Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, **kwargs):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret, **kwargs)
        self.client = get_kafka_client()
        self.producer = self.client.topics[bytes('twitter_topic', 'ascii')].get_producer()

    def on_data(self, data):
        try:
            json_data = json.loads(data)

            send_data = '{}'
            json_send_data = json.loads(send_data)
            json_send_data['text'] = json_data['text']
            json_send_data['senti_val'] = afinn.score(json_data['text'])

            print(json_send_data['text'], " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", json_send_data['senti_val'])

            self.producer.produce(bytes(json.dumps(json_send_data), 'ascii'))
            return True
        except KeyError:
            return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #    print("Usage: PYSPARK_PYTHON=python3 /bin/spark-submit ex.py <YOUR WORD>", file=sys.stderr)
    #    exit(-1)

    word = "covid"  # sys.argv[1]

    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    twitter_stream = TweetListener(credentials.API_KEY, credentials.API_SECRET_KEY, credentials.ACCESS_TOKEN,
                                   credentials.ACCESS_TOKEN_SECRET)

    # create AFINN object for sentiment analysis
    afinn = Afinn()

    twitter_stream.filter(languages=['en'], track=[word])
