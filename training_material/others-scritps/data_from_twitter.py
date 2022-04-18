import tweepy, time, credentials, json

# Authentication
auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Get user_id
user = api.get_user(screen_name='tonikon18')
# print(user)  # type <class 'tweepy.models.User'>
# User(_api=<tweepy.api.API object at 0x0000017CDE9C6530>,
#       _json={'id': 244632800, 'id_str': '244632800', 'name': 'Antony Bacilio S.', 'screen_name': 'tonikon18', ... })
print("ID of my twitter account : ", user.id)

# Get user_screen_name
user2 = api.get_user(user_id="244632800")
print("Screen name of my twitter account : ", user2.screen_name)
print("\n")

# Collecting timeline (historical tweets) of a user (@tonikon18).
try:
    list_tweets = tweepy.Cursor(api.user_timeline,
                                screen_name="tonikon18",
                                exclude_replies=True,
                                count=10).items()
    for tweet in list_tweets:
        # print(tweet)
        tweet_text = tweet.text
        time = tweet.created_at
        tweeter = tweet.user.screen_name
        # print("Text:" + tweet_text + ", Timestamp:" + str(time) + ", user:" + tweeter)
        tweet_dict = {"tweet_text": tweet_text.strip(), "timestamp": str(time), "user": tweeter}
        # As a JSON Object
        tweet_json = json.dumps(tweet_dict)
        print(tweet_json)  # type Str.
except tweepy.TweepyException:
    time.sleep(60)
