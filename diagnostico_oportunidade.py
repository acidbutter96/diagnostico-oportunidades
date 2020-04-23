import numpy as np
import pandas as pd

from datetime import datetime

import matplotlib.pyplot as plt

#configuração fonte títulos

font_title = {'family': 'cursive',
        'color':  'black',
        'weight': 'bold',
        'size': 26,
        }

font_axis = {'family': 'cursive',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

import seaborn as sns

#configurações do seaborn

sns.set_style('darkgrid')


#Seleção de Atributos

#Analisar o head do Data Frame

pd.read_csv('Data_Base.csv', encoding = 'ISO-8859-1').head()

#Definir nome dos atributos previsores pois estes não foram informados no Data frame.

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
	fig = plt.figure(figsize=(14,13),dpi=200).tight_layout()
	#plt.tight_layout()
	plot = sns.heatmap(crrdf,cmap='viridis').set_title('Mapa de Calor - Correlação Entre Dados', fontdict = font_title)
	plot.get_figure().savefig('heatmap.png')
	return plot

heatmap()