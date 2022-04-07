# Twitter API ---> twitter_v4.py (Kafka Producer) ---> leaf.js + Flask (Kafka Consumer).

# APPLICATION 2 : is a Python Flask app with two routes.
# One route is an API which spins of an Apache Kafka Consumer and listens to the Twitter Topic (lines 17-18).
# The second route renders the frontend map with Leaflet JS (lines 21-23).

from flask import Flask, jsonify, request, Response, render_template
from pykafka import KafkaClient
import json
import requests

app = Flask(__name__)

URL_API_POWERBI = ""


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/topic/<topicname>')
def get_messages(topicname):
    data_dict = {}
    client = get_kafka_client()

    def events():
        consumer_1 = client.topics[topicname].get_simple_consumer()
        for tweet in consumer_1:
            data_str = tweet.value.decode()  # tweet.decode('utf8')
            # print(data_str)  # type Str.

            data_dict = json.loads(data_str)
            # print(data_dict) # type Dict.
            yield f"{data_dict}\n\n"

    return Response(events(), mimetype="text/event-stream")


def post_to_powerbi(data):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5001)
