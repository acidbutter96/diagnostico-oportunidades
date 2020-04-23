import numpy as np
import pandas as pd

from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns

#configurações do seaborn

sns.set_style('darkgrid')


#Analisar o head do Data Frame

pd.read_csv('Data_Base.csv', encoding = 'ISO-8859-1').head()

#Definir nome das colunas

colunas = ['ID', 'Data/Hora Dia',  'Mês', 'Ano', 'D#', 'Código', 'Código 2', 'Código 3', 'Tipo de venda', 'UF', 'Código 4', 'Família', 'Produto 1', 'ABC',  'Produto 2', 'Venda Bruta col', 'Venda Bruta 1', 'Venda Bruta 2', 'Venda Bruta 3']

df = pd.read_csv('Data_Base.csv',names=colunas, encoding = 'ISO-8859-1')

#Verificar quantos valores se repetem na mesma 

#Remover colunas que não utilizaremos para diagnóstico

#df.drop('Data/Hora Dia', axis=1, inplace=True)

YmdHM = (lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M'))

#Year month day hour minute
#converter coluna em formato datetime

df['Data/Hora Dia'] = df['Data/Hora Dia'].apply(YmdHM)

#Verificar quais colunas possuem valores que não se repetem e remover

verificar = [len(df.iloc[:,i].value_counts().values) for i in range(len(df.columns.values))]

unit, index = -1, []
for i in verificar: 
	unit+=1 
	print('verificando {}'.format(colunas[unit]))
	if i==1:
		index.append(unit)
		df.drop(colunas[unit], axis=1, inplace=True)
		print('Coluna {} removida'.format(colunas[unit]))
		#colunas.remove(colunas[unit])

for i in index:
	colunas.remove(colunas[i])
#remover 'Mês'

colunas.remove('Mês')
df.drop('Mês', inplace=True, axis=1)

#Verificar o restante dos dados a partir das correlações entre as colunas

def heatmap():
	crrdf = df.corr()
	fig = plt.figure(figsize=(10,5),dpi=200)
	plt.tight_layout()
	sns.heatmap(crrdf).set_title('Mapa de Calor - Correlação Entre Dados').get_figure().savefig('heatmap.png')

heatmap()