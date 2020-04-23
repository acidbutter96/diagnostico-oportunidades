import numpy as np
import pandas as pd

from datetime import datetime

import matplotlib.pyplot as plt

#configuração fonte títulos

font_title = {'family': 'DejaVu Sans',
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


#ML


#Para codificar os dados categóricos pois o algorítmo não suporta str, como no R.
from sklearn.preprocessing import LabelEncoder

#Divisão dados de treino e teste
from sklearn.model_selection import train_test_split

#Método de Naive Bayes
from sklearn.naive_bayes import GaussianNB







#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

def heatmap(df,label='heatmap'):
	crrdf = df.corr()
	fig = plt.figure(figsize=(14,13),dpi=200).tight_layout()
	#plt.tight_layout()
	plot = sns.heatmap(crrdf,cmap='viridis').set_title('Mapa de Calor - Correlação Entre Dados', fontdict = font_title)
	plot.get_figure().savefig(label+'.png')

heatmap(df)
plt.show()

def pairplots(df,hue=False,label=''):
	plt.figure(figsize=(14,13),dpi=200)
	plt.title('Plot de pares entre atributos', fontdict = font_title)
	#plt.tight_layout()
	sns.pairplot(df,hue=hue)
	plt.savefig('pairplot'+label+'.png')


#remover ID e dados irrelevantes

df2 = df.drop(['ID', 'D#', 'Código',  'Código 2', 'Código 3','Código 4'],axis=1)

#todos as compras ocorrem no mesmo ano e na mesma hora (00:00) portanto só vou deixar o mês

df2['Mês'] = df2['Data/Hora Dia'].apply(lambda x: x.month)
df2['Dia'] = df2['Data/Hora Dia'].apply(lambda x: x.day)

#df2.rename(columns={'Data/Hora Dia':'Mês'},inplace=True)

#remover coluna datahoradia

df2.drop('Data/Hora Dia',axis=1,inplace=True)


#Somar as vendas brutas e remover as parciais


df2['Lucro'] = df2['Venda Bruta 1']+df2['Venda Bruta 2']+df2['Venda Bruta 3']

df2.drop(['Venda Bruta 1','Venda Bruta 2','Venda Bruta 3','Família'],axis=1,inplace=True)

#Lucro ou prejuízo


df2['Lucro']=df2['Lucro'].apply(lambda x: 'Lucro' if x>= df2['Lucro'].mean() else 'Prejuízo')


#verificar plot de pares

#pairplots(df2,hue='ABC',label='ABC')
#pairplots(df2,hue='UF',label='UF')
#pairplots(df2,hue='Produto 1',label='Produto 1')
#pairplots(df2,hue='Produto 2',label='Produto 2')



plt.show()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Modelo de Classificação

#Pretendo realizar algumas previsões com relação ao lucro das vendas feitas ao longo do ano levando em conta, dia, hora e todos os parâmetros contidos no Data base. Peço perdão pela confusão mas as colunas do data frame não haviam índices então não sabia com quais atributos eu estava trabalhando.


#Transformar dados categóricos (str) em números (int)

#previsores: atributos que serão usados para previsão da classe

#removendo dados não 'str' do atributo ABC


df2 = df2[df2['ABC'].apply(lambda x: False if type(x)!= np.str else True)]


previsores = df2.drop('Lucro',axis=1).values

#classe: atributos que queremos prever

classe = df2['Lucro']


#verificando as colunas
df2.info()

#problema com a coluna ABC

#df2['ABC'] = df2['ABC'].apply(lambda x: str(x))


#somente a primeira é não categórica


labelencoder = LabelEncoder()

categoricos = ['Tipo de venda', 'UF', 'Produto 1', 'ABC', 'Produto 2']

for n in range(5):
	previsores[:,n] = labelencoder.fit_transform(previsores[:,n])


#Hold out
X_treinamento, X_teste, Y_treinamento, Y_teste = train_test_split(previsores,classe,test_size=.3,random_state=3452)


#Naive Bayes

naive_bayes = GaussianNB()

#ajuste

naive_bayes.fit(X_treinamento,Y_treinamento)


#previsões de dados

previsao = naive_bayes.predict(X_teste)


#Taxa de acerto e de erro

from sklearn.metrics import accuracy_score


taxa_acerto = (accuracy_score(Y_teste, previsao))*100
taxa_erro = (1 - taxa_acerto)*100


print('taxa de acerto do modelo de Naive Bayes: {}% \n---------------------\n taxa de erro do modelo de Naive Bayes: {}%'.format(taxa_acerto,taxa_erro))

#Visualizaremos a matriz de confusão através da Yellow Brick

from yellowbrick.classifier import ConfusionMatrix

v = ConfusionMatrix(GaussianNB())
v.fit(X_treinamento,Y_treinamento)
v.score(X_teste,Y_teste)
plt.title('Naive Bayes',fontdict=font_title)
plt.tight_layout()
plt.savefig('ConfusionMatrix Naive Bayes.png')
#v.poof()

plt.show()

#Da mesma forma pelo método de florestas aleatórias

from sklearn.ensemble import RandomForestClassifier

floresta = RandomForestClassifier(n_estimators = 200)

floresta.fit(X_treinamento,Y_treinamento)

previsoes2 = floresta.predict(X_teste)

u = ConfusionMatrix(RandomForestClassifier()).fit(X_treinamento,Y_treinamento)
u.score(X_teste,Y_teste)
plt.title('Florestas Aleatórias',fontdict=font_title)
plt.show()


taxa_acerto2 = (accuracy_score(Y_teste, previsoes2))*100
taxa_erro2 = (1-taxa_acerto2)*100

print('taxa de acerto do modelo de Florestas Aleatórias: {}% \n---------------------\n taxa de erro do modelo de: {}%'.format(taxa_acerto,taxa_erro))

#Da mesma forma podemos realizar os métodos de predição para outros dados categóricos do Data Base e a partir disso realizar um diagnóstico de oportunidade.

#Devido à falta de tempo e às dúvidas que tive sobre os dados dispostos na tabela (cujos atributos estavam vazios, consegui chegar até aqui)

#Poderíamos adotar outros métodos como o de seleção de atributos, mas os resultados estão bem próximos, talvez o modelo esteja super ajustado.