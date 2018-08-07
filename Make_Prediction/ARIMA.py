import csv
import math

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from pyramid.arima import auto_arima

import statsmodels.api as sm


from data_stationary import stationary

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
        

    def fit_data(self):

        self.d = auto_arima(self.data, start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=False, d=1, D=1, trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

        #print(self.stepwise_fit.summary())


    def predict_future_values(self):
        '''
        Predict the future values
        '''

        self.next_25 = self.d.predict(n_periods=2025)
        print(self.next_25)
        dataset = pd.DataFrame({'Column1':self.next_25})
        #print(dataset)

        fig = plt.figure()
        ax1 = fig.add_subplot(111)


        a_diff_cumsum = self.data.cumsum()


        rebuilt = a_diff_cumsum.fillna(0) + 2
        rebuilt = 10**rebuilt
        rebuilt = rebuilt * 0.6771419996315278


        a = dataset.cumsum()


        r = a.fillna(0) + 2
        r = 10**r
        r = r * 0.6771419996315278
        k = pd.concat([rebuilt,r], axis=1)
        ax1.plot(k)

        plt.legend(loc='upper left');
        plt.show()


    def update_fit(self):
        updated_data = np.concatenate([self.data, self.next_25])



if __name__ == '__main__':
    a = ARIMA_implementation()
    a.fit_data()
    a.predict_future_values()
    #a.update_fit()
