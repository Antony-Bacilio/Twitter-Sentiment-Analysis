import json
import time
import re
import pandas as pd
from streamz.dataframe import DataFrame as DataFrameZ
import requests
import streamlit as st
import streamlit.components.v1
from afinn import Afinn
from dateutil.parser import parse
import ast

URL_POST_API_POWERBI_FR = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/75ba7120-ac3b-4a25-8066-b9111b6e6e96/rows?key=nuyRnKriZVVlhLxNJNXSmRrSJ4Nc26OovUEtQFsCoqT85IvaSt5NmV8oG3PJIOZmwdbtntpeqSo%2BMHLPfrd4IQ%3D%3D"


# Transform score in 'sentiment'.
def transform_score(score):
    try:
        if score < 0:
            return 'NEGATIVE'
        elif score == 0:
            return 'NEUTRAL'
        else:
            return 'POSITIVE'
    except TypeError:
        return 'NEUTRAL'


# TODO :
#  - Predict sex of a user? (gender-api, gender-guesser python)
#  - Display others analysis: https://towardsdatascience.com/visualization-of-information-from-raw-twitter-data-part-1-99181ad19c
#  - Copy template of dashboard's teacher (VAL...)
#  - Set dashboards and report of PowerBI to adjust in a mobile.
#  - Deployment StreamLit Web App on a server and display from mobile.
def sentiment_analysis():
    # Address from the flask api
    url_localhost_flask = "http://localhost:5001/api/tweets/twitterdata1"
    response = requests.get(url_localhost_flask, stream=True)
    # response = urllib.request.urlopen(url_localhost_flask).read()
    print("status: ", requests.status_codes)
    response.raise_for_status()
    # print(response)  # <Response [200]>
    # print(response.raw)  # <urllib3.response.HTTPResponse object at 0x00000144CDBEA0B0>

    # create AFINN object for sentiment analysis
    afinn = Afinn(language='fr')

    data_table = pd.DataFrame()
    list_vals = []

    for tweet in response.iter_lines(decode_unicode=True):
        if tweet:
            print("tweet:\n", tweet)  # type Str.
            print(type(tweet))

            # If tweets were in Binary format.
            # tweet_str = tweet.decode('utf8')
            # print("tweet_str: \n", tweet_str)

            # Replace one quote by double quote in order to transform it in a Dict.
            # tweet_str = tweet_str.replace("\'", "\"")
            # p = re.compile('(?<!\\\\)\'')
            # tweet_str = p.sub('\"', tweet_str)
            # tweet_str = tweet_str.replace("null", "None")
            # print("tweet with double quote:\n", tweet)  # type Str.

            # Processing in Dict format.
            # tweet_dict = ast.literal_eval("\'"+tweet_str+"\'")
            tweet_dict = json.loads(tweet)
            print("tweet_dict:\n", tweet_dict)  # type Dict.

            # Add a Sentiment fields.
            score_message = afinn.score(tweet_dict['message'])
            print(score_message)
            tweet_dict['sentiment'] = transform_score(score_message)
            print(tweet_dict)

            # TODO : DF in streaming : https://streamz.readthedocs.io/en/latest/dataframes.html
            list_val = [i for i in tweet_dict.values()]
            # print("list_vals:\n", list_vals)
            list_keys = [i for i in tweet_dict.keys()]
            # print("list_keys:\n", list_keys)

            # df3 = pd.concat([df1, df2], ignore_index=True)
            # df3

            list_vals.append(list_val)
            print("list_vals:\n", list_vals)
            data_t = pd.DataFrame(list_vals, columns=list_keys)  # data_table = pd.DataFrame([tweet_dict])
            print("data_t:\n", data_t)
            # data_table = pd.DataFrame.from_dict(tweet_dict)
            print("data_table:\n", data_table)
            data_table.update(data_t)
            st.write(data_table)
            print("salut")

            # Re-transform in Str to send to PowerBI.
            # Change format of datetime field.
            date = tweet_dict.pop('datetime')
            tweet_dict['datetime'] = parse(date)
            print("tweet_dict (with Datetime format):\n", tweet_dict)
            tweet_str = json.dumps(tweet_dict, default=str)

            push = requests.post(URL_POST_API_POWERBI_FR, "[" + tweet_str + "]", stream=True)  # data.encode('utf-8')
            print("\tData transformed pushed to PowerBI...")
            time.sleep(3)


if __name__ == '__main__':
    st.header("Welcome to our Sentiment Analysis StreamLit Web App")
    st.subheader('''
                    The page is divided in two categories:
                        1. Classifier library : Report and Dashboard of tweets (PowerBI).
                        2. Afinn library : Report and Dashboard of tweets (PowerBI).
                        3. Data predictions''')

    # The st.selectbox option helps us to create a dropdown menu which consists both the
    # above options. Further ahead, now let’s connect our PowerBI report to the app.
    options = st.selectbox("Please Select: ", ['PowerBI', 'Predictions'])

    # link_copied_from_powerbi_web_service
    URL_GET_POWERBI_RAPPORT_TWEETS_EN = "https://app.powerbi.com/reportEmbed?reportId=8e46e37b-5da1-4965-95c5-2977428760f6&autoAuth=true&ctid=bc3dae5f-0b33-403d-b719-946457461af5&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLW5vcnRoLWV1cm9wZS1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D"
    URL_GET_POWERBI_RAPPORT_TWEETS_FR = ""

    if options == 'PowerBI':
        print("Hi!")

        st.components.v1.iframe(URL_GET_POWERBI_RAPPORT_TWEETS_EN, width=1000, height=700, scrolling=True)
        # src: https://docs.streamlit.io/library/components/components-api
        # st.markdown(URL_POWERBI_RAPPORT_VANARSDEL, unsafe_allow_html=True)

    else:
        sentiment_analysis()
