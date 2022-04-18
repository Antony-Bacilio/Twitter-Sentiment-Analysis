import pandas as pd
from datetime import datetime
from datetime import timedelta
import requests
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


##class for data_generation


def data_generation():
    surr_id = random.randint(1, 3)
    speed = random.randint(20, 200)
    date = datetime.today().strftime("%Y-%m-%d")
    time = datetime.now().isoformat()

    return [surr_id, speed, date, time]


if __name__ == '__main__':

    REST_API_URL = 'https://api.powerbi.com/beta/dbd6664d-4eb9-46eb-99d8-5c43ba153c61/datasets/232a6770-4269-4348' \
                   '-8c6f-3123100e7c81/rows?key=ii3qvXx9SRAGZ6j4FvTQx' \
                   '%2FRlknST06zRmqDnvlX8DdZV0MPgm4d2H2NYqj18IbxkJcZL3iOBGDQvnurf2MLNVw%3D%3D '

    while True:
        data_raw = []
        for i in range(1):
            row = data_generation()
            data_raw.append(row)
            print("Raw data - ", data_raw)

            # set the header record
            HEADER = ["surr_id", "speed", "date", "time"]

            data_df = pd.DataFrame(data_raw, columns=HEADER)
            data_json = bytes(data_df.to_json(orient='records'), encoding='utf-8')
            print("JSON dataset", data_json)

            # Post the data on the Power BI API
            req = requests.post(REST_API_URL, data_json)

            print("Data posted in Power BI API")
            time.sleep(2)
