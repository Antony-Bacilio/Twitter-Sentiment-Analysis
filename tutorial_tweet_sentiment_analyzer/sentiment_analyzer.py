# Execution with tweepy v4.
# Twitter API ---> StreamLit.

import tweepy as tw
import streamlit as st
import pandas as pd
import credentials
from transformers import pipeline
import requests

# Authentication
auth = tw.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

api = tw.API(auth, wait_on_rate_limit=True)

# Definition of an instance of sentiment analysis
# using the pipeline function of hugging face transformers that we already imported.
classifier = pipeline('sentiment-analysis')

# Title and a little description of what our app is doing.
st.title('Live Twitter Sentiment Analysis with Tweepy and HuggingFace Transformers')
st.markdown('This app uses tweepy to get tweets from twitter based on the input name/phrase. '
            'It then processes the tweets through HuggingFace transformers pipeline function for sentiment analysis. '
            'The resulting sentiments and corresponding tweets are then put in a dataframe for display which is what '
            'you see as result.')


def run():
    with st.form(key='Enter name'):
        search_words = st.text_input('Enter the name for which you want to know the sentiment')
        number_of_tweets = st.number_input(
            'Enter the number of latest tweets for which you want to know the sentiment(Maximum 50 tweets)', 0, 50, 10)
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            tweets = tw.Cursor(api.search_tweets,
                               q=search_words,
                               lang="en").items(number_of_tweets)
            print(tweets)
            tweet_list = [i.text for i in tweets]  # Text of each tweet.
            print("tweet_list:\n", tweet_list)
            p = [i for i in classifier(tweet_list)]
            print("p:\n", p)
            q = [p[i]['label'] for i in range(len(p))]
            c0 = 'Latest ' + str(number_of_tweets) + ' Tweets' + ' on ' + search_words
            c1 = 'Sentiment'
            df = pd.DataFrame(list(zip(tweet_list, q)),
                              columns=[c0, c1])
            st.write(df)


if __name__ == '__main__':
    run()
