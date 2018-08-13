import sys
import argparse

from Data.stock_choices import list_of_stocks
from Visualize_Prediction.make_visualization import visualization

class visualize():
    '''
    The goal of this function is to use the user's arguments and provide a correct
    output
    '''
    def parser(self):
        '''
        The goal of this function is to add the necessary arguments to the parser
        '''
        visualize_parser = argparse.ArgumentParser()

        #Add the Arguments
        #   1. The user can choose if they want to see the predicted values for the stock or not
        #   2. The user can choose what stock they want to be displayed
        visualize_parser.add_argument('--data_display')
        visualize_parser.add_argument('--choice')

        self.arguments = visualize_parser.parse_args()

        stock_choice, type = self.data_from_arguments()
        return stock_choice, type

    def data_from_arguments(self):  
        '''
        The goal of this function is to read the input, and know what to do next
        '''
        #Check to see if the stock was an acceptable input
        length = len(list_of_stocks)
        for i in list_of_stocks:

            if self.arguments.choice == i:
                self.stock_choice = i
                # Break if the stock was acceptable
                break
            length -= 1

        #This gets activated if the stock input was not valid
        if length == 0:
            print("")
            print("Enter a valid stock!")
            sys.exit(0)

        # Decides if the user wants to see the forecasted values or not
        # Assigns that information to a global variable
        if self.arguments.data_display == "forecast":
            self.type = "forecast"
        elif self.arguments.data_display == "simple":
            self.type = "simple"

        else:
            #This activates if the user did not provide an acceptable input for the
            # --data_display argument
            print("Use one of these commands:")
            print("")
            print("--data_display [forecast] allows you to see the predicted prices,")
            print("--data_display [simple] allows you to see the normal prices")
            sys.exit(0)

        return self.stock_choice, self.type

if __name__ == "__main__":
    start_visualize = visualize()
    stock_choice, type = start_visualize.parser()

    #Calls a differnt file to visualize based on the information provided by the user
    show_visualization = visualization(stock_choice, type)
