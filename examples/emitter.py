import requests

def user_defined_function(args):
    response = requests.request("GET", "http://backend:8080/tracked")
    json.loads(response.text)

