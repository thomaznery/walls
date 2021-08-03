from threading import Thread
from market.output import print_threads, print_context
from market.helper.ClockHelper import CHelper
from market.MarketData import MarketData
from queue import Queue
import time
from market.Signal import Send_Signal

ch = CHelper()
marketD = MarketData()


NOME = 'RSI DOLAR - Halfredo Menezes'
TEMPO_GRAFICO = 1
ATIVOS = ['WDOFUT']
_FREQUENCY = 0.5  # segundos
POINT = 0.1
_QUEUE_SIZE = round((60/_FREQUENCY) * 10, 0)  # 10 minutos de pregao


class RSIDolar(Thread):
    def __init__(self) -> None:
        Thread.__init__(self)
        self.rsi = None
        self.name = NOME
        self.signal = {1: 'compra', 2: 'venda'}
        self.tendencia = {1: 'alta', 2: 'baixa'}
        self.medias_15 = Queue(_QUEUE_SIZE)

        # esta pilha controla o excesso de ordens, pois, não ira criar uma
        # nova thread de envio de ordem enquanto o objeto nao foi retirado na queue.
        # este objeto pode ser removido no momento de zerar posicao
        self.rsi_dolar_sinais = Queue(1)

    def update(self):
        if self.medias_15.full():
            self.rsi = marketD.rsi_1min_dolar()
        self.acumular_media_15()

    def run(self):
        while ch.is_pregao_aberto():
            tendencia = None
            signal = None
            self.rsi = None
            self.update()
            time.sleep(_FREQUENCY)
            if self.medias_15.full():
                tendencia = self.identificar_tendencia()
                if None != tendencia and None != self.rsi:
                    if self.rsi < 30 and tendencia == self.tendencia[1]:
                        signal = self.signal[1]
                        self.rsi_dolar_sinais.put(signal)
                    if self.rsi > 70 and tendencia == self.tendencia[2]:
                        signal = self.signal[2]
                        self.rsi_dolar_sinais.put(signal)

            if not self.rsi_dolar_sinais.empty():
                send = Send_Signal()
                send.start()
            content = {
                'rsi': self.rsi,
                'tendencia': tendencia,
                'signal': signal,
                'queueSize': self.medias_15.qsize(),
                'maxSize': self.medias_15.maxsize}
            print_context(content)


    # se as medias se deslocaram , e se esse deslocamento foi maior que 3 pts de dolar
    def identificar_tendencia(self):
        result = None
        values = []
        diff = 0
        for item in self.medias_15.queue:
            values.append(item)
        diff = round(values[-1] - values[0], 2)

        if diff > POINT * 10:
            result = self.tendencia[1]
        if diff < POINT * -10:
            result = self.tendencia[2]

        context = {
            'M Inicio': values[-1],
            'M Final': values[0],
            'Diff': diff,
            'Pontos de corte/Alta': POINT * 10,
            'Pontos de corte/Baixa': POINT * -10,
            'Tendencia': result
        }
        # print_context(context)
        return result


    # acumular medias por 15 minutos, sendo que  get_frequency() / 60  = quantidade de loops necessário para se
    # ter um minutos de media... então, x15, pois precisamos de 15min de mercado aberto
    def acumular_media_15(self):
        media = marketD.mm_exponencial_15()
        if self.medias_15.full():
            self.medias_15.get()
            self.medias_15.put(media)
        else:
            self.medias_15.put(media)

    # 5 segundos para cada loop desta estratégia
    def get_frequency(self):
        return _FREQUENCY
