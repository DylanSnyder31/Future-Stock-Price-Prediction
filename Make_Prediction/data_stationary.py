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
        diff = np.log(y).diff().dropna()
        return diff

    def second_order_differencing(self, y):
        diff_2 = np.log(y).diff().diff(7).dropna()
        return diff_2


    def main(self):
        while self.test_for_nonstationary():
            self.test_for_nonstationary()
        return self.data
