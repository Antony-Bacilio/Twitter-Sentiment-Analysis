import tweepy
import credentials
import pandas as pd
import requests
import time

REST_API_URL = 'https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/42a914fc-2b2e-4775' \
                   '-9c36-88df2549fcde/rows?key=f7yAOnoLZCrWdlMqaAbf%2BWgGaM%2FHbQU' \
                   '%2Bjz67qqJuwlrujnFYpbm6r4cDU6O0L32N3aGpqbOwPOABaF0uGfU%2FBw%3D%3D '


while True:
    client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN)
    query = 'covid -is:retweet'
    response = client.search_recent_tweets(query=query, max_results=10,
                                           tweet_fields=['created_at', 'lang'], user_fields=['profile_image_url'],
                                           expansions=['author_id'])
    print("'Response':\n", response)  # type : <class 'tweepy.client.Response'>

    users = {u['id']: u for u in response.includes['users']}
    print("Response.includes['users']:\n", users)  # type Dict.

    data_raw = []
    print("'Response.data':\n", response.data)  # type List[<Tweet id=..., text=...>, <Tweet id=...>].

    tweet_list = [i.text for i in response.data]
    id_list = [i.id for i in response.data]
    vals = list(zip(id_list, tweet_list))
    print("vals:\n", vals)
    df = pd.DataFrame(vals,
                      columns=['identifiant', 'message'])
    print(df)
    # data_bytes = bytes(df.to_json(orient='records'), encoding='utf-8')  # type Binary.
    data_bytes = df.to_json(orient='records', force_ascii=True)
    print("JSON dataset: ", data_bytes)  # type Str.

    # Post the data on the Power BI API
    req = requests.post(REST_API_URL, data_bytes)

    print("Data posted in Power BI API")
    time.sleep(2)
