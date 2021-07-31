from market.Corretora import Agente, Negocio
from market.MarketData import MarketData
from market.output import print_agentes

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

""""
    Classe com funcao de ler e acumular todos os negocios dos dias, separados por corretora
"""
class acumula:
    def __init__(self, ativo) -> None:        
        self.market = MarketData()        
        self.agentes = []
        self.set_agentes()
        self.ativo = ativo
        self.qtd_agressao_compra_dia = 0
        self.qtd_agressao_venda_dia = 0                      

        pass
    
    #receber o negocio e enviar ao coletor
    def run(self):        
        negocio = self.market.last(self.ativo)        
        self.colector(negocio)

    #fazer a analise do negocio e direcionado ao agente agressor
    def colector(self, negocio):
        agressor = negocio['agressor']
        quantidade = int(negocio['qntd'])
        
        self.acumular_volume(agressor, quantidade, negocio['preco'])
      
        index_comprador = self.get_index(int(negocio['comprador']))
        index_vendedor = self.get_index(int(negocio['vendedor']))
        
        #cada ordem geram dois negocios        
        negocio_model = Negocio(negocio['preco'], 
            negocio['hora'], negocio['qntd'],negocio['comprador'],negocio['vendedor'], agressor)

        
        self.agentes[index_comprador].increment_trade_agressao(negocio_model)    
        self.agentes[index_vendedor].increment_trade_passivo(negocio_model)    
        
        print(index_comprador)
        print(self.agentes[0].nome)
        print(negocio)
        print_agentes(self.agentes)

    def acumular_volume(self, agressor, quantidade, preco ):
        preco = preco.replace('.', '')
        preco = preco.replace(',', '.')                      
                
        if 'Comp' in agressor:
            self.qtd_agressao_compra_dia += quantidade * 1
        else:
            self.qtd_agressao_venda_dia += quantidade
        
    def get_index(self, numero):
        try:
            index = 0 
            for key, value in corretoras.items():                 
                if key == numero:                      
                    return index
                index += 1
            return 0
        except Exception as e:
            print(e.with_traceback())


    def get_agente_id(self, num_agente):
        return num_agente if self.agentes[num_agente] != None else 0
             

    def set_agentes(self) -> list: 
        for key, value in corretoras.items():                      
            self.agentes.append(Agente(key, value))        
