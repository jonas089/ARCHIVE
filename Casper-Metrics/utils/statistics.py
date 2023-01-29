import numpy as np
def mean(arr):
    sum = 0
    for v in arr:
        sum += v
    return sum/len(arr)

def median(arr):
    return np.median(arr)

def average_deploy_cost_per_month(data_by_month):
    y = []
    for key in data_by_month:
        total_cost = 0
        for value in data_by_month[key]:
            total_cost += int(value)

        average_cost = total_cost/len(data_by_month[key])
        y.append(average_cost)

    #################################################################
    # def generate(x_arr, y_arr, x_label, y_label, path, filename): #
    #################################################################
    for i in range(0, len(y)):
        y[i] = (y[i] / 1000000000)
    return y
