from market.acumulador import acumula
from market.MarketData import MarketData
from threading import Thread, Lock
from queue import Queue
from estrategias.RSIDolar import RSIDolar
import time
from market.ClockHelper import CHelper


def send_signal():
    time.sleep(2)
    signal = rsi_dolar_sinais.get(0)
    print('env ordem de ' + signal)
    SIGNAL = None
    threads_ordens.get()


def execute():    
    try:
        while ch.is_pregao_aberto():
            signal = instance.run()
            if rsi_dolar_sinais.empty():
                rsi_dolar_sinais.put(signal)
                threads_ordens.put(
                    Thread(target=send_signal, name=f'Thread send_orfer criada [/b]').start())
    except Exception as e:
        print(e)
    except KeyboardInterrupt as kb:
        print('.......')

def iniciar_cobertura():            
    try:
        acumulador_indice.run()
    except Exception as e:
        print(e)
    except KeyboardInterrupt as kb:
        print('.......')
   


if __name__ == '__main__':
    SIGNAL = None
    acumulador_indice = acumula('wdou21')
    instance = RSIDolar()
    ch = CHelper()
    rsi_dolar_sinais = Queue(1)
    threads_ordens = Queue(2)
    threads_rsi_dolar = Queue(1)
    """threads_rsi_dolar.put(
        Thread(target=execute, name='Thread[execute rsi.dolar]').start())"""

    Thread(target=iniciar_cobertura, name='Thread[acumulador_indice]').start()
    