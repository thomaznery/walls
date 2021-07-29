import time
from market.ClockHelper import CHelper


class RSIDolar():
    def __init__(self) -> None:

        self.NAME = 'RSI DOLAR 1 MIN'
        self.RSI = 78
        self.signal = ('compra', 'venda')
        self.TEMPO_GRAFICO = 1
        self.ATIVO = 'WDOFUT'
        self.ATIVO_LABEL = 'DÓLAR FUTURO'
        pass

    def update(self):
        pass

    def run(self):
        self.update()
        if self.rsi > 70:
            return self.signal[0]
        if self.rsi < 30:
            return self.signal[1]
        return None
