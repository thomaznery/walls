import requests
import pickle4.pickle as pickle


class Post:
    def __init__(self) -> None:
        self.url = 'http://127.0.0.1:8000/marketdata/state_att'

    def send_acumulador_state(self, data):
        response = requests.post(url=self.url, data=data)
        return response
