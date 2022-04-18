# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import json
import requests

app = Flask(__name__)

METEO_API_KEY = "928e83e3e5e8c6729f91e306bec4ce42"

if METEO_API_KEY is None:
    # URL de test :
    METEO_API_URL = "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
else:
    # URL avec clé :
    METEO_API_URL = "https://api.openweathermap.org/data/2.5/forecast?lat=48.883587&lon=2.333779&appid=" + METEO_API_KEY


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")


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
    for prev in content["list"]:
        datetime = prev['dt'] * 1000
        temperature = prev['main']['temp'] - 273.15  # Conversion de Kelvin en °c
        temperature = round(temperature, 2)
        data.append([datetime, temperature])

    return jsonify({
        'status': 'ok',
        'data': data
    })


if __name__ == "__main__":
    app.run(debug=True)
