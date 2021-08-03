from datetime import datetime
import requests


class CHelper:

    def __init__(self) -> None:
        self.url_api_calendario = 'https://api.calendario.com.br/?json=true&ano=2021&estado=SP&cidade=SAO_PAULO&token=bWljaGVsaW5pdGhvbWF6QGdtYWlsLmNvbSZoYXNoPTM1MDYxNDk2'
        self.feriados = []
        for item in requests.get(self.url_api_calendario).json():
            self.feriados.append(item['date'])
        self.dtime = datetime
        self.dias_uteis = [0, 1, 2, 3, 4]
        self.horario_pregao = range(9, 18, 1)
        pass

    def hora(self):
        return self.dtime.now().strftime('%H')

    def min(self):
        return self.dtime.now().strftime('%M')

    def ano(self):
        return self.dtime.now().strftime('%Y')

    def mes(self):
        return self.dtime.now().strftime('%m')

    def is_feriado(self) -> bool:
        return self.dtime.now().strftime(f'%d/%m/%Y') in self.feriados

    def is_dia_util(self):
        return self.dtime.now().weekday() in self.dias_uteis

    def is_pregao_aberto(self):
        if not self.is_feriado() and self.is_dia_util():
            return int(self.hora()) in self.horario_pregao
        return False

    def now(self):
        return self.dtime.now()

    def hoje(self):
        return self.dtime.now().strftime('')
