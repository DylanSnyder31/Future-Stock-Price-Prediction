from train_agent import training_parser
import json
from Make_Prediction.ARIMA import ARIMA_implementation
import sys
import statsmodels.api as sm
import matplotlib.pyplot as plt

'''
To-DO:
    1. Make number of predictions an argument for the user
'''
class visualization():

    def __init__(self, stock_choice, type):

        self.stock_choice = stock_choice
        self.type = type

        self.main()

    def get_stock_values(self):
        '''
        returns optimal values
        '''

        with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as file_save:
            try:
                current_dictionary = json.load(file_save)
            except json.decoderself.JSONDecodeError:
                current_dictionary = {}

        trained = False
        for i in current_dictionary:
            if str(i) == str(self.stock_choice):
                trained = True
                optimal_values_string = current_dictionary[i]

                p = int(optimal_values_string[1])
                d = int(optimal_values_string[4])
                q = int(optimal_values_string[7])

                optimal_values = (p,d,q)

                break

        if trained == False:
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
            data = ARIMA_implementation(self.stock_choice)
            stationary_data, data = data.get_data()
            return optimal_values, stationary_data, data



    def predict_future_values(self, optimal_values, stationary_data, data):
        '''
        returns predicted values
        '''
        number_of_predictions = 60

        updated_data = [x for x in stationary_data]
        predictions = []
        for i in range(number_of_predictions):
            model = sm.tsa.statespace.SARIMAX(updated_data, order = optimal_values)
            model_fit = model.fit(disp=0)
            forecast = model_fit.forecast()[0]
            updated_data.append(forecast)
            predictions.append(forecast)

        return predictions, updated_data

    def show_graph(self, predicted_values, data_with_predictions):
        '''
        Shows the graph
        '''
        plt.plot(data_with_predictions)
        plt.plot(predicted_values)
        plt.show()

    def main(self):
        optimal_values, stationary_data, data = self.get_stock_values()
        predicted_values, data_with_predictions = self.predict_future_values(optimal_values, stationary_data, data)

        self.show_graph(predicted_values, data_with_predictions)
