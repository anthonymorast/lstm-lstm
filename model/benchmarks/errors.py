##########
#
# An implementation of popular error measurements.
# Will be used to compare the 'goodness' of models.
#
# Assume below that n = number obs, y = actual values,
# and hat(y) = predicted values.
##########

from sklearn import metrics
from math import sqrt

#####
# Mean Error = sum_1^n(hat(y_i) - y_i)/n
#####
def me(y, y_hat):
    n = len(y)
    if n != len(y_hat):
        print('Size of predicted values and actual values are not equal')
    return float(sum([y_hat[i] - y[i] for i in range(0, n)])) / float(n)


#####
# Mean Absolute Error = sum_1^n(abs(hat(y_i) - y_i))/n
#####
def mae(y, y_hat):
    return metrics.mean_absolute_error(y, y_hat)


#####
# Mean Squared Error = sum_1^n((hat(y_i) - y_i)^2)/n
#####
def mse(y, y_hat):
    return metrics.mean_squared_error(y, y_hat)


#####
# Root Mean Squared Error = sqrt(Mean Squared Error)
#####
def RootMse(y, y_hat):
    e = mse(y, y_hat)
    return sqrt(e)


#####
# Mean Absolute Percentage Error = (100%/n) sum_1^n(abs((hat(y_i) - y_i)/y_i))
#####
def mape(y, y_hat):
    n = len(y)
    if len(y) != len(y_hat):
        print('Size of predicted values and actual values are not equal')
        return
    t = 0
    for i in range(0, n):
        t = t + abs((y_hat[i] - y[i]) / y[i])
    t = t/n
    return t*100


#####
# Symmetric Mean Absolute Percentage Error = (100%/n) sum_1^n(abs(hat(y_i) - y_i)/(abs(y_i) + abs(hat(y_i))))
#####
def smape(y, y_hat):
    n = len(y)
    if len(y) != len(y_hat):
        print('Size of predicted values and actual values are not equal')
        return
    t = 0
    for i in range(0, n):
        t = t + (abs(y_hat[i] - y[i]))/(abs(y[i]) + abs(y_hat[i]))
    t = t/n
    return t*100
