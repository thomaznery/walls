from .helper import acumuladorHelper as ah
from market.Corretora import Agente, Negocio
from market.MarketData import MarketData
from market.output import print_agentes


#lista de corretoras monitoras pelo sistema, apenas corretas grandes que movimentam o mercado
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

""""
    Classe com funcao de ler e acumular todos os negocios dos dias, separados por corretora
"""
class acumula:
    def __init__(self, ativo) -> None:        
        self.market = MarketData()        
        self.agentes = []
        self.ativo = ativo.upper()
        self.qtd_agressao_compra_dia = 0
        self.qtd_agressao_venda_dia = 0               
        self.volume_total = 0       
        for key, value in corretoras.items():                      
            self.agentes.append(Agente(key, value))        
            
    #receber o negocio e enviar ao coletor
    def run(self):        
        negocio = self.market.last(self.ativo)        
        self.colector(negocio)

    #fazer a analise do negocio e direcionado ao agente agressor
    def colector(self, negocio):
        agressor = negocio['agressor']
        preco = negocio['preco']
        comprador = negocio['comprador']
        vendedor = negocio['vendedor']
        quantidade = int(negocio['qntd'])
        negocio_model = Negocio(preco, negocio['hora'], quantidade,comprador,vendedor, agressor)
        
        index_comprador = self.get_index(int(comprador))
        index_vendedor = self.get_index(int(vendedor))
                         
        ah.direcionar_negocio(self.agentes, index_comprador, index_vendedor, negocio_model, agressor)   
        self.somar_quantidade_dia(agressor, quantidade)
        self.acumular_volume(quantidade, preco)
        print(f'negocio= {negocio}')  
        print(f'volume total= {self.volume_total}')
        
    
    def somar_quantidade_dia(self, agressor, quantidade):
        if ah.isAgressaoCompra(agressor):
            self.qtd_agressao_compra_dia += quantidade
        else:
            self.qtd_agressao_venda_dia += quantidade

    def acumular_volume(self, quantidade, preco):
        ativo = self.ativo
        preco = ah.preco_to_float(preco, ativo)
        quantidade = int(quantidade)
        volume = 0
        if ah.is_dolar(ativo):
            volume = (preco * PONTO_MINI_DOLAR) * quantidade            
        if ah.is_indice(ativo):
            volume = (preco * PONTO_MINI_INDICE) * quantidade
        if ah.is_acao(ativo):
            volume = preco * quantidade
        self.volume_total += volume
      
        
    def get_index(self, numero):
        numero = int(numero)        
        index = 0 
        for key, value in corretoras.items():                 
            if key == numero:                      
                return index
            index += 1
        self.agentes.append(Agente(numero, 'Agente nao monitorado'))
        corretoras[int(numero)] = 'Agente nao monitorado'
        return len(self.agentes)-1 #retorna o ultim item incluido, evitando recusrividade 
        
        