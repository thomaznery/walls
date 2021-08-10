import requests


def send_acumulador_state(data):
    url = 'http://127.0.0.1:8000/marketdata/state_att'
    response = requests.post(url, data)
    return response
