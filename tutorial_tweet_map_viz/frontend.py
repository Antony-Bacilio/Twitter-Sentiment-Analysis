# Twitter API ---> twitter_v4.py (Kafka Producer) ---> leaf.js + Flask (Kafka Consumer).

# APPLICATION 2 : is a Python Flask app with two routes.
# One route is an API which spins of an Apache Kafka Consumer and listens to the Twitter Topic (lines 17-18).
# The second route renders the frontend map with Leaflet JS (lines 21-23).

from flask import Flask, jsonify, request, Response, render_template
from pykafka import KafkaClient
import json
import requests
import re
import pandas as pd

from transformers import pipeline

app = Flask(__name__)

URL_API_POWERBI = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/f05333e4-bf4c-4807-9d39-d5e789e8d2ed/rows?key=zjszKG0LBatEnBFHALeQDY9vYx2JNNWraTT3WYi7bxXCNlP48d9ZQOuZ0syKO6R7yEFGOoBzgN67Za8y8UqMtQ%3D%3D"
tweet_list = []


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/powerbi")
def report_powerbi():
    return render_template("report_powerbi.html")


@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()

    def events():
        consumer_1 = client.topics[topicname].get_simple_consumer()
        for tweet in consumer_1:
            tweet_str = tweet.value.decode()  # tweet.decode('utf8')
            # print(tweet_str)  # type Str.

            tweet_dict = json.loads(tweet_str)
            # print(tweet_dict) # type Dict.
            yield f"data:{tweet_str}\n\n"
            # yield 'data:{0}\n\n'.format(tweet_str)

    return Response(events(), mimetype="text/event-stream")


@app.route('/api/tweets/<topicname>')
def publish_tweets(topicname):
    client = get_kafka_client()
    consumer_2 = client.topics[topicname].get_simple_consumer()

    def event():
        for tweet in consumer_2:
            tweet_str = tweet.value.decode()  # tweet.decode('utf8')
            # print(data_str)  # type Str.

            post_to_powerbi(tweet_str)

            tweet_dict = json.loads(tweet_str)
            print(tweet_dict)

            new_tweet_dict = dict((k, v) for (k, v) in tweet_dict.items() if
                                  k == 'created_at' or k == 'id' or k == 'text' or k == 'lang')
            yield f"{new_tweet_dict}\n\n"

    return Response(event(), mimetype="text/event-stream")


def post_to_powerbi(data):
    tweet_dict = json.loads(data)
    resp = sentiment_analysis(tweet_dict['text'])
    print("resp: ", resp)
    # Preparing a data structure to push into PowerBI.
    tweet_filtered = {'user': tweet_dict['user']['name'],
                      'message': tweet_dict['text'],
                      'datetime': tweet_dict['created_at'],
                      'country': tweet_dict['place']['country'],
                      'city': tweet_dict['place']['name'],
                      'followers': tweet_dict['user']['followers_count']
                      }
    print(tweet_filtered)
    tweet_filtered_str = json.dumps(tweet_filtered)
    push = requests.post(URL_API_POWERBI, "[" + tweet_filtered_str + "]")
    print("Data pushed to PowerBI")


def sentiment_analysis(message):
    # Definition of an instance of sentiment analysis
    # using the pipeline function of hugging face transformers that we already imported.
    classifier = pipeline('sentiment-analysis')
    # tweet_list.append(message)
    # print("tweet_list:\n", tweet_list)
    # p = [sentiment for sentiment in classifier(tweet_list)]
    p = classifier(message)  # type Dict. ?
    print("p:\n", p)
    # q = [p[i]['label'] for i in range(len(p))]
    q = p[0]['label']
    return q
    # c0 = 'Tweet'
    # c1 = 'Sentiment'
    # df = pd.DataFrame(list(zip(tweet_list, q)), columns=[c0, c1])


# Nettoyage de tweets (message).
def nlp_pipeline(text):
    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)

    return text


if __name__ == "__main__":
    app.run(debug=True, port=5001)
