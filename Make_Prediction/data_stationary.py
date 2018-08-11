import numpy as np

from statsmodels.tsa.stattools import adfuller

class stationary():

    def __init__(self, data):
        self.data = data

    def test_for_nonstationary(self):
        first_order = True

        result = adfuller(self.data, autolag='AIC')

        if result[1] > 0.05 and result[1] > result[4]['5%']:

            if first_order:
                self.data = self.first_order_differencing(self.data)
                first_order = False

            else:
                self.data = self.second_order_differencing(self.data)

            return True
        else:
            return False

    def first_order_differencing(self, y):
        data = np.log(y).diff().dropna()
        return data

    def second_order_differencing(self, y):
        data_2 = np.log(y).diff().diff(7).dropna()
        return data_2


    def main(self):
        while self.test_for_nonstationary():
            self.test_for_nonstationary()
        return self.data

    def smp500_data(self, data):
        data = data.drop(data.index[82949])
        data = data.drop(data.index[165733])
        data = data.drop(data.index[165855])
        data = data.drop(data.index[205073])
        data = data.drop(data.index[239828])
        data = data.drop(data.index[434374])
        data = data.drop(data.index[434496])
        data = data.drop(data.index[478587])
        data = data.drop(data.index[558205])
        data = data.drop(data.index[581897])
        data = data.drop(data.index[598226])

        cleaned_data = data.astype(np.float64)
        return cleaned_data
