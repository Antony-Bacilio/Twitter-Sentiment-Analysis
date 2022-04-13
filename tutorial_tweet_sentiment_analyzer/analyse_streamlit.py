import json
import time
import urllib
from json import JSONEncoder
import re
import pandas as pd
import requests
import streamlit as st
from pykafka import KafkaClient
from afinn import Afinn

URL_API_POWERBI = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/8bf3f281-5b73-4a4f-a010" \
                  "-2df19883a9ce/rows?key=Mx%2BL%2BPKWe3fKPoBVkg%2FiKsjvR6w3pC55Can0R8dhFWNG8DzYG5KGAjdVa6ruHDqGmGt" \
                  "%2B7M877mgAfj10l2KlhQ%3D%3D "


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


class EncoderFunc(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


# url_google = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor=false"
url_localhost_flask = "http://127.0.0.1:5001/topic/twitterdata1"
# url_localhost_flask = "http://127.0.0.1:5002/api/tweets/twitterdata1"  # http://127.0.0.1:5002/ is from the flask api
response = requests.get(url_localhost_flask, stream=True)
response.raise_for_status()
# print(response)  # <Response [200]>
# print(response.raw)  # <urllib3.response.HTTPResponse object at 0x00000144CDBEA0B0>

for tweet in response.iter_lines(decode_unicode=True):
    print(tweet)  # type Str.

    # tweet1 = tweet.decode('utf-8')
    # print(tweet1)  # type Str.

    # p = re.compile('(?<!\\\\)\'')
    # tweet1 = p.sub('\"', tweet)

    tweet1 = tweet.replace("\'", "\"")  # Replace one quote by double quote in order to transform it in a Dict.
    print(tweet1)  # type Str.

    # tweet_dict = json.loads(tweet1)
    # print(tweet_dict)  # type Dict.
    # TODO: Use 'afinn' library to analyse score of messages.

    # push = requests.post(URL_API_POWERBI, tweet1.encode('utf-8'))  # stream=True
    time.sleep(1)

    # data_table1 = pd.DataFrame(tweet)
    # st.write(data_table1)

if __name__ == '__main__':
    pass
