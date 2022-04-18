import json
import streamlit as st
import pandas as pd
import requests
from afinn import Afinn
from dateutil.parser import parse
import predict_gender as pg


URL_POST_API_POWERBI_FR = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/75ba7120-ac3b-4a25-8066-b9111b6e6e96/rows?key=nuyRnKriZVVlhLxNJNXSmRrSJ4Nc26OovUEtQFsCoqT85IvaSt5NmV8oG3PJIOZmwdbtntpeqSo%2BMHLPfrd4IQ%3D%3D"


# Transform score in 'sentiment'.
def transform_score(score):
    try:
        if score < 0:
            return 'DEFAVORABLE'
        elif score == 0:
            return 'NEUTRE'
        else:
            return 'FAVORABLE'
    except TypeError:
        return 'NEUTRAL'


# TODO :
#  - Display others analysis: https://towardsdatascience.com/visualization-of-information-from-raw-twitter-data-part-1-99181ad19c
#  - Copy template of dashboard's teacher (VAL...)
#  - Set dashboards and report of PowerBI to adjust in a mobile.
#  - Deployment StreamLit Web App on a server and display from mobile.
def analysis(url):
    response = requests.get(url, stream=True)
    print("testing responses !!!")
    # print("status: ", requests.status_codes)
    # response.raise_for_status()

    # create AFINN object for sentiment analysis
    afinn = Afinn(language='fr')
    print("testing Afinn library !!!")

    # df_tweet_all = pd.DataFrame(columns=["user", "message_fr", "sentiment", "sex"])
    # list_vals = []

    for tweet in response.iter_lines(decode_unicode=True):
        if tweet:
            print("tweet:\n", tweet)  # type Str.
            # If tweets were in Binary format.
            # tweet_str = tweet.decode('utf8')
            # print("tweet_str: \n", tweet_str)

            # Replace one quote by double quote in order to transform it in a Dict.
            # tweet_str = tweet_str.replace("\'", "\"")
            # tweet_str = tweet_str.replace("null", "None")

            # Processing in Dict format.
            tweet_dict = json.loads(tweet)
            # print("tweet_dict:\n", tweet_dict)  # type Dict.

            # Add a Sentiment fields.
            score_message = afinn.score(tweet_dict['message_fr'])
            tweet_dict['sentiment'] = transform_score(score_message)

            # Add 'Gender' field to predict after.
            tweet_dict_sex = tweet_dict
            tweet_dict_sex['sex'] = pg.gender(tweet_dict['user'], tweet_dict['country'])
            print("tweet_dict_sex:\n", tweet_dict_sex)

            # TODO : DF in streaming : https://streamz.readthedocs.io/en/latest/dataframes.html
            list_val = [i for i in tweet_dict_sex.values()]
            list_keys = [i for i in tweet_dict_sex.keys()]

            # Transforming 'Dict' in 'Dataframe'.
            df_tweet = pd.DataFrame([tweet_dict_sex])
            # df_tweet.update(data_t)

            # st.write(df_tweet)
            df_tweet = df_tweet.drop(columns=["datetime", "message_size", "followers", "latitude", "longitude", "country", "city"])
            # Stack dataframes.
            # df_tweet_all = pd.concat([df_tweet_all, df_tweet], ignore_index=True)
            st.dataframe(df_tweet)
            print("df displayed !!")

            # Re-transform in Str to send to PowerBI.
            # Change format of datetime field.
            date = tweet_dict.pop('datetime')
            tweet_dict['datetime'] = parse(date)
            print("tweet_dict to be sent in 'Str' format:\n", tweet_dict)
            tweet_str = json.dumps(tweet_dict, default=str)

            # Post tweets on PowerBI.
            push = requests.post(URL_POST_API_POWERBI_FR, "[" + tweet_str + "]", stream=True)  # data.encode('utf-8')
            print("\tData transformed pushed to PowerBI...")

        else:
            print(" === tweet vide... ===\n")
