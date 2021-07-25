from websearch.google import WSGoogle
import configparser


class MarketData:
    def __init__(self) -> None:
        self.google = WSGoogle()
        self.config = configparser.ConfigParser().read('./saida/messages.ini')
