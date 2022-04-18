# APPLICATION 2 : is a Python Flask app with two routes.
# One route is an API which spins of an Apache Kafka Consumer and listens to the Twitter Topic (lines 18–24).
# The second route renders the frontend map with Leaflet JS (lines 14–16).

from flask import Flask, jsonify, request, Response, render_template
from pykafka import KafkaClient
import json


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('Testing get data from Flask.')


@app.route('/get/data-flask/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()

    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())

    return Response(events(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
