from statsmodels.tsa.arima_model import ARIMA
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
    def evaluate_arima_model(self, arima_order):
        # prepare training dataset

        history = [x for x in self.training_data]

        # make predictions
        predictions = list()
        for t in range(len(self.testing_data)):
            model = sm.tsa.statespace.SARIMAX(history, order = arima_order,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
            model_fit = model.fit(disp=0)
            yhat = model_fit.aic
            predictions.append(yhat)
            history.append(self.testing_data.iloc[t])
        # calculate out of sample error
        error = mean_squared_error(self.testing_data, predictions)
        return error

    # evaluate combinations of p, d and q values for an ARIMA model
    def evaluate_models(self):

        best_score, best_cfg = float("inf"), None

        for p in self.p:
            for d in self.d:
                for q in self.q:
                    order = (p,d,q)
                    try:
                        mse = self.evaluate_arima_model(order)
                        if mse < best_score:
                            best_score, best_cfg = mse, order
                        print('ARIMA%s MSE=%.3f' % (order,mse))
                    except:
                        continue

        print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
        return best_cfg
    def main(self):
        self.evaluate_models()
        return 1,1,1
