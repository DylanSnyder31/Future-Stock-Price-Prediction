import sys
import json

import statsmodels.api as sm
import matplotlib.pyplot as plt

from train_agent import training_parser
from Make_Prediction.ARIMA import ARIMA_implementation

class visualization():
    '''
    The goal of this class is to visualize the data
    '''
    def __init__(self, stock_choice, type):
        self.stock_choice = stock_choice
        self.type = type

        self.main()

    def get_stock_values(self):
        '''
        The goal of this function is to return optimal values
        '''
        #Gets the dictionary of values that were saved to the JSON file
        with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as file_save:
            try:
                current_dictionary = json.load(file_save)
            except json.decoderself.JSONDecodeError:
                current_dictionary = {}

        trained = False
        #Loop through the dictionary to see if the stock has saved values
        for i in current_dictionary:
            #The stock has optimal values
            if str(i) == str(self.stock_choice):
                trained = True

                optimal_values_string = current_dictionary[i]
                p = int(optimal_values_string[1])
                d = int(optimal_values_string[4])
                q = int(optimal_values_string[7])

                optimal_values = (p,d,q)
                break

        #The stock does NOT have optimal values
        if trained == False:
            # Ask the user if they would like to train the stock
            # This is because if the stock has not optimal values, then
            # It has not been trainined for, and could be done now

            print("")
            print("This stock has not been trained for. Do you want to do that now? [y/n]")
            answer = input()

            if answer.lower() == "y" or answer.lower() == "yes":
                train_stock = training_parser()
                train_stock.start_training(self.stock_choice)

            elif answer.lower() == "n" or answer.lower() == "no":
                sys.exit(0)

            else:
                print("")
                print("Enter a valid response.")
                #Repeats the loop if asking the user

                self.get_stock_values()

        else:
            #Continue through the Hierarchy of visualizing the data
            data = ARIMA_implementation(self.stock_choice)
            stationary_data, data = data.get_data()
            return optimal_values, stationary_data, data



    def predict_future_values(self, optimal_values, stationary_data, data):
        '''
        The goal of this function is to get and return predicted values
        '''
        self.data_length = len(data)
        self.data = data
        self.number_of_predictions = 600

        updated_data = [x for x in stationary_data]
        predictions = []

        for i in range(self.number_of_predictions):
            model = sm.tsa.statespace.SARIMAX(updated_data, order = optimal_values)
            model_fit = model.fit(disp=0)
            forecast = model_fit.forecast(1)[0]
            updated_data.append(forecast)

            predictions.append(forecast)

        return predictions, updated_data

    def show_graph(self, predicted_values, data_with_predictions):
        '''
        Shows the graph
        '''
        predicted_data = []
        full_data = [x for x in self.data]
        index = len(full_data) - 1
        for i in range(self.number_of_predictions):
            value = (full_data[index] + predicted_values[i])
            full_data.append(value)
            predicted_data.append(value)
        plt.plot(self.data)
        plt.plot(predicted_data)
        plt.show()

    def main(self):
        optimal_values, stationary_data, data = self.get_stock_values()
        predicted_values, data_with_predictions = self.predict_future_values(optimal_values, stationary_data, data)

        self.show_graph(predicted_values, data_with_predictions)
