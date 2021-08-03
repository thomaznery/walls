from threading import Thread


class Send_Signal(Thread):
    def __init__(self) -> None:
        Thread.__init__(self)

    def run(self):
        print('enviando sinal')
