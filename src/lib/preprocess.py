# Project ICD-TP1 python file
#
# lib package
# preprocess functions
#
# Description:
# This file contains functions that implement data preprocessing
#   for the project's database.
################################################################

from .native_libs import *

def preprocess_show(*dfs):
	for df in dfs:
		print(df.head(5))
		print(df.describe())
		print()


def preprocess():
	table283 = preprocess_283()
	table6588 = preprocess_6588()

	return table283, table6588

def preprocess_283():
	# Ler tabela 283, que contém dados sobre a produção vegetal e área colhida
	#   de soja, separados por região(inclui União), de 1920 a 2006.
	table283 = pd.read_csv("../database/283-soja-bgr-ap.csv", skiprows=1)
	# Limpeza dos dados
	temp = table283.copy()
	# Transformar dois tipos de valores da coluna "Variavel" em duas colunas inteiras.
	# Primeiro, focamos em "Produção vegetal"
	table283 = table283[table283['Variável'] == 'Produção vegetal (Toneladas)']
	# Essa coluna não terá significado na nova tabela que estamos montando.
	table283 = table283.drop('Variável', axis=1)
	table283 = table283.rename(columns={'Brasil e Grande Região': 'Região', 'Valor' : 'Produção vegetal (Toneladas)'})
	# Obtendo os valores para area colhida, em hectares
	table283_area_colhida = temp[(temp['Variável'] == 'Área colhida (Hectares)') | (temp['Variável'] == 'Área colhida')]['Valor'].copy()
	# Aqui, adiciono de volta os valores referentes à área colhida, em uma nova coluna à direita
	table283.insert(loc=table283.shape[1], column='Área colhida (Hectares)', value=table283_area_colhida.values)
	# Ordenando por região e ano
	table283 = table283.sort_values(by=['Região', 'Ano'])
	# Consertando indexes
	table283 = table283.reset_index(drop=True)

	return table283

def preprocess_6588():
	# Ler tabela 6588, que contém estimativas mensais de produção vegetal e área colhida,
	#   para cada região e para o Brasil inteiro.
	table6588 = pd.read_csv("../database/6588-soja-bgr-ap.csv", skiprows=2)
	
	# Processo parecido ao do processamento para tabela283
	temp = table6588.copy()
	# Transformar dois tipos de valores da coluna "Variavel" em duas colunas inteiras.
	# Primeiro, focamos em linhas Variável == 'Produção (Toneladas)'
	table6588 = table6588[table6588['Variável'] == 'Produção (Toneladas)']
	# Essa coluna não terá significado na nova tabela que estamos montando.
	table6588 = table6588.drop('Variável', axis=1)
	# Renomeamos colunas
	table6588 = table6588.rename(columns={'Brasil e Grande Região': 'Região', 'Valor' : 'Produção vegetal (Toneladas)'})
	# Obtemos valores da outra "Variável"
	table6588_area_colhida = temp[(temp['Variável'] == 'Área colhida (Hectares)') | (temp['Variável'] == 'Área colhida')]['Valor'].copy()
	# Aqui, adiciono de volta como uma coluna
	table6588.insert(loc=3, column='Área colhida (Hectares)', value=table6588_area_colhida.values)
	# Finalmente, consertamos indexes
	table6588 = table6588.reset_index(drop=True)
	# Pronto, o formato do DataFrame agora está correto, basta
	#   agora pegarmos as linhas que importam (última estimativa)
	#   de cada ano.
	
	# Abaixo é o algoritmo que pega o ultimo mes de cada ano
	########################################################
	table6588_meses = table6588['Mês']
	# A tabela cobre de 2006 a 2020, mas primeiro pegamos
	#   todos os anos menos o ultimo no range abaixo, porque
	#   o ultimo deve ser tratado especialmente abaixo.
	table6588_first_year = 2006
	table6588_last_year  = 2020
	
	table6588_common_last_month    = 'dezembro' # Ultimo mês nos anos sem ser o último
	table6588_last_year_last_month = 'agosto'   # Último mês para o último ano
	
	table6588_range_anos = np.arange(table6588_first_year, table6588_last_year) 
	
	# For every year, find lines that mention it and leave only
	#   the last one
	for ano in table6588_range_anos:
    # Find the lines that mention the current year
    # Every year except the last one is supposed to have dezembro included
    
    # Current slice (gets only best month in current year)
		current_slice = table6588['Mês'].str.contains(table6588_common_last_month + ' ' + str(ano))
		# Rest of the years
		the_rest      = ~table6588['Mês'].str.contains(str(ano))
		
		table6588 = table6588[current_slice | the_rest]
	
	# Treating last year specially
	# Current slice (gets only best month in current year)
	
	current_slice = table6588['Mês'].str.contains(table6588_last_year_last_month + ' ' + str(table6588_last_year))
	# Rest of the years
	the_rest      = ~table6588['Mês'].str.contains(str(table6588_last_year))
	table6588 = table6588[current_slice | the_rest]
	
	########################################################
	
	# Finalmente
	# Renomeando columa "Mês"
	table6588 = table6588.rename(columns={'Mês': 'Ano'})
	table6588['Ano'] = table6588['Ano'].str.replace('dezembro |agosto ', '', regex=True)
	# Ordenando por ano e regiao
	table6588 = table6588.sort_values(by=['Região', 'Ano'])
	# Consertando indexes
	table6588 = table6588.reset_index(drop=True)
	
	return table6588
