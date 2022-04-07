import json
import time
import urllib
from json import JSONEncoder
import re
import pandas as pd
import requests
import streamlit as st
from pykafka import KafkaClient

URL_API_POWERBI = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/8bf3f281-5b73-4a4f-a010" \
                  "-2df19883a9ce/rows?key=Mx%2BL%2BPKWe3fKPoBVkg%2FiKsjvR6w3pC55Can0R8dhFWNG8DzYG5KGAjdVa6ruHDqGmGt" \
                  "%2B7M877mgAfj10l2KlhQ%3D%3D "


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


class EncoderFunc(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

"""
def get_messages_from_topic(topicname):
    client = get_kafka_client()
    consumer_2 = client.topics[topicname].get_simple_consumer()

    for tweet in consumer_2:
        print("Testing get_from_topic : \n")
        print(tweet)
        data_str = tweet.value.decode()  # tweet.decode('utf8')
        print(data_str)  # type Str.

        data_dict = json.loads(data_str)
        print(data_dict)  # type Dict.

        return f"{data_dict}\n\n"
"""

# url_google = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor=false"
url_localhost_flask = "http://127.0.0.1:5002/api/tweets/twitterdata1"  # http://127.0.0.1:5002/ is from the flask api
response = requests.get(url_localhost_flask, stream=True)
response.raise_for_status()
# print(response)  # <Response [200]>
# print(response.raw)  # <urllib3.response.HTTPResponse object at 0x00000144CDBEA0B0>
"""data_text = response.text
data_content = response.content  # Binary.
data_content_decode = json.loads(response.content.decode('utf-8'))
data_json = response.json()  # json.loads(response.read())
print(data_content_decode)  # type ."""

for tweet in response.iter_lines(decode_unicode=True):
    print(tweet)  # type Str.

    # tweet1 = tweet.decode('utf-8')
    # print(tweet1)  # type Str.

    p = re.compile('(?<!\\\\)\'')
    # tweet1 = p.sub('\"', tweet)

    tweet1 = tweet.replace("\'", "\"")
    print(tweet1)

    # tweet_dict = json.loads(tweet1)
    # print(tweet_dict)  # type Dict.
    # get_messages_from_topic("twitterdata1")
    push = requests.post(URL_API_POWERBI, tweet1.encode('utf-8'))
    time.sleep(1)

    # data_table1 = pd.DataFrame(tweet)
    # st.write(data_table1)

if __name__ == '__main__':
    pass
