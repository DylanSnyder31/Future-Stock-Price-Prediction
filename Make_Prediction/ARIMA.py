import sys
import json

import numpy as np
import pandas as pd
import statsmodels.api as sm

from Make_Prediction.data_stationary import stationary
from Make_Prediction.best_values import pdq_values

class ARIMA_implementation():
    '''
    The goal of this funciton is to provide an ARIMA implementation in python
    '''
    def __init__(self, stock_choice):
        '''
        The goal of this __init__ function is to get the training and testing data based
        on the stock that was chosen by the user
        '''
        self.stock_choice = stock_choice
        #Get the data
        try:
            self.read_data = pd.read_csv('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data\individual_stocks_5yr\%s_data.csv' %(str(stock_choice)) )
            self.data = self.read_data['open']
        except FileNotFoundError:
            # This only activates if the data that was called for was the SMP500 as a whole, not an individual stock
            self.read_data = pd.read_csv('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/all_stocks_5yr.csv')

            #Delete unecessary columns
            del self.read_data['date']
            del self.read_data['Name']

            #Rremove unecssary rows
            #!! This does NOT stationize the data
            station = stationary(self.read_data)
            self.read_data = station.smp500_data(self.read_data)

            #Only view the important row (for this application)
            self.data = self.read_data['open']

        #Make data stationary
        station = stationary(self.data)
        self.stationary_data = station.main()

        #split into training and testing data
        self.training_data = self.stationary_data[:int(int(len(self.stationary_data))*.7)]
        self.testing_data = self.stationary_data[int(int(len(self.stationary_data))*.7):]

    def is_data_fitted(self):
        '''
        The goal of this funciton is see if the chosen stock already has optimal values
        If it does, the function will ask the user if they wish to re-train for this stock
        '''

        try:
            with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as paramters:
                #Get the dictionary
                paramter_dictionary = json.load(paramters)

                #Search the dictionary for the chosen stock
                for i in paramter_dictionary:

                    #If the stock has been found
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

                            #Ask the user again;
                            #Response was not valid
                            self.is_data_fitted()

                return False

        except json.decoder.JSONDecodeError:
            #If the dictionary is empty; The stock does not have optimal values
            return False

    def fit_data(self):
        '''
        The goal of this function is to get the optimal values for the data
        '''
        #See if user input is necessary
        self.is_data_fitted()

        #Call another file in order to get the best values
        best = pdq_values(self.training_data, self.testing_data)
        self.best_values = best.main()

        return self.best_values

    def get_data(self):
        '''
        The goal of this funciton is to make it easier to recieve the data from
        another file
        '''
        return self.stationary_data, self.data

    def main(self):
        ARIMA = ARIMA_implementation(self.stock_choice)
        self.best_values = ARIMA.fit_data()

        return self.best_values
