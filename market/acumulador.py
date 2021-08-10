import pickle
from queue import Queue
import queue
from market.http import send_acumulador_state
from .helper.AcumuladorHelper import *
from threading import Thread
from market.Corretora import Agente, Negocio
from .MarketData import ultimo_negocio
from .helper.ClockHelper import *
from .db import Conexao


# lista de corretoras monitoras pelo sistema, apenas corretas grandes que movimentam o mercado
# nao olhamos para corretoras, pequenas, como Clear, Modal
corretoras = {
    0: 'Agente nao monitorado',
    122: 'BGC Liquidez',
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

PONTO_MINI_DOLAR = 10
PONTO_MINI_INDICE = 0.20
TEMPO_GRAFICO = 5
""""
    Classe com funcao de ler e acumular todos os negocios dos dias, separados por corretora
"""


_NOME = 'Times and Trader WSS'


class acumula(Thread):
    def __init__(self, ativo) -> None:
        Thread.__init__(self)
        self.agentes = []
        self.ativo = ativo.upper()
        self.qtd_agressao_compra_dia = 0
        self.qtd_agressao_venda_dia = 0
        self.volume_total = 0
        for key, value in corretoras.items():
            self.agentes.append(Agente(key, value, self.ativo))
        self.db = Conexao()

    def run(self):  # receber o negocio e enviar ao coletor
        not_replicate_order = Queue(10)

        cont = 0
        while cont in range(0, 25, 1):
            # while is_pregao_aberto():
            cont += 1
            negocio = ultimo_negocio(self.ativo)

            if not not_replicate_order.queue.__contains__(int(negocio['numero'])):
                not_replicate_order.put(int(negocio['numero']))

        self.db.close()

    def get_state(self):
        state_acumulador = {
            'ativo': self.ativo,
            'qtd_agressao_compra_dia': self.qtd_agressao_compra_dia,
            'qtd_agressao_venda_dia': self.qtd_agressao_venda_dia,
            'volume_total': self.volume_total,
            'agentes': self.agentes
        }
        return state_acumulador

    def colector(self, negocio):
        numero = negocio['numero']
        agressor = negocio['agressor']
        preco = negocio['preco']
        comprador = negocio['comprador']
        vendedor = negocio['vendedor']
        quantidade = int(negocio['qntd'])
        negocio_model = Negocio(numero,
                                preco, negocio['hora'], quantidade,
                                comprador, vendedor, agressor)
        #self.db.incluir_negocio(negocio, self.ativo)
        index_comprador = self.get_index(int(comprador))  # index na lista em memoria
        index_vendedor = self.get_index(int(vendedor))

        if int(seg()) % 5 == 0:
            state = self.get_state()
            send_acumulador_state(state)

        if int(seg()) % 60 == 0:
            data = self.db.get_las_minute(self.ativo, 'max(preco) as max_preco,  min(preco) as min_preco , sum(quantidade) as quantidade ', 'group by agressor')
            data['var'] = round((data.at[0, 'max_preco'] - data.at[0, 'min_preco']) / data.at[0, 'min_preco'] * 100, 2)

            # a cada minuto tem um objeto do tipo
            # max_preco  min_preco  quantidade  var
            # 0   529050.0   528500.0         186  0.1
            # 1   529050.0   528500.0          18  0.1

        direcionar_negocio_em_memoria(self.agentes, index_comprador,
                                      index_vendedor, negocio_model, agressor)

        self.acumular_volume(quantidade, preco, agressor)

        # ULTIMA HORA DO PREGAO salvar todos os negocios em um temp/ para utilizar no proximo dia
        if int(hora()) > 16:  # depois das 17 a cada 5 segundos
            with open('market\\helper\\temp\\lastday_wdo.pickle', 'wb') as handle:
                pickle.dump(dict(negocio), handle, protocol=pickle.DEFAULT_PROTOCOL)

    # acumula volume diario do ativo

    def acumular_volume(self, quantidade, preco, agressor):
        if isAgressaoCompra(agressor):
            self.qtd_agressao_compra_dia += quantidade
        else:
            self.qtd_agressao_venda_dia += quantidade

        ativo = self.ativo
        preco = preco_to_float(preco, ativo)
        quantidade = int(quantidade)
        volume = 0
        if is_dolar(ativo):
            volume = (preco * PONTO_MINI_DOLAR) * quantidade
        if is_indice(ativo):
            volume = (preco * PONTO_MINI_INDICE) * quantidade
        if is_acao(ativo):
            volume = preco * quantidade

        self.volume_total += volume

    # retorna o indes em que o agente espa posicionado dentro da lista de agentes da classe
    # em memoria
    def get_index(self, numero):
        numero = int(numero)
        index = 0
        for key, value in corretoras.items():
            if key == numero:
                return index
            index += 1
        self.agentes.append(
            Agente(numero, 'Agente Null', self.ativo))
        corretoras[int(numero)] = 'Agente nao monitorado'
        # retorna o ultim item incluido, evitando recusrividade
        return len(self.agentes)-1
