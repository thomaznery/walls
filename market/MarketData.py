from client_rtd import RTDClient
from websearch.google import WSGoogle
from ClockHelper import CHelper
import socket
import logging
import TypeDataTryd as tdt
import pythoncom

# deixar o tryd aberto e logado, com servido de DDL ativo na mesma maquina
HOST = '127.0.0.1'
PORT = 12002


def ByteConvert(dataInfo, ativo):
    return str.encode(dataInfo+ativo+"#")


class MarketData:
    def __init__(self) -> None:
        # self.google = WSGoogle()
        logging.basicConfig(filename='socket_marketData.log',
                            encoding='utf-8', level=logging.DEBUG)
        self.ch = CHelper()
        self.clientRTD = RTDClient('tryd.rtdserver')

    def last(self, ativo):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                while True:
                    import time
                    try:
                        arrInfo = ''
                        s.sendall(ByteConvert(tdt.COTACAO, ativo))
                        data = s.recv(250)
                        arrInfo = data.decode().replace(
                            'COT!', '').split('|')
                        return arrInfo[1:2]
                    except Exception as e:
                        print(e)
                    finally:
                        arrInfo = ''

        except Exception as e:
            print("Erro ao contectar no servidor RTD")
            logging.info(e)

    def registrarTopicos(self, topicos: list):
        for topic in topicos:
            self.clientRTD.register_topic(topic)


if __name__ == '__main__':
    md = MarketData()

    topics = ['GRF', 'WDOQ21_MINUTE01_RSI']
    md.clientRTD.connect()
    md.registrarTopicos(topicos=topics)
    c = 1
    while c in range(1, 5, 1):
        import time
        time.sleep(1)
        md.last('WDOQ21_MINUTE01_RSI')
        """pythoncom.PumpWaitingMessages()
        if md.clientRTD.update():
            print(md.clientRTD.get('WDOQ21_MINUTE01_RSI_0'))"""
