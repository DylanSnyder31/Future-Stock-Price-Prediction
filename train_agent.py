#Import necessary package for parsing the terminal
import argparse
import json
import sys
from Data.stock_choices import list_of_stocks
from Make_Prediction.ARIMA import ARIMA_implementation

'''
To-DO:
    1. Visualize the results
    2. Document the code
    3. Create the Juypter Notebook 'tutorial'
'''

class training_parser():

    def __init__(self):
        #Gets the list of stock names
        self.list_of_stocks = list_of_stocks


    def create_parser(self):
        self.training_parser = argparse.ArgumentParser()

        self.add_arguments()

    def add_arguments(self):
        #Allow user to choose what stock to train for
        self.training_parser.add_argument('--choice')

        #Allow the user to see a list of all available
        self.training_parser.add_argument('--list')

        #Allow the user to see what stocks already have optimal parameters trained for
        self.training_parser.add_argument('--trained')


        self.args = self.training_parser.parse_args()



        self.check_arguments()

    def check_arguments(self):

        #Check to see if the stock was an acceptable input
        length = len(list_of_stocks)
        for i in list_of_stocks:

            if self.args.choice == i:
                self.stock_choice = i
                break
            length -= 1

        if length == 0 and self.args.choice is not None:
            print("")
            print("Enter a valid stock!")
            sys.exit(0)

        if self.args.list == "show":
            print("")
            print("The list of stocks are: ")
            print("")
            print(list_of_stocks)
            sys.exit(0)

        if self.args.trained == "show":
            with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as file_save:
                try:
                    current_dictionary = json.load(file_save)
                except json.decoderself.JSONDecodeError:
                    current_dictionary = {}
            print("")
            print("Stocks that are already trainined for are:")
            print("")
            print('%s'%(current_dictionary))
            sys.exit()

        try:
            self.start_training(self.stock_choice)
        except AttributeError:
            print("")
            print("""Use a command:
                    [--list show] prints off the list of available stocks
                    [--trained show] prints the stocks that already have been trainined for
                    [--choice *STOCK NAME*] allows you to train the model for a particular stock""")
            sys.exit(0)
    def start_training(self, stock_choice):
        self.stock_choice = stock_choice
        ARIMA = ARIMA_implementation(self.stock_choice)

        self.best_order = ARIMA.main()

        self.save_order()
    def save_order(self):
        with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as file_save:
            try:
                current_dictionary = json.load(file_save)
            except json.decoderself.JSONDecodeError:
                current_dictionary = {}
        with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json', 'w') as file_save:
            current_dictionary[str(self.stock_choice)] = str(self.best_order)
            json.dump(current_dictionary, file_save)

    def main(self):
        self.create_parser()

if __name__ == "__main__":
    train = training_parser()
    train.main()
