from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello world !"


@app.route('/api/meteo/')
def meteo():
    dictionnaire = {
        'type': 'Prévision de température',
        'valeurs': [24, 24, 25, 26, 27, 28],
        'unite': "degrés Celcius"
    }
    return jsonify(dictionnaire)


if __name__ == "__main__":
    app.run()
