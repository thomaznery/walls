import pandas as pd


_COD_SERIE_SELIC_DIARIO = 'bcdata.sgs.11'

class SelicBC:
        def __init__(self) -> None:
                pass


        def get_selic_acumulada_30_dias(self):              
                URL = f'http://api.bcb.gov.br/dados/serie/{_COD_SERIE_SELIC_DIARIO}/dados/ultimos/30?formato=json'                
                acumulado = pd.read_json(URL)
                total = acumulado['valor'].sum()
                return round(total, 2)

        
