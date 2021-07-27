
from threading import local
import MetaTrader5 as mt5
import boto3


class Broker:

    result = 0

    def __init__(self) -> None:
        ssm_client = boto3.client("ssm", region_name='sa-east-1')
        response = ssm_client.get_parameter(
            Name="senha-modal-mt5", WithDecryption=True)
        SENHA_MODAL_MT5 = response["Parameter"]["Value"]

        if not mt5.initialize(
                login=2013505,
                server='ModalMais-DMA4 - Beta',
                password=SENHA_MODAL_MT5):
            print("initialize() failed, error code =", mt5.last_error())
            quit()
        print("MT5 CONNECTADO PARA NEGOCIAÇÂO")

    def get_ticket(self, ativo) -> list:
        ticket = mt5.symbol_info_tick(ativo)
        return ticket

    def get_positions_len() -> int:
        positions = mt5.positions_get()
        if None == positions:
            return 0
        else:
            return len(positions)

    def bid(self, ativo):
        try:
            ticket = mt5.symbol_info_tick(ativo)
            return ticket.bid
        except AttributeError:
            print("Value Error on bid: method")

    def ask(self, ativo):
        try:
            ticket = mt5.symbol_info_tick(ativo)
            return ticket.ask
        except AttributeError:
            print("AttributeError on ask: method")

    def long(self, signal, ativo):
        if self.get_positions_len() == 0:
            # preparamos a estrutura de solicitação para compra
            symbol = ativo
            symbol_info = mt5.symbol_sinfo(symbol)
            if symbol_info is None:
                print(symbol, "ativo nao encontrado, tentaremos inclui-lo")
                mt5.shutdown()
                quit()

            # se o símbolo não visivel disponível no MarketWatch, adicionamo-lo
            if not symbol_info.visible:
                print(symbol, "nao está visível, tentando... ")
                if not mt5.symbol_select(symbol, True):
                    print("symbol_select({}}) failed, exit", symbol)
                    mt5.shutdown()
                    quit()

            lot = 0.1
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).ask
            deviation = 20
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "sl": price - 100 * point,
                "tp": price + 100 * point,
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }

            # enviamos a solicitação de negociação
            result = mt5.order_send(request)
            # verificamos o resultado da execução
            print("1. order_send(): para {} {} lote = {} com desvio padrão={} ticks".format(
                symbol, lot, price, deviation))
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("2. order_send falhou, retorno={}".format(result.retcode))
            # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
                result_dict = result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field, result_dict[field]))
                    # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
                    if field == "request":
                        traderequest_dict = result_dict[field]._asdict()
                        for tradereq_filed in traderequest_dict:
                            print("       traderequest: {}={}".format(
                                tradereq_filed, traderequest_dict[tradereq_filed]))
                print("shutdown() and quit")
                mt5.shutdown()
                quit()

            print("ORDEM ENVIADA ", result)
            print("   POSICAO COMPRADA EM: POSITION_TICKET={}".format(result.order))
        else:
            print("..existe posicao aberta para o atvo")

    def close_position(self, signal, ativo):
        position_id = self.result['order']
        price = mt5.symbol_info_tick(ativo).bid
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": ativo,
            "volume": 0.1,
            "type": mt5.ORDER_TYPE_SELL,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # enviamos a solicitação de negociação
        result = mt5.order_send(request)
        # verificamos o resultado da execução
        print("zerando posição Long #{}-> Venda {} {} , quantidade:{} ".format(
            position_id, ativo, 0.1, price))
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("falhar na esxeção da ordem de venda={}".format(result.retcode))
            print("-->result", result)
        else:
            print("4. Posição:{} encerrada, retorno: {}".format(
                position_id, result))
        # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(
                            tradereq_filed, traderequest_dict[tradereq_filed]))

    def desconectar():
        mt5.shutdown()
