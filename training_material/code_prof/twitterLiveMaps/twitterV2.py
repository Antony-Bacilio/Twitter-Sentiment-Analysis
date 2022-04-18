import tweepy

consumer_key = "dKKSIgcQMBLZM7iH1Qb3VxD74"
consumer_secret = "OJtDmMvoO0c6y1DvQDV7bPE2ZlsqW7dNyeic1aov6jINfYN5SA"
access_token = "1499769278127611907-gDz9p9ZbCR1IPdUL2cjNyxwPTpelvv"
access_token_secret = "NrhnjFz0kWd8zuyNN1rrOzdh6WyFIukgVofpXhFV8oc5W"

# Your app's API/consumer key and secret can be found under the Consumer Keys
# section of the Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps


# Your account's (the app owner's account's) access token and secret for your
# app can be found under the Authentication Tokens section of the
# Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps


import tweepy

stream = tweepy.Stream(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
stream.filter(track=["Tweepy"])


class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        print(status.id)


printer = IDPrinter(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
printer.sample()
