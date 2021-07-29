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
    c = 1
    try:
        # while ch.is_pregao_aberto():
        while c in range(1, 10, 1):
            c += 1
            time.sleep(1)
            signal = instance.run()
            if rsi_dolar_sinais.empty():
                rsi_dolar_sinais.put(signal)
                threads_ordens.put(
                    Thread(target=send_signal, name=f'Thread criada no {c} [/b]').start())
    except Exception as e:
        print(e)
    except KeyboardInterrupt as kb:
        print('.......')


if __name__ == '__main__':
    SIGNAL = None
    rsi_dolar_sinais = Queue(1)
    instance = RSIDolar()
    ch = CHelper()
    threads_ordens = Queue(2)
    threads_rsi_dolar = Queue(1)
    """threads_rsi_dolar.put(
        Thread(target=execute, name='Thread[execute rsi.dolar]').start())"""

    md = MarketData()
    print(md.last('wdoq21'))