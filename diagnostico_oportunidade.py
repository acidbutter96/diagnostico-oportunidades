import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



#Analisar o head do Data Frame

pd.read_csv('Data_Base.csv', encoding = 'ISO-8859-1').head()

#Definir nome das colunas

colunas = ['Codigo', 'Data/Hora Dia',  'Mês', 'Ano', 'D#', 'Código', 'Código 2', 'Código 3', 'Tipo de venda', 'UF', 'Código 4', 'Família', 'Produto 1', 'ABC',  'Produto 2', 'Venda Bruta col', 'Venda Bruta 1', 'Venda Bruta 2', 'Venda Bruta 3']

df = pd.read_csv('Data_Base.csv',names=colunas, encoding = 'ISO-8859-1')
