# Project ICD-TP1 python file
#
# lib package
# process class
#
# Description:
# This file contains functions that implement data processing
#   for the project's database.
################################################################

from .native_libs import *

class process:
	def __init__(self):
		self.__table283 = self.__gentable283()
		self.__table6588 = self.__gentable6588()
		self.__utable = self.__unite()

	def get_table(self):
		return self.__utable

	def get_tables(self):
		return self.__table283, self.__table6588

	# Gets rid of year 2006 in table283, and appends the
	#   two original tables into one.
	def __unite(self):
		t283, t6588 = self.__table283, self.__table6588
		t283_not2006 = t283[t283['Ano'] != 2006]
		united = t283_not2006.append(t6588)
		# Sorting values again
		united = (united.sort_values(by=['Região', 'Ano'])).reset_index(drop=True)
		return united

	# Ler e limpar tabela 283, que contém dados sobre a produção 
	#   vegetal e área colhida de soja, separados por região(inclui 
	#   União), de 1920 a 2006.
	def __gentable283(self):
		
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

		# Removing invalid values from columns
		self.drop_invalid([table283])
		return table283

	# Ler e limpar tabela 6588, que contém estimativas mensais 
	#   de produção vegetal e área colhida, para cada região e
	#   para o Brasil inteiro.
	def __gentable6588(self):
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
		# Removing invalid values from columns
		self.drop_invalid([table6588])	

		return table6588

	def drop_invalid(self, tables):
		for table in tables:
			# Again, assume the first two columns are ['Ano', 'Região']
			for col in table.columns[2:]:
				for ind in table.index:
					val = table.loc[ind, col]
					if isinstance(val, str):
						if not val.isdecimal():
								table.loc[ind, col] = 0
			# Make those columns of numeric type
			# Except second column, which really is supposed to be string
			table.iloc[::, 0] = table.iloc[::, 0].astype(np.int64)
			table.iloc[::, 2:] = table.iloc[::, 2:].astype(np.float64)

	# Method used to normalize the table given as input
	@staticmethod
	def normalize(table):
		# We wont mess with first two columns
		table = table.copy()
		t = table.iloc[::, 2:]
		col_means = np.array([])
		for col in t.columns:
			# Calculate the correct mean based only upon non-zero values
			col_means = np.append(col_means, t[col].sum() / (t[col] != 0).sum())
		std = t.std()
		t = (t - col_means) / std
		table.iloc[::, 2:] = t
		return table

	# Normalize np array
	@staticmethod
	def arr_normalize(arr):
		return (arr - arr.mean()) / arr.std()

	# Return table in which two last columns were replaced
	#   by their division.
	@staticmethod
	def prod(table):
		table = table.copy()
		numerator = table[table.columns[-2]]
		denominator = table[table.columns[-1]]
		# Our new column
		n = len(numerator)
		prod_col = np.zeros(n)
		# We have to handle division by zero
		for i in range(n):
				if (numerator[i] == 0) or (denominator[i] == 0):
						prod_col[i] = 0
				else:
						prod_col[i] = numerator[i] / denominator[i]
		table.insert(loc=2, column='Produtividade (Tonelada / Hectare)', value=prod_col)
		return table.drop(columns=table.columns[3:])

	# Receives a normalized table.
	# First, drops the column 'Produção vegetal (Toneladas)'
	# Then, select only years after ~begin~
	# Then, puts in the increment of the values per year,
	#   instead of the values themselves.
	@staticmethod
	def fetchab(table, begin):
		table = table.copy()
		ystr = 'Ano'
		# Dropping column 'Produção vegetal (Toneladas)'
		table    = table.drop(columns=['Produção vegetal (Toneladas)'])
		# Getting only years after begin
		table = table[table[ystr] >= begin]
		# Putting in incremented values
		years = table[ystr].unique()
		vstr = 'Área colhida (Hectares)'
		cstr = 'Crescimento anual (%)'
		table = table.rename(columns={vstr : cstr})
		t = table.copy() # Temporary copy

		for year in years[1:]:
			cury_idx = table[table[ystr] == year].index
			lasty_idx = table[table[ystr] == (year-1)].index
			before  = t.loc[lasty_idx, cstr].values
			after = t.loc[cury_idx, cstr].values 
			diff = ((after - before) / before) * 100
			table.loc[cury_idx, cstr] = diff

		# Drop first year
		table = table.drop(index=table[table[ystr] == begin].index)
		return table
	
	# Returns the table separated into regions provided
	@staticmethod
	def sep_reg(table, regions):
		regstr = 'Região'
		separated = (table[table[regstr] == reg] for reg in regions)
		return separated
	
