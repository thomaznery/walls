from .helper.AcumuladorHelper import preco_to_float


def somar_list(array):
    soma = 0
    for item in array:
        soma += item
    return soma


class Negocio:
    def __init__(self, numero, preco, hora, quantidade, comprador, vendedor, agressor) -> None:
        self.numero = numero
        self.preco = preco
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
    def __init__(self, id, nome, ativo) -> None:
        self.id = int(id)
        self.nome = nome
        self.ativo = ativo
        self.agressao_compras = []
        self.agressao_vendas = []
        self.compras_passivas = []
        self.vendas_passivas = []
        self.preco_medio_agressao_venda = 0
        self.preco_medio_agressao_compra = 0
        self.quantidade_de_ordens = 0

    # vai incluir um trade de agressao para o agente, na compra ou na venda
    def increment_trade_agressao(self, negocio: Negocio):
        self.quantidade_de_ordens += 1
        if self.id == int(negocio.comprador):
            self.agressao_compras.append(negocio)
        if self.id == int(negocio.vendedor):
            self.agressao_vendas.append(negocio)

    def increment_trade_passivo(self, negocio: Negocio):
        self.quantidade_de_ordens += 1
        if self.id == int(negocio.comprador):
            self.compras_passivas.append(negocio)
        if self.id == int(negocio.vendedor):
            self.vendas_passivas.append(negocio)

    def get_total_ordens(self):
        return self.quantidade_de_ordens

    def get_agressao_compra(self):
        return self.agressao_compras

    def get_vendas_passivas(self):
        sum = 0
        for neg in self.vendas_passivas:
            sum += int(neg.quantidade)
        return sum

    def get_compras_passivas(self):
        sum = 0
        for neg in self.compras_passivas:
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

    def get_preco_medio_agressao(self, compra):
        valores = []
        divisor = 0
        negocios = self.agressao_compras if compra else self.agressao_vendas
        for neg in negocios:
            valores.append(preco_to_float(
                neg.preco, self.ativo) * neg.quantidade)
            divisor += neg.quantidade
        if divisor != 0:
            return somar_list(valores)/divisor

    def get_content(self):
        pm_agressao_compra = self.get_preco_medio_agressao(True)
        pm_agressao_venda = self.get_preco_medio_agressao(False)
        return {
            'nome': self.nome,
            'Agressão Compradora': f'PM- {pm_agressao_venda}',
            'Agressão Vendedora': f'PM- {pm_agressao_compra}',
            'Total de ordens': f'{self.quantidade_de_ordens}'
        }
