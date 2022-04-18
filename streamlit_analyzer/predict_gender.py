# Ex: https://gender-api.com/get?name=elizabeth&key=5CTSxkh3D9cFZYplaGPUozWdMlhQF3CwjXRb
import requests
import re

KEY_API = "5CTSxkh3D9cFZYplaGPUozWdMlhQF3CwjXRb"


# Cleaning of tweets (user).
def cleaning_user(text):
    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)

    return text


def gender(name, country):
    name = cleaning_user(name)
    URL_GENDER_API = "https://gender-api.com/get?name=" + name + "&country=" + country + "&key=" + KEY_API
    response = requests.get(URL_GENDER_API)
    response_data = response.json()
    if response_data["gender"] == "male":
        return "Masculin"
    elif response_data["gender"] == "female":
        return "Feminin"
    else:
        return "Inconnu"
