import requests
import pickle
from market.db import Conexao
from market.Acumulador import acumula
import numpy
import pandas as pd

ac = acumula('wdou21')

ac.start()

c = Conexao()
