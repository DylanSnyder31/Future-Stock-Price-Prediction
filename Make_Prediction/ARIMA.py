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
        try:
            self.read_data = pd.read_csv('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data\individual_stocks_5yr\%s_data.csv' %(str(stock_choice)) )
            self.data = self.read_data['open']

        except FileNotFoundError:
            self.read_data = pd.read_csv('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/all_stocks_5yr.csv')
            del self.read_data['date']
            del self.read_data['Name']

            station = stationary(self.read_data)
            self.read_data = station.smp500_data(self.read_data)

            self.data = self.read_data['open']

        #Make data stationary
        station = stationary(self.data)
        self.stationary_data = station.main()

        #split into training and testing data
        self.training_data = self.stationary_data[:int(int(len(self.stationary_data))*.7)]
        self.testing_data = self.stationary_data[int(int(len(self.stationary_data))*.7):]

    def is_data_fitted(self):

        try:
            with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as paramters:
                paramter_dictionary = json.load(paramters)
                for i in paramter_dictionary:
                    if str(i) == str(self.stock_choice):
                        print("")
                        print("This stock already has the optimal values, do you wish to continue? [y/n]")
                        user_preference = input()
                        if user_preference.lower() == "y" or user_preference.lower() == "yes":
                            return False
                        elif user_preference.lower() == "n" or user_preference.lower() == "no":
                            sys.exit(0)
                        else:
                            print("")
                            print("Enter a valid response.")
                            #Repeats the loop if asking the user

                            self.is_data_fitted()
                return False

        except json.decoder.JSONDecodeError:
            return False

    def fit_data(self):
        #See if user input is necessary
        self.is_data_fitted()

        best = pdq_values(self.training_data, self.testing_data)
        self.best_values = best.main()
        return self.best_values



    def main(self):
        ARIMA = ARIMA_implementation(self.stock_choice)
        self.best_values = ARIMA.fit_data()
        return self.best_values
