import pandas as pd
from queue import Queue


# case de tendencia de alta final do dia
data_set_alta = pd.read_excel(
    'estrategias\medias_dolar_test_case1.xlsx', usecols='c')

medias = Queue(100)
for item in data_set_alta.values:
    medias.put(item)

if medias.full():
    print('cheio')

values = []
for item in medias.queue:
    values.append(item.copy())

# somente em caso de teste
list.reverse(values)


print(values[-1])
print(values[0])
