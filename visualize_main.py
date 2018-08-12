import argparse
import sys
from Data.stock_choices import list_of_stocks
from Visualize_Prediction.make_visualization import visualization
'''
Take the values the user inputed, and output the correct grpah

Example:

    python visualize_main.py -APPL -Trained

This would then produce a graph of the APPL stock and the prediction the NN gave, along with the
other data I will include on the UI

* -Untrained will produce the normal graph, without any NN assisstance
* Can do this for every stock, as well as the S&P 500
'''

class visualize():

    def parser(self):
        visualize_parser = argparse.ArgumentParser()
        visualize_parser.add_argument('--data_display')
        visualize_parser.add_argument('--choice')
        self.arguments = visualize_parser.parse_args()

        stock_choice, type = self.data_from_arguments()
        return stock_choice, type

    def data_from_arguments(self):
        #Check to see if the stock was an acceptable input
        length = len(list_of_stocks)
        for i in list_of_stocks:

            if self.arguments.choice == i:
                self.stock_choice = i
                break
            length -= 1

        if length == 0:
            print("")
            print("Enter a valid stock!")
            sys.exit(0)


        if self.arguments.data_display == "forecast":
            self.type = "forecast"
        elif self.arguments.data_display == "simple":
            self.type = "simple"

        else:
            print("Use one of these commands:")
            print("")
            print("--data_display [forecast] allows you to see the predicted prices,")
            print("--data_display [simple] allows you to see the normal prices")
            sys.exit(0)

        return self.stock_choice, self.type

if __name__ == "__main__":
    start_visualize = visualize()
    stock_choice, type = start_visualize.parser()

    show_visualization = visualization(stock_choice, type)
