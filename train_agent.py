import sys
import json
import argparse

from Data.stock_choices import list_of_stocks
from Make_Prediction.ARIMA import ARIMA_implementation

class training_parser():
    '''
    The job of this class is to take the user's arguments as input and decide what
    should happen next
    '''

    def __init__(self):
        #Gets the list of stock names
        self.list_of_stocks = list_of_stocks

    def create_parser(self):
        '''
        The goal of this function is to create the parser
        '''
        self.training_parser = argparse.ArgumentParser()
        self.add_arguments()

    def add_arguments(self):
        '''
        The goal of this function is to add all necessary arguments to the parser
        '''
        #Allow user to choose what stock to train for
        self.training_parser.add_argument('--choice')

        #Allow the user to see a list of all available
        self.training_parser.add_argument('--list')

        #Allow the user to see what stocks already have optimal parameters trained for
        self.training_parser.add_argument('--trained')

        self.args = self.training_parser.parse_args()
        self.check_arguments()

    def check_arguments(self):
        '''
        The goal of this function is to take the users input and decide what the
        output should be. This is where the logic is held
        '''
        #Check to see if the stock was an acceptable input
        length = len(list_of_stocks)
        for i in list_of_stocks:
            if self.args.choice == i:
                self.stock_choice = i
                #If the stock was acceptable, break the loop
                break
            length -= 1

        if length == 0 and self.args.choice is not None:
            #This only happens when the stock was not a valid name
            print("")
            print("Enter a valid stock!")
            sys.exit(0)

        #This will show the list of stocks that are acceptable to train for
        if self.args.list == "show":
            print("")
            print("The list of stocks are: ")
            print("")
            print(list_of_stocks)
            sys.exit(0)

        #This wlil show the user the stocks that already have optimal variabels
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
            #Start the training
            self.start_training(self.stock_choice)
        except AttributeError:
            #This only happens when the user did not provide any arguments
            print("")
            print("""Use a command:
                    [--list show] prints off the list of available stocks
                    [--trained show] prints the stocks that already have been trainined for
                    [--choice *STOCK NAME*] allows you to train the model for a particular stock""")
            sys.exit(0)

    def start_training(self, stock_choice):
        '''
        The goal of this function is to start the training
        '''
        # Self.stock_choice is repeated because the visualize operation can call to train the stock, this allows the
        # Training process to know what stock to train for without adding additional functions
        self.stock_choice = stock_choice
        ARIMA = ARIMA_implementation(self.stock_choice)
        self.best_order = ARIMA.main()

        self.save_order()

    def save_order(self):
        '''
        The goal of this function is to save the optimal (p,d,q) values for future use
        '''
        #Saves the order to a JSON file
        with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json') as file_save:
            try:
                current_dictionary = json.load(file_save)
            except json.decoderself.JSONDecodeError:
                #This gets called if the JSON file is empty
                current_dictionary = {}

        with open('C:\Programming\Projects\Current GitHub Project\-MAKE-A-NAME-\Data/best_parameters.json', 'w') as file_save:
            #Saves the values
            current_dictionary[str(self.stock_choice)] = str(self.best_order)
            json.dump(current_dictionary, file_save)

    def main(self):
        '''
        The goal of this function is to start the whole process
        '''
        self.create_parser()

if __name__ == "__main__":
    train = training_parser()
    train.main()
