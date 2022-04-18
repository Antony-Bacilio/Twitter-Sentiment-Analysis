# -*- coding: utf-8 -*-
from pickle import TRUE
from flask import Flask, render_template, jsonify
import json
import requests
import random
from datetime import date
import time
import pandas as pd
import numpy as np

app = Flask(__name__)

# METEO_API_URL = 'https://api.powerbi.com/beta/e81af6ba-a66f-4cab-90f9-9225862c5cf8/datasets/51a56115-ac32-437a-8f2c
# -3ed1fa1dc37a/rows?key=24THP%2FqLUg2EWnDtFiTUr8GTjjPOU%2FxjT%2BnkTt9%2FHMlkMG
# %2B5BhWe0pYVfsJcE8gVNitZ3C2Fp1akv3LR7hLVNQ%3D%3D'
METEO_API_URL = 'https://api.powerbi.com/beta/dbd6664d-4eb9-46eb-99d8-5c43ba153c61/datasets/4fad882c-4fc1-458a-b363' \
                '-f5305a4645ef/rows?key=og49MAHp' \
                '%2BscrW1wJK8oCKdGlySKw8wMQXa2fzbGp7Au27SZv5VOEcO7wugML8duAokZmDAOEsorfSgI3HNw5KQ%3D%3D '
rnd = random.Random()


@app.route('/api/meteo/')
def meteo():
    response = requests.get(METEO_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(
                content['message'])
        }), 500

    data = []  # On initialise une liste vide

    while True:
        Zone_Name = "Zone A"
        Temperature = random.uniform(10, 35)
        Date_Time = date.today()
        data.append([Date_Time, Temperature, Zone_Name])

        print(data)
        # print("JSON dataset", data_json)

        # Post the data on the Power BI API
        req = requests.post(METEO_API_URL, data)

        print("Data posted in Power BI API")
        time.sleep(2)

    return jsonify({
        'status': 'ok',
        'data': data
    })


if __name__ == "__main__":
    app.run(debug=True)
