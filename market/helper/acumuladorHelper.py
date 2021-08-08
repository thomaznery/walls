import re


def is_dolar(ativo: str) -> bool:
    return 'WDO' in ativo


def is_indice(ativo: str) -> bool:
    return 'WIN' in ativo


def is_acao(ativo: str) -> bool:
    return re.match('[A-Za-z]{4}[0-9]{1}', ativo)


def isAgressaoCompra(agressor) -> bool:
    return 'Comp' in agressor


def isAgressaoVenda(agressor) -> bool:
    return 'Vend' in agressor


def isLeilao(agressor) -> bool:
    return 'Leil' in agressor


# se for uma agressao de compra,  incluiremos o negocio na variavel de lista de agressoes DO COMPRADOR e na lista de passivos do VENDEDOR
# se for uma agressao de venda, incluiremos o negocio na vriavel de lista de agressoes DO VENDEDOR e na lista de passivos do COMPRADOR
def direcionar_negocio(agentes, index_comprador, index_vendedor, negocio_model, agressor):
    if isLeilao(agressor):
        agentes[index_comprador].increment_trade_passivo(negocio_model)
        agentes[index_vendedor].increment_trade_passivo(negocio_model)
    if isAgressaoCompra(agressor):
        agentes[index_comprador].increment_trade_agressao(negocio_model)
        agentes[index_vendedor].increment_trade_passivo(negocio_model)
    if isAgressaoVenda(agressor):
        agentes[index_vendedor].increment_trade_agressao(negocio_model)
        agentes[index_comprador].increment_trade_passivo(negocio_model)


def preco_to_float(preco: str, ativo: str) -> bool:
    if is_dolar(ativo):
        preco = preco.replace('.', '')
        preco = preco.replace(',', '')
        return float(preco)
    if is_acao(ativo):
        preco = preco.replace(',', '.')
    return float(preco)
