meses = { 1 : 'Janeiro',
        2: 'Fevereiro',	
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',	
        10: 'Outubro',
        11: 'Novembro',	
        12: 'Dezembro'}


vencimentos_indice = { 
        'F' : 'Janeiro',
        'G' : 'Fevereiro',	
        'H' : 'Março',
        'J' : 'Abril',
        'K' : 'Maio',
        'M' : 'Junho',
        'N' : 'Julho',
        'Q' : 'Agosto',
        'U' : 'Setembro',	
        'V' : 'Outubro',
        'X' : 'Novembro',	
        'Z' : 'Dezembro'}

STR_BASE_INDICE = 'WIN'

##TODO
def get_contrato_atual(mes:int, ano:int):
    i_mes = int(mes[-1] if int(mes) < 10 else mes)
    mes_str = meses[i_mes]
    letra = '#'
    for key,value in vencimentos_indice.items():        
        print(f'{value},{mes_str}')
        if value == mes_str:
            letra = key.upper()
            break

    ano = str(ano)[2:]
    return '{0}{1}{2}'.format(STR_BASE_INDICE,letra,ano)

from ClockHelper import CHelper
ch = CHelper()
print(get_contrato_atual(ch.mes(), ch.ano()))