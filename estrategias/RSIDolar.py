class RSIDolar:
    def __init__(self) -> None:
        self.rsi = 0
        self.signal = ('compra', 'venda')
        pass

    def update(self):
        pass

    def run(self):
        if self.rsi > 70:
            return self.signal[0]
        if self.rsi < 30:
            return self.signal[1]
        return None