from Corretora import Agente
from market.MarketData import marketData

corretoras = {
    122: 'BGC Liquidez',  # 0
    85: 'BTG',
    72: 'Bradesco',
    6003: 'C6',
    88: 'Capital',
    45: 'Credit',
    120: 'Genial',
    238: 'Goldman',
    1130: 'Intl',
    114: 'Itau',
    16: 'JpMorgan',
    13: 'Merril',
    40: 'Morgan',
    23: 'Necton',
    92: 'Renascenca',
    27: 'Santander',
    127: 'Tullet',
    8: 'UBS',
    3: 'XP'
}


def get_corretoras() -> list:
    corretoras = {}
    for key, value in corretoras.items():
        corretoras.update(key , Agente(key, value))
    return corretoras


class acumula:
    def __init__(self, ativo) -> None:
        print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(
            __file__, __name__, str(__package__)))
        self.market = Ma
        self.ativo = ativo
        self.qtd_agressao_compra = 0
        self.qtd_agressao_venda = 0
        self.corretoras = get_corretoras()
        print(self.corretoras)
        pass

    def run(self):
        while True:
            negocio = self.market.last(self.ativo)
            self.colector(negocio)

    def colector(self, negocio):
        if 'comp' in negocio['agressor']:
            self.qtd_agressao_compra += negocio['qntd']
            negocio['comprador']
        else:
            self.qtd_agressao_venda += negocio['qntd']


ac = acumula('wdoq21')
ac.run()
