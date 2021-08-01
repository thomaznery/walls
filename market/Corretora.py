
class Negocio:
    def __init__(self, preco, hora, quantidade, comprador, vendedor, agressor) -> None:
        self.preco =  preco
        self.hora = hora
        self.quantidade = quantidade
        self.comprador = comprador 
        self.vendedor = vendedor
        self.agressor = agressor
    
    def get_preco(self) -> float:
        return float(self.preco)


# o objeto Agente é criado e mantido até o final do pregão, acumulando os valores no escopo da corretora
# os trades(negocio) são divididos em duas formas , TRADE AGRESSIVO, onde, o agressor = Comprador e
# 
class Agente:
    def __init__(self, id, nome) -> None:
        self.id = int(id)
        self.nome = nome
        self.agressao_compras = []
        self.agressao_vendas = []     
        self.compras_passivas = []
        self.vendas_passivas = []

        self.quantidade_de_ordens = 0
    
    # vai incluir um trade de agressao para o agente, na compra ou na venda
    def increment_trade_agressao(self,negocio:Negocio):        
        self.quantidade_de_ordens += 1       
        if self.id == int(negocio.comprador) :            
            self.agressao_compras.append(negocio)                
        if self.id == int(negocio.vendedor):
            self.agressao_vendas.append(negocio)
        
    def increment_trade_passivo(self, negocio:Negocio):
        self.quantidade_de_ordens += 1       
        if self.id == int(negocio.comprador): 
            self.compras_passivas.append(negocio)                
        if self.id == int(negocio.vendedor): 
            self.vendas_passivas.append(negocio)

    def get_vendas_passivas(self):
        sum = 0
        for neg  in self.vendas_passivas:
            sum += int(neg.quantidade)
        return sum

    def get_compras_passivas(self):
        sum = 0
        for neg  in self.compras_passivas:
            sum += int(neg.quantidade)
        return sum

    def get_agressoes_venda(self) -> float:
        sum = 0
        for neg in self.agressao_vendas:
            sum += int(neg.quantidade)
        return sum
    
    def get_agressoes_compra(self) -> float:
        sum = 0
        for neg in self.agressao_compras:
            sum += int(neg.quantidade)
        return sum

    def get_preco_medio_agressao_venda(self):
        valores = []
        divisor = 0 
        for neg in self.agressao_vendas:
            valores.append(neg.preco * neg.quantidade)
            divisor += divisor
        return sum(valores)/divisor
    
    




