# Project ICD-TP1 python file
#
# lib package
# visualize class
#
# Description:
# This file contains the implementation of the visualize class,
#   which is intended to give an automatic way of generating the
#   graphs necessary for an exploratory analysis of the project
#   database.
################################################################

from .native_libs import *
from .utils import *

from matplotlib import pyplot as plt

class visualize:
	
	# Class manager
	# The first two columns of ~table~ are supposed to be
	#   'Região' and 'Ano', respectively.
	def __init__(self, table):
		# We need at least the two columns 'Região' and 'Ano',
		#   and one or more additional columns to the right.
		if len(table.columns) < 3:
			raise ValueError("Table with wrong format!")
		# Define object attributes
		self.__kidxs = np.array(table.columns[:2])
		self.__kcols = table.columns[2:]
		
		self.__plot(table);

	def __plot(self, table):
		years = table[self.__kidxs[0]].unique()
		regions = table[self.__kidxs[1]].unique()
		group = table.groupby(list(self.__kidxs[::-1])).sum()

		# Plotting standards chosen, taken from course material...
		plt.rcParams['figure.figsize']  = (12, 8)
		plt.rcParams['axes.labelsize']  = 20
		plt.rcParams['axes.titlesize']  = 20
		plt.rcParams['legend.fontsize'] = 20
		plt.rcParams['xtick.labelsize'] = 20
		plt.rcParams['ytick.labelsize'] = 20
		plt.rcParams['lines.linewidth'] = 4
		# ... until here
		# Below is local
		plt.rcParams['figure.titlesize'] = 24

		for col in self.__kcols:
			# One figure and one axis per column
			fig = plt.figure()
			# Figure title
			fig.suptitle(col)
			axes = plt.axes()
			for region in regions:
					reg_group = group.loc[region]
					axes.plot(years, reg_group[col], label=region)

			yticks_lims = (group[col].min(), group[col].max())
			plt.yticks(np.linspace(*yticks_lims, num=10))
			axes.legend()
			fig.show()

	@staticmethod
	def plot_ab(A, title):
		# Plotting standards chosen, taken from course material...
		plt.rcParams['figure.figsize']  = (12, 8)
		plt.rcParams['axes.labelsize']  = 20
		plt.rcParams['axes.titlesize']  = 20
		plt.rcParams['legend.fontsize'] = 20
		plt.rcParams['xtick.labelsize'] = 20
		plt.rcParams['ytick.labelsize'] = 20
		plt.rcParams['lines.linewidth'] = 4
		# ... until here
		# Below is local
		plt.rcParams['figure.titlesize'] = 24
		
		bins_kwargs = {'bins' : 30, 'edgecolor' : 'k', 'alpha' : 0.8, 'density' : True}
		# One figure and one axis per column
		fig = plt.figure()
		# Figure title
		fig.suptitle(title)
		axes = plt.axes()
		axes.hist(A, **bins_kwargs)
		fig.show()

	@staticmethod
	def plot_two(A, B, title):
		# Plotting standards chosen, taken from course material...
		plt.rcParams['figure.figsize']  = (12, 8)
		plt.rcParams['axes.labelsize']  = 20
		plt.rcParams['axes.titlesize']  = 20
		plt.rcParams['legend.fontsize'] = 20
		plt.rcParams['xtick.labelsize'] = 20
		plt.rcParams['ytick.labelsize'] = 20
		plt.rcParams['lines.linewidth'] = 4
		# ... until here
		# Below is local
		plt.rcParams['figure.titlesize'] = 24
		
		bins_kwargs = {'bins' : 30, 'edgecolor' : 'k', 'alpha' : 0.8, 'density' : True}
		# One figure and one axis per column
		fig = plt.figure()
		# Figure title
		fig.suptitle(title)
		axes = plt.axes()
		axes.hist(A, **bins_kwargs)
		axes.hist(B, **bins_kwargs)
		fig.show()

	@staticmethod
	def print_ics(*ics, title):
		print(title)
		for ic in ics:
			print(ic)
	
	@staticmethod
	def print_diff(df1, df2, title):
		arr1 = df1.iloc[::, -1].values
		arr2 = df2.iloc[::, -1].values
		print(title)
		print("Diferença:", utils.abs_mean(arr1, arr2))

	@staticmethod
	def plot_lr(predictor, df):
		visualize(df)
		years = df['Ano'].values
		predictions = predictor.predict(years.reshape(-1, 1))
		plt.plot(years, predictions, label='Regressão', color='k')
		plt.legend()
		
		
