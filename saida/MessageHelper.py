import re


class MHelper:
    def __init__(self) -> None:
        pass

    def extract_tickets(self, msg: str) -> list:
        list = []
        if None != msg and 4 < len(msg):
            list = re.findall(r'[A-Za-z]{4}[0-9]{1}', msg.upper())
        return list
