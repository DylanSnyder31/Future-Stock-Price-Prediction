from train_agent import training_parser
import json
from Make_Prediction.ARIMA import ARIMA_implementation
import sys

'''
To-Do:
    1. Training from visualization does not work
        A. Because the parsers believe no parser has been used
            I. The fact is that the parser --choice [stock] HAS been used
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
                optimal_values = current_dictionary[i]
                break

        if trained == False:
            print("")
            print("This stock has not been trained for. Do you want to do that now? [y/n]")
            answer = input()

            if answer.lower() == "y" or answer.lower() == "yes":
                train_stock = training_parser()
                train_stock.start_training()

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



    def show_graph(self):
        '''
        Shows the graph
        '''

    def main(self):
        optimal_values, stationary_data, data = self.get_stock_values()
        print("SDFHSDKJFHLKJSDF")
        sys.exit(0)
        predicted_values = self.predict_future_values(optimal_values, stationary_data, data)
