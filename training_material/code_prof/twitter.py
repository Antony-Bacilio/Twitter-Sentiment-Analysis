# version1 with normal Bearer
import tweepy
import credentials
import pandas as pd

""" client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN)
query='covid -is:retweet'
response= client.search_recent_tweets(query=query,max_results=100,
tweet_fields=['created_at','lang'],user_fields=['profile_image_url'],
expansions=['author_id'])
users= {u['id'] : u for u in response.includes['users']}
for tweet in response.data:

    if(users[tweet.author_id]):
     user=users[tweet.author_id]
    print(tweet.id)
    print(user.username)
    print(user.profile_image_url)  """

# utiliser kafka streaming

""" stream = tweepy.Stream(
    credentials.API_KEY, credentials.API_SECRET_KEY,
    credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET
)
class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        print(status.id)


printer = IDPrinter(
    credentials.API_KEY, credentials.API_SECRET_KEY,
    credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET
)
printer.sample()

stream.filter(track=["Tweepy"]) """

# version avec client streaming
client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN)
query = 'covid -is:retweet'
response = client.search_recent_tweets(query=query,
                                       max_results=20,
                                       tweet_fields=['created_at', 'lang'],
                                       user_fields=['profile_image_url'],
                                       expansions=['author_id'])
print(response)
users = {u['id']: u for u in response.includes['users']}
print(users)
"""
for tweet in response.data:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
        print(tweet.id)
        print(tweet.created_at)
        print(tweet.lang)
        print(user.username)
        print(tweet.text)
        print(user.profile_image_url)"""


class IDPrinter(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.id)
        print(tweet.text)


printer = IDPrinter(credentials.BEARER_TOKEN)
printer.sample()

# create data frame
columns = ['User', 'Tweet']
data = []

for tweet in response.data:
    data.append([tweet.user.screen_name, tweet.full_text])

df = pd.DataFrame(data, columns=columns)

print(df)
# stream.filter(track=['codeanddogs'])
# version2 with Academic Bearer

""" import tweepy
import credentials
#place_country:GB
client = tweepy.Client(bearer_token=credentials.ACADEMIC_BEARER_TOKEN)
query='covid -is:retweet'
response= client.search_recent_tweets(query=query,max_results=100,
tweet_fields=['created_at','lang'],
expansions=['geo.place_id'])

places = {p['id']:p for p in response.includes['places']}
for tweet in response.data:

    print(tweet.id) """
