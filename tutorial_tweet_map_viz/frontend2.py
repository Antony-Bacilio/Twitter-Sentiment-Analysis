# Twitter API ---> twitter_v4.py (Kafka Producer) ---> leaf.js + Flask (Kafka Consumer).

# APPLICATION 2 : is a Python Flask app with two routes.
# One route is an API which spins of an Apache Kafka Consumer and listens to the Twitter Topic (lines 17-18).
# The second route renders the frontend map with Leaflet JS (lines 21-23).
import pandas as pd
from flask import Flask, jsonify, request, Response, render_template
from pykafka import KafkaClient
import json
import requests

app = Flask(__name__)

topic1 = None
URL_API_POWERBI = ""


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


@app.route("/")
def index():
    return "SALUT"


"""
@app.route('/topic/<topicname>')
def get_messages(topicname):
    topic1 = topicname
    data_dict = {}
    client = get_kafka_client()

    def events():
        consumer_1 = client.topics[topic1].get_simple_consumer()
        for i in consumer_1:
            data_str = i.value.decode()
            # print(type(data_str))
            # data_dict = json.loads(data_str)
            # print(data_dict)
            # print(type('{0}\n\n'.format(data_str)))
            yield 'data:{0}\n\n'.format(data_str)

    return Response(events(), mimetype="text/event-stream")"""


def post_to_powerbi(data):
    pass


@app.route('/api/tweets/<topicname>')
def get_tweets(topicname):
    client = get_kafka_client()
    consumer_2 = client.topics[topicname].get_simple_consumer()

    def event():
        for tweet in consumer_2:
            data_str = tweet.value.decode()  # tweet.decode('utf8')
            # print(data_str)  # type Str.

            data_dict = json.loads(data_str)
            # print(data_dict)  # type Dict.
            # URL_PUBLISH = "http://127.0.0.1:5002/api/post/tweets/"+topicname
            # push = requests.post(URL_PUBLISH, data_dict)
            if data_dict['lang'] == 'en' or data_dict['lang'] == 'es' or data_dict['lang'] == 'fr':
                print(data_dict)
                new_data_dict = dict((k, v) for (k, v) in data_dict.items() if k == 'created_at' or k == 'id' or k == 'text' or k == 'lang' or k == 'timestamp_ms')
                data_dict = new_data_dict
                yield f"{data_dict}\n\n"

    return Response(event(), mimetype="text/event-stream")


"""
@app.route('/topic/<topicname2>')
def post_messages(topicname2):
    client2 = get_kafka_client()
    topic2 = client2.topics[topicname2]  # List of Topics and take one (<topicname2>).
    # Create a Producer for Topic (twitterdata2) in order to produce Events (records/messages)
    producer2 = topic2.get_sync_producer()
    consumer_1 = client2.topics[topic1].get_simple_consumer()
    for data in consumer_1:
        producer2.produce(data.encode('ascii'))  # producer.produce(bytes(data, encoding='utf-8'))
"""

"""
def post_to_streamlit():
    streamlit_url = "http://127.0.0.1:8501/"
    client = get_kafka_client()
    consumer_1 = client.topics[topic1].get_simple_consumer()
    for i in consumer_1:
        req = requests.post(streamlit_url, data=i.json.JSONDecoder(), stream=True)
"""

if __name__ == "__main__":
    app.run(debug=True, port=5002)
