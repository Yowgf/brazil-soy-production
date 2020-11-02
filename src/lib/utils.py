# Project ICD-TP1 python file
#
# lib package
# utils class
#
# Description:
# This file contains the implementation of the utils class,
#   which provides array/table manipulation functions.
################################################################

from .native_libs import *

class utils:
	# Returns the growth of the numeric columns in the period
	#   covered by the input table.
	@staticmethod
	def growth(table, period):
		if len(table.columns) != 3:
			raise ValueError("Wrong table format. Needs to be exactly 3 columns.")
		begin = period[0]
		end = period[1]
		t = table.copy()

		# Get the parts of the table we are interested in
		t_begin = t[t['Ano'] == begin].iloc[::, -1].values
		t_end   = t[t['Ano'] == end].iloc[::, -1].values
		
		# Porcentage growth per unit of time
		diff = ((t_end - t_begin) / t_begin) / (end - begin) * 100
		# 'Região' and the last column
		t = t[t.columns[1:]].groupby(by='Região').sum()
		t.iloc[::, -1] = diff

		# Finally, a simple name change to make it look better
		t = t.rename(columns={t.columns[-1] : 'Crescimento anual médio (%)'})
		# and... sorting!
		t = t.sort_values(by=t.columns[-1])
		return t

	@staticmethod
	def bootstrap(series, niter=5000):
		nsamples = int(np.ceil(np.sqrt(len(series))))
		means = np.array([])
		for i in range(niter):
			sample = series.sample(nsamples, replace=True)
			means = np.append(means, sample.mean())
		return means

	# Performs test AB in two preprocessed tables
	# Also, the tables are considered to have the same
	#   size, so we can simply permute the indexes.
	@staticmethod
	def ab(tableA, tableB):
		if len(tableA) != len(tableB):
			raise ValueError("Tables are supposed to have theh same size.")

		# First, do one-hot enconding
		supertable = tableA.append(tableB)

		m = len(tableA)
		supertable = supertable.drop(columns=supertable.columns[1])
		
		# Do numperms permutations
		numperms = 1000
		means = np.array([])
		possibilities = np.array(supertable.index)
		for i in range(numperms):
			perm = np.random.permutation(possibilities)
			sampleA = supertable.loc[perm[:m]][supertable.columns[-1]].values
			sampleB = supertable.loc[perm[m:]][supertable.columns[-1]].values
			
			# Then get their difference
			means = np.append(means, utils.abs_mean(sampleA, sampleB))
		return means
	
	# Returns the confidence interval for array arr
	@staticmethod
	def ic(arr):
		leftbound = np.percentile(arr, 2.5)
		rightbound = np.percentile(arr, 97.5)
		return leftbound, rightbound

	@staticmethod
	def abs_mean(arr1, arr2):
		return np.abs(arr1 - arr2).mean()
