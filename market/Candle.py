import numpy


def identificar_candle(values: list):
    max = numpy.max(values)
    min = numpy.min(values)
    fechamento = values[-1]
    abertura = values[1]
