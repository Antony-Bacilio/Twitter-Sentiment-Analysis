import datetime
import json
from json import JSONEncoder
import random
import requests
import time
import pandas as pd
import numpy as np

URL_API_POWERBI = "https://api.powerbi.com/beta/bc3dae5f-0b33-403d-b719-946457461af5/datasets/27d8afa1-55f0-4690-91e5" \
                  "-de6b7e811bdd/rows?key=tO9GZsFjka9Yc8wLMdPBgy26VSa0SC7YHE8OfDSfyFDxyFIkpzgpdeKCWhYeYFoZ" \
                  "%2BpCY4Hulvv%2BCwOfPmZHKMg%3D%3D "

rnd = random.Random()


class EncoderFunc(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class Temp:
    def __init__(self, zonename, temperature, dateime, ):
        self.zone_name = zonename
        self.date_time = dateime
        self.temperature = temperature

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


if __name__ == "__main__":
    while 1:
        rvalue = round(rnd.uniform(22.5, 25.5), 4)
        current_time = datetime.datetime.utcnow()
        tempDate = Temp("Zone A", rvalue, str(current_time), )

        # json_dict = EncoderFunc().encode(tempDate)
        # json_j = json.JSONEncoder().encode(tempDate)
        # print(json_dict)

        # json_temp = json.dumps(tempDate.to_json(), indent=4)
        # print(json_temp) # type Str.

        json_custom = json.dumps(tempDate, indent=4, cls=EncoderFunc)
        print(json_custom)  # type Str.

        data_to_push = "[" + json_custom + "]"  # with "[]" to match with PowerBI JSON format (no necessary).
        print(data_to_push)
        post_to_powerbi = requests.post(URL_API_POWERBI, json_custom)
        # post_to_powerbi = requests.post(URL_API_POWERBI, data_to_push)
        time.sleep(1)

        # src : https://pynative.com/make-python-class-json-serializable/
