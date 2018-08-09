import csv
import sys
import math
import itertools
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from pyramid.arima import auto_arima

import statsmodels.api as sm

from Make_Prediction.data_stationary import stationary
from Make_Prediction.best_values import pdq_values

class ARIMA_implementation():

    def __init__(self):
        '''
        TO DO:
            Get different data based on user input
        '''
        #Get the data
        self.read_data = pd.read_csv('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data\individual_stocks_5yr\AAPL_data.csv')
        self.data = self.read_data['open']

        #Make data stationary
        station = stationary(self.data)
        self.stationary_data = station.main()

        #split into training and testing data
        self.training_data = self.stationary_data[:int(int(len(self.stationary_data))*.7)]
        self.testing_data = self.stationary_data[int(int(len(self.stationary_data))*.7):]

    def fit_data(self):
        '''Fit the model with the optimal p,d,q values'''
        #Grid Seearch Method
        ## This part only needs to be done once, if the values are saved
        '''
        best = pdq_values(self.training_data, self.testing_data)
        best_values = best.main()
        '''

        '''
        HARD CODED IN!!!!  (CHANGE LATER)
        '''
        model = sm.tsa.statespace.SARIMAX(self.training_data, order = (0,2,0),
                                        enforce_stationarity=False, enforce_invertibility=False)

        self.model_fit = model.fit(disp=0)


    def predict_future_values(self):
        '''
        Predict the future values
        '''
        pred_uc = self.model_fit.get_forecast(steps=120)
        pred_ci = pred_uc.conf_int()



        '''
        VISUALIZING IN MATPLOTLIB
        '''
        t = self.training_data.cumsum()
        t = t.fillna(0) + 2
        t = 10**t

        t = t /1.42
        print(self.data)
        pred_uc = pred_uc.conf_int(alpha=0.05)
        print(pred_uc)



        ax = t.plot(label='Observed', figsize=(16, 8), color='#006699')

        #pred_uc.predicted_mean.plot(ax=ax, label='Forecast', color='#ff0066');

        #ax.fill_between(pred_ci.index,
                        #pred_ci.iloc[:, 0],
                        #pred_ci.iloc[:, 1], color='#ff0066', alpha=.25);


        plt.show()


        sys.exit(0)

    def main(self):
        pass
