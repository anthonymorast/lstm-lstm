##########
#
# An implementation of popular error measurements.
# Will be used to compare the 'goodness' of models.
#
# Assume below that n = number obs, y = actual values,
# and hat(y) = predicted values.
##########

import  statsmodels as sm

#####
# Mean Error = sum_1^n(hat(y_i) - y_i)/n
#####
def MeanError(y, y_hat):
    n = len(y)
    if n != len(y_hat):
        print('Size of predicted values and actual values are not equal')
        return
    return float(sum([y_hat[i] - y[i] for i in range(0, n)])) / float(n)

#####
# Mean Absolute Error = sum_1^n(abs(hat(y_i) - y_i))/n
#####
def MeanAbsoluteError(y, y_hat):
    return sm.

#####
# Mean Squared Error = sum_1^n((hat(y_i) - y_i)^2)/n
#####

#####
# Root-Mean-Square Error = sqrt(Mean Squared Error)
#####

#####
# Mean Absolute Percentage Error = (100%/n) sum_1^n(abs((hat(y_i) - y_i)/y_i))
#####

#####
# Symmetric Mean Absolute Percentage Error = (100%/n) sum_1^n(abs(hat(y_i) - y_i)/(abs(y_i) + abs(hat(y_i))))
#####
