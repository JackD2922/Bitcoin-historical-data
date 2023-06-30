#Relative Strength Index

import numpy as np

class FourteenDayRSI:
    def rsi(self, closing_price):
        change = np.zeros(14)
        for i in range(13):
            change[i] = closing_price[i+1] - closing_price[i]
        
        gains = np.where(change >= 0, change, 0)
        losses = np.where(change < 0, -change, 0)
        
        average_gain = np.mean(gains)
        average_loss = np.mean(losses)
        
        if average_loss == 0:
            rsi = 100
        else:
            rs = average_gain / average_loss
            rsi = 100 - (100 / (1 + rs))
        
        return rsi