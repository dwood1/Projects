import numpy as np


tars = np.zeros((10, 50))
scoop = np.ndarray.tolist(tars)

scoop[2][5] = "kipper"
print(scoop)