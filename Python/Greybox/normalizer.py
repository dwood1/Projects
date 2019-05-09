# # filename: normalizer
# # holds the normalize, normalize_c, denormalize, and denormalize_c functions
#

import numpy as np


def denormalize(normalized, min1, max1):
    x = normalized * (max1 - min1) + min1
    return x


def normalize(value, min1, max1):
    x = (value - min1) / (max1 - min1)
    return x


def normalize_c(c, c_max, c_min):
    n = len(c)
    c_norm = np.zeros((1, n))
    for i in range(0, n):
        c_norm[0,i] = (c[i] - c_min[i]) / (c_max[i] - c_min[i])
    c_norm = [i for i in c_norm[0]]
    return c_norm


def denormalize_c(c_norm, c_max, c_min):
    #print("c_norm = "+str(c_norm), "c_max = "+str(c_max), "c_min = "+str(c_min))
    n = len(c_norm)
    c = np.zeros((1, n))

    for i in range(0, n):
        c[0][i] = c_norm[i] * (c_max[i] - c_min[i]) + c_min[i]

    c = [i for i in c[0]]
    #print("c = " + str(c))
    return c

