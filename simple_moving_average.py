#simple_moving_average
import numpy as np

#7 Day Moving Averasge
class SDSMA:

    # the array where the closing price over 7 days is stored
    def sma(self, x):
        m = np.mean(x)
        #m = the average of the array
        return m
