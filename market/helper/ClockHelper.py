from datetime import datetime
import requests


url_api_calendario = 'https://api.calendario.com.br/?json=true&ano=2021&estado=SP&cidade=SAO_PAULO&token=bWljaGVsaW5pdGhvbWF6QGdtYWlsLmNvbSZoYXNoPTM1MDYxNDk2'
feriados = []
for item in requests.get(url_api_calendario).json():
    feriados.append(item['date'])
dtime = datetime
dias_uteis = [0, 1, 2, 3, 4]
horario_pregao = range(9, 18, 1)


def hora():
    return dtime.now().strftime('%H')


def min():
    return dtime.now().strftime('%M')


def ano():
    return dtime.now().strftime('%Y')


def seg():
    return dtime.now().strftime('%S')


def mes():
    return dtime.now().strftime('%m')


def is_feriado() -> bool:
    return dtime.now().strftime(f'%d/%m/%Y') in feriados


def is_dia_util():
    return dtime.now().weekday() in dias_uteis


def is_pregao_aberto():
    if not is_feriado() and is_dia_util():
        return int(hora()) in horario_pregao
    return False


def now():
    return dtime.now()


def hoje():
    return dtime.now().strftime('')


def dia(pattern):
    return dtime.now().strftime(pattern)
