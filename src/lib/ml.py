# Project ICD-TP1 python file
#
# lib package
# ml class
#
# Description:
# This file contains the implementation of the ml class, which
#   deals with machine learning and regression stuff.
################################################################

from .native_libs import *
from .process import *

from sklearn import metrics
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split

class ml:
	@staticmethod
	def lin_reg(x, y):
		# Normalize x and y
		x = x.values.reshape(-1, 1)
		y = y.values

		# Choose some alphas
		min_alpha = 0.1
		max_alpha = 10
		alpha = min_alpha
		possible_alphas = np.array([])
		while alpha < max_alpha:
				alpha = alpha * 2
				possible_alphas = np.append(possible_alphas, [alpha])

		# Ok, so let's do it, shall we?
		lr_estimator = RidgeCV(alphas=possible_alphas, scoring='neg_mean_squared_error')
		lr_predictor = lr_estimator.fit(x, y)

		# Alright! Our model has been trained.
		return lr_predictor
