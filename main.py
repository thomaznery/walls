import threading
from market.acumulador import acumula
from queue import Queue
from estrategias.RSIDolar import RSIDolar
import time
from market.output import print_threads


# thread do acumulador
def iniciar_cobertura():
    try:
        acumulador_indice.run()
    except Exception as e:
        print(e)
    except KeyboardInterrupt as kb:
        print('.......')


def monitorar_threads():
    cont = 1
    while cont in range(10):
        time.sleep(1)
        cont += 1
        print_threads(threading.enumerate())


if __name__ == '__main__':
    acumulador_indice = acumula('wdou21')
    rsi = RSIDolar()
    rsi.start()

    acumulador_indice.start()

    #Thread(target=iniciar_cobertura, name='Thread[acumulador_indice]').start()
