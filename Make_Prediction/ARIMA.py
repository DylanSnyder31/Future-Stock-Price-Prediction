import csv
import math

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from pyramid.arima import auto_arimaself

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf

class ARIMA_implementation():

    def __init__(self):
        '''
        Reads the data
        '''
        self.read_data = pd.read_csv('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data\individual_stocks_5yr\AAPL_data.csv')
        self.data = self.read_data['open']

    def stationary(self):
        '''
        Makes data stationary, if not already
        '''
        loop = True
        while loop == True:
            result = adfuller(self.data)

            if result[1] > 0.05:
                #Make the data stationary

                #Log the data in order to fit it to a Gaussian Distribution
                self.data = self.data.apply(math.log10)

                #
                self.data = self.data.diff()
                self.data = self.data[~np.isnan(self.data)]

            else:
                print("Data is Stationary")

                #Plot the stationary data
                loop = False


    def fit_data(self):
        '''
        Fit the data
        '''

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
        print(rebuilt)
        print(r)
        k = pd.concat([rebuilt,r], axis=1)
        ax1.plot(k)

        plt.legend(loc='upper left');
        plt.show()


    def update_fit(self):
        updated_data = np.concatenate([self.data, self.next_25])



if __name__ == '__main__':
    a = ARIMA_implementation()
    a.stationary()
    a.fit_data()
    a.predict_future_values()
    #a.update_fit()
