import warnings

import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

class pdq_values():
    '''
    The goal of this function is to use grid search in order to find the optimal
    values for p,d,q;

    These values play a crucial role in fitting the ARIMA model to data
    '''
    def __init__(self, train, test):
        warnings.filterwarnings("ignore")

        #Set the data to float32
        self.training_data = train.astype('float32')
        self.testing_data = test.astype('float32')

        #Define all possible p,d,q values
        self.p = [0, 1, 2, 4, 6, 8, 10]
        self.d = range(0, 3)
        self.q = range(0, 3)

    def evaluate_arima_model(self, order_values):
        '''
        The goal of this function is to evaluate a specific combination of p,d,q values;
        Returns the mean_squared_error
        '''
        data_steps = [x for x in self.training_data]
        predictions = list()

        for i in range(len(self.testing_data)):
            '''
            This loop used SARIMAX to make a prediction for the next value of the dataset,
            for the length of the testing_data. Then the testing_data and the predictions are
            compared and the error is calculated
            '''
            #Make and fit the model
            model = sm.tsa.statespace.SARIMAX(data_steps, order = order_values, enforce_stationarity=False, enforce_invertibility=False)
            model_fit = model.fit(disp=0)
            score = model_fit.aic
            predictions.append(score)
            data_steps.append(self.testing_data.iloc[i])

        # Calculate and return the error
        error = mean_squared_error(self.testing_data, predictions)
        return error

    def evaluate_models(self):
        '''
        The goal of this function is to test ALL combinations of p,d,q and find
        the best one. This is accomplished by iterating through all possible combinations
        and then using the evaluate_arima_model() function to get the error
        '''

        lowest_error, best_order = float("inf"), None

        for p in self.p:
            for d in self.d:
                for q in self.q:
                    #What the current order of values is
                    order_of_values = (p,d,q)
                    try:
                        error = self.evaluate_arima_model(order_of_values)

                        #See if the error is lower than the lowest error
                        if error < lowest_error:
                            lowest_error, best_order = error, order_of_values

                        print('ARIMA: %s error=%.3f' % (order_of_values,error))
                    except:
                        continue

            print('Best ARIMA: %s error=%.3f' % (best_order,lowest_error))

        return best_order

    def main(self):
        order = self.evaluate_models()
        return order
