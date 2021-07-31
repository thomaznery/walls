from prettytable import PrettyTable
from market.Corretora import Agente
import os

def print_agentes(agentes: list):    
    #os.system('cls' if os.name == 'nt' else 'clear')
    table = PrettyTable(['Corretora', 
                        'Agressão Compra(Qntd)', 
                        'Compras passivas(Qntd)',
                        'Agressão Venda(Qntd)',
                        'Vendas Passivas(Qntd)',
                         'Total de ordens'])    
                         
    table.align['Corretora'] = "l"
    table.align['Agressão Compra(Qntd)'] = "r"
    table.align['Compras passivas(Qntd)'] = "r"
    table.align['Agressão Venda(Qntd)'] = "r"
    table.align['Vendas Passivas(Qntd)'] = "r"    
    table.align['Total de ordens'] = "r"
    for agente in agentes:        
        table.add_row([f'{agente.id}-{agente.nome}' , 
            agente.get_agressoes_compra(), 
            agente.get_compras_passivas(),
            agente.get_agressoes_venda(),
            agente.get_vendas_passivas(),            
             agente.quantidade_de_ordens])        
        pass
    print(table)

