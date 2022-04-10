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


@app.route("/powerbi")
def report_powerbi():
    return render_template("report_powerbi.html")


def post_to_powerbi(data):
    # push = requests.post(URL_API_POWERBI, data.encode('utf-8'))
    pass


@app.route('/api/tweets/<topicname>')
def publish_tweets(topicname):
    client = get_kafka_client()
    consumer_2 = client.topics[topicname].get_simple_consumer()

    def event():
        for tweet in consumer_2:
            tweet_str = tweet.value.decode()  # tweet.decode('utf8')
            # print(data_str)  # type Str.

            tweet_dict = json.loads(tweet_str)
            # print(data_dict)  # type Dict.
            # URL_PUBLISH = "http://127.0.0.1:5002/api/post/tweets/"+topicname
            # push = requests.post(URL_PUBLISH, data_dict)
            print(tweet_dict)
            new_tweet_dict = dict((k, v) for (k, v) in tweet_dict.items() if k == 'created_at' or k == 'id' or k == 'text' or k == 'lang' or k == 'timestamp_ms')
            tweet_dict = new_tweet_dict
            yield f"{tweet_dict}\n\n"

    return Response(event(), mimetype="text/event-stream")


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
