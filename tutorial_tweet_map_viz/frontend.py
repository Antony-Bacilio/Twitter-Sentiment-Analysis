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
from datetime import datetime
from dateutil.parser import parse

app = Flask(__name__)

URL_API_POWERBI = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/f05333e4-bf4c-4807-9d39" \
                  "-d5e789e8d2ed/rows?key=zjszKG0LBatEnBFHALeQDY9vYx2JNNWraTT3WYi7bxXCNlP48d9ZQOuZ0syKO6R7yEFGOoBzgN67Za8y8UqMtQ%3D%3D "
URL_API_POWERBI_TWEET = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/5dbe2194-ef79" \
                        "-40b9-a2a9-2d2288d987a5/rows?key=Eur7Z71GOtJI%2F%2BiCH3Cc%2FwH" \
                        "%2FaSBKfd4vl5d7a4jWN0BYrTKcqqHWU1V1NV7RcQITskX2DBIw4l4w%2FAAoRFN5Ww%3D%3D "


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/powerbi")
def report_powerbi():
    return render_template("report_powerbi.html")


# TODO : Perhaps use 'WordCloud' library to display subject tweets randomly in a 'brainstorming'
#  (on a web interface OR on PowerBI as a graphique): https://www.datacamp.com/community/tutorials/wordcloud-python
#  PS: Check ProjectType
@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()

    def events():
        consumer_1 = client.topics[topicname].get_simple_consumer()
        for tweet in consumer_1:
            tweet_str = tweet.value.decode()  # tweet.decode('utf8')
            # print(tweet_str)  # type Str.
            # tweet_dict = json.loads(tweet_str)
            # print(tweet_dict) # type Dict.
            yield f"data:{tweet_str}\n\n"

    return Response(events(), mimetype="text/event-stream")


@app.route('/api/tweets/<topicname>')
def publish_tweets(topicname):
    client = get_kafka_client()
    consumer_2 = client.topics[topicname].get_simple_consumer()

    def event():
        for tweet in consumer_2:
            tweet_str = tweet.value.decode()  # tweet.decode('utf8')
            # print(data_str)  # type Str.

            # Post tweets to PowerBI in 'Str' format.
            # Get the data pushed in JSON Dict format.
            tweet_transformed_dict = post_to_powerbi(tweet_str)
            print("tweet_transformed_dict:\n", tweet_transformed_dict)  # Type Dict.
            # new_tweet_dict = dict((k, v) for (k, v) in tweet_dict.items() if k == 'created_at' or k == 'text' or k
            # == 'lang')

            yield f"{tweet_transformed_dict}\n\n"

    return Response(event(), mimetype="text/event-stream")


# Pushing tweets transformed on PowerBI Service.
def post_to_powerbi(data: str):
    # Transforming data String in a Dict format.
    tweet_dict = json.loads(data)

    # Get message of tweet properly cleaned.
    print("message tweet (without cleaning):\n", tweet_dict['text'])
    message_tweet = nlp_cleaning_pipeline(tweet_dict['text'])

    # Sentiment response from a message (tweet).
    sentiment_status = sentiment_analysis(message_tweet)
    print("message tweet cleaned:\n", message_tweet)
    print("sentiment: ", sentiment_status)

    # Preparing a data structure to push into PowerBI.
    # TODO: Add a column about 'number of characters' of tweets messages for example.
    tweet_filtered = {'datetime': parse(tweet_dict['created_at']),
                      'user': tweet_dict['user']['name'],
                      'message': message_tweet,
                      'message_size': len(message_tweet),
                      'sentiment': sentiment_status,
                      'followers': tweet_dict['user']['followers_count'],
                      'latitude': tweet_dict['place']['bounding_box']['coordinates'][0][0][1],
                      'longitude': tweet_dict['place']['bounding_box']['coordinates'][0][0][0],
                      'city': tweet_dict['place']['name'],
                      'country': tweet_dict['place']['country']
                      }
    print("tweet_filtered:\n", tweet_filtered)  # type Dict.
    tweet_filtered_str = json.dumps(tweet_filtered, default=str)  # https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    push = requests.post(URL_API_POWERBI_TWEET, "[" + tweet_filtered_str + "]")  # stream=True
    print("tweet_filtered_str:\n", tweet_filtered_str)
    print("\tData transformed pushed to PowerBI...")
    return tweet_filtered


# Sentiment analysis of twets (message)
def sentiment_analysis(message: str):
    # Definition of an instance of sentiment analysis
    # using the pipeline function of hugging face transformers that we already imported.
    classifier = pipeline('sentiment-analysis')
    # TODO: Check 'nlp_cleaning_pipeline' function.
    # TODO: Fix 'tensorflow' bug during execution.
    sentiment_list = classifier(message)
    print("sentiment_list:\n", sentiment_list)  # type List.
    sentiment_status = sentiment_list[0]['label']
    return sentiment_status


# Cleaning of tweets (message).
def nlp_cleaning_pipeline(text):
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
