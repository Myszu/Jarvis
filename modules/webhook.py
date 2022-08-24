import requests

def respond(hook, msg):
    r = requests.post(url=hook, json={"Content": msg})