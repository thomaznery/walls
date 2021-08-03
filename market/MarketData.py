import threading
from market.helper.ClockHelper import CHelper
import socket
import logging
import market.TypeDataTryd as tdt
import requests


# deixar o tryd aberto e logado, com servido de DDL ativo na mesma maquina
HOST = '127.0.0.1'
PORT = 12002


def ByteConvert(dataInfo, ativo):
    return str.encode(dataInfo+ativo+"#")


class MarketData:
    def __init__(self) -> None:
        logging.basicConfig(filename='socket_marketData.log',
                            encoding='utf-8', level=logging.DEBUG)
        self.ch = CHelper()

    def ultimo_negocio(self, ativo):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((HOST, PORT))
                try:
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

    # RSI 1minuto
    def rsi_1min_dolar(self) -> float:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((HOST, PORT))
                try:
                    arrInfo = ''
                    s.sendall(ByteConvert(tdt.INTERVALO_GRAFICO,
                              'WDOU21_MINUTE01_RSI_0'))
                    data = s.recv(33)
                    arrInfo = data.decode().replace(
                        'GRF!', '').replace('#', '').replace(',', '.').split(";")
                    rsi = float(arrInfo[1])
                    return round(rsi, 3)
                except Exception as e:
                    print(e)
                finally:
                    arrInfo = ''

        except Exception as e:
            print("Erro ao contectar no servidor RTD")
            logging.info(e)

     # RSI 1minuto
    def mm_exponencial_15(self) -> float:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.settimeout(3)
                try:
                    arrInfo = ''
                    s.sendall(ByteConvert(tdt.INTERVALO_GRAFICO,
                              'WDOU21_MINUTE01_MA_0'))
                    data = s.recv(33)
                    arrInfo = data.decode().replace(
                        'GRF!', '').replace('#', '').replace(',', '.').split(";")
                    rsi = float(arrInfo[1])
                    return round(rsi, 3)
                except Exception as e:
                    print(e)
                finally:
                    arrInfo = ''

        except Exception as e:
            print("Erro ao contectar no servidor RTD")
            logging.info(e)
