# filename: Initialize

def initialize(T_inf, T_a, n):
    import numpy as np
    T = np.zeros((1, n+2))           # Preallocate memory by establishing array of zeroes
    for i in range(0, n):
        T[0][i] = T_inf - (T_inf - T_a) / (n - 1) * i

    T[0][n] = T_a
    T[0][n+1] = T_a

    return T