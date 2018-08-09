#Import necessary package for parsing the terminal
import argparse

import sys
from Data.stock_choices import list_of_stocks
from Make_Prediction.ARIMA import ARIMA_implementation
class training_parser():

    def __init__(self):
        #Gets the list of stock names
        self.list_of_stocks = list_of_stocks

        self.create_parser()

    def create_parser(self):
        self.training_parser = argparse.ArgumentParser()

        self.add_arguments()

    def add_arguments(self):
        #Allow user to choose what stock to train for
        self.training_parser.add_argument('--choice')

        #Allow the user to see a list of all available
        self.training_parser.add_argument('--list')

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


        self.start_training()

    def start_training(self):

        ARIMA = ARIMA_implementation(self.stock_choice)
        self.best_order = ARIMA.main()

    def save_order(self):
        '''
        SAVE THE BEST ORDER
        '''


if __name__ == "__main__":
    train = training_parser()
