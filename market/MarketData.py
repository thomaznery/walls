
from ClockHelper import CHelper
import socket
import logging
import TypeDataTryd as tdt


# deixar o tryd aberto e logado, com servido de DDL ativo na mesma maquina
HOST = '127.0.0.1'
PORT = 12002


def ByteConvert(dataInfo, ativo):
    return str.encode(dataInfo+ativo+"#")


class MarketData():
    def __init__(self) -> None:
        # self.google = WSGoogle()
        logging.basicConfig(filename='socket_marketData.log',
                            encoding='utf-8', level=logging.DEBUG)
        self.ch = CHelper()

    def last(self, ativo):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))                
                try:
                    print('aaaaaaaaa')
                    arrInfo = ''
                    s.sendall(ByteConvert(tdt.NEGOCIO, ativo))
                    data = s.recv(3250)
                    arrInfo = data.decode().replace(
                        'NEG!', '').replace('#', '').split("|")
                    negocio = {
                        'numero': arrInfo[1],
                        'hora': arrInfo[2],
                        'preco': arrInfo[3],
                        'qntd': arrInfo[4],
                        'comprador': arrInfo[5],
                        'vendedor': arrInfo[6],
                        'agressor': arrInfo[7]
                    }
                    return dict(negocio)
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