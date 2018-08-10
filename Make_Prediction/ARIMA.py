import csv
import math
import itertools
import pandas as pd
import numpy as np
import json
import sys
from pyramid.arima import auto_arima
import statsmodels.api as sm

from Make_Prediction.data_stationary import stationary
from Make_Prediction.best_values import pdq_values

class ARIMA_implementation():

    def __init__(self, stock_choice):
        self.stock_choice = stock_choice
        #Get the data
        self.read_data = pd.read_csv('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data\individual_stocks_5yr\%s_data.csv' %(str(stock_choice)) )
        self.data = self.read_data['open']

        #Make data stationary
        station = stationary(self.data)
        self.stationary_data = station.main()

        #split into training and testing data
        self.training_data = self.stationary_data[:int(int(len(self.stationary_data))*.7)]
        self.testing_data = self.stationary_data[int(int(len(self.stationary_data))*.7):]

    def is_data_fitted(self):
        #Return False if the data needs to be fitted; True if not needed to be fitted
        try:
            with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as paramters:
                paramter_dictionary = json.load(paramters)
                for i in paramter_dictionary:
                    if str(i) == str(self.stock_choice):
                        print("")
                        print("This stock already has the optimal values, do you wish to continue? [y/n]")
                        user_preference = input()
                        if user_preference.lower() == "y" or "yes":
                            return False
                        elif user_preference.lower() == "n" or "no":
                            return True
                        else:
                            print("")
                            print("Enter a valid response.")
                            
                return False

        except json.decoder.JSONDecodeError:
            return False

    def fit_data(self):

        if self.is_data_fitted():
            sys.exit(0)

        best = pdq_values(self.training_data, self.testing_data)
        self.best_values = best.main()
        return self.best_values



    def main(self):
        ARIMA = ARIMA_implementation(self.stock_choice)
        self.best_values = ARIMA.fit_data()
        return self.best_values
