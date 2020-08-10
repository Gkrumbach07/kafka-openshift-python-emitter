import requests
import json

def user_defined_function(args):
    response = requests.request("GET", "http://backend:8080/tracked")
    data = json.loads(response.text)
    for loc in data["locations"]:
        yield loc


