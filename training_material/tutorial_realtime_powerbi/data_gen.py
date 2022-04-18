from data_transf import TransformerDataGenerator
import requests
import time
import pandas as pd
import numpy as np
import tensorflow

REST_API_URL = 'https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/086fb7ac-5a02-450b-9ffd' \
               '-e4662033cfe0/rows?key=90Iy74H%2FEL3jec08PGPSzxgF' \
               '%2F73eBo68mXK5FtnryvHxnkMBgVitKiB2NQ7l9XQJ6aqq8XoIgUseO9OE2Wc1bQ%3D%3D '

tf = TransformerDataGenerator()

tf_json = None

while True:
    data_raw = []
    for i in range(1):
        tf_json = tf.data_generator()[0]
    data_json = bytes(tf_json, encoding='utf-8')
    print(data_json)
    # print("JSON dataset", data_json)

    # Post the data on the Power BI API
    req = requests.post(REST_API_URL, data_json)

    print("Data posted in Power BI API")
    time.sleep(2)
