import time
from market.ClockHelper import CHelper


class RSIDolar():
    def __init__(self) -> None:

        self.name = 'Estrategia RSI DOLAR 1 MIN'
        self.rsi = 78
        self.signal = ('compra', 'venda')
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
