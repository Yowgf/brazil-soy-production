# Project Brazil Soy Production python file
#
# lib package
# ml class
#
# Description:
# This file contains the implementation of the ml class, which
#   deals with machine learning and regression stuff. Makes
#   extensive use of sklearn library.
################################################################

from sklearn import metrics
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from .native_libs import *
from .process import *


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
        lr_estimator = RidgeCV(alphas=possible_alphas, scoring="neg_mean_squared_error")
        lr_predictor = lr_estimator.fit(x, y)

        # Alright! Our model has been trained.
        return lr_predictor

    # Performs polynomial regression on x and y, and
    #   returns the trained estimator
    @staticmethod
    def poly_reg(x, y, *, degree=3):
        polyreg = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())
        polyreg.fit(x, y)
        return polyreg

    # Predicts the maximum of a function of the years, given
    #   the predictor and the period
    @staticmethod
    def predict_max(predictor, df, period):
        # First we need to find out the mean squared error
        # This is the statistic we will be using to build the interval
        y_true = df["Produtividade (Tonelada / Hectare)"].values
        y_pred = predictor.predict(df["Ano"].values.reshape(-1, 1)).reshape(len(y_true))
        diff = y_true - y_pred
        mean_err = np.sqrt((diff**2).mean())

        # Error margin
        errmarg = mean_err
        years = np.linspace(*period, num=period[1] - period[0], endpoint=True).reshape(
            -1, 1
        )
        predictions = predictor.predict(years)
        pred_max = predictions.max()
        max_ic = pred_max * (1 - errmarg), pred_max * (1 + errmarg)
        # Find out what year is the max
        func = lambda arr, num: np.abs(arr - num).argmin()
        year_max = int(np.round(years[func(predictions, pred_max)]))
        return (
            np.round(pred_max, decimals=3),
            year_max,
            tuple(np.round(max_ic, decimals=3)),
        )
