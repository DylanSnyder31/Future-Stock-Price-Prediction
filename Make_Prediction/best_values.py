from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import warnings
class pdq_values():

    def __init__(self, train, test):
        self.training_data = train.astype('float32')
        self.testing_data = test.astype('float32')

        self.p = [0, 1, 2, 4, 6, 8, 10]
        self.d = range(0, 3)
        self.q = range(0, 3)



        warnings.filterwarnings("ignore")


    def evaluate_arima_model(self, order_values):
        data_steps = [x for x in self.training_data]
        predictions = list()
        for i in range(len(self.testing_data)):
            model = sm.tsa.statespace.SARIMAX(data_steps, order = order_values, enforce_stationarity=False, enforce_invertibility=False)
            model_fit = model.fit(disp=0)
            aic_score = model_fit.aic
            predictions.append(aic_score)
            data_steps.append(self.testing_data.iloc[i])

        # calculate out of sample error
        error = mean_squared_error(self.testing_data, predictions)
        return error

    def evaluate_models(self):

        lowest_error, best_order = float("inf"), None

        for p in self.p:
            for d in self.d:
                for q in self.q:
                    order_of_values = (p,d,q)
                    try:

                        error = self.evaluate_arima_model(order_of_values)
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
