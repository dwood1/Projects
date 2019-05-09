def optimize(data, c_0, c_max, c_min, t_missing, startrow_trng, startrow_pred):
    from Greybox import error_to, normalizer as nor
    import numpy as np
    from scipy.optimize import minimize

    c_norm0 = nor.normalize_c(c_0, c_max, c_min)
    lb = c_min
    ub = c_max
    bnds = ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
    c_normie = [0.1299, 0.5688, 0.4694, 0.0119, 0.3371]

    # bnds = (lb, ub)
    fun = lambda c0: error_to.error_to(data, c0, c_max, c_min, t_missing, startrow_trng, startrow_pred)
    minimized = minimize(fun, c_norm0, method='SLSQP', bounds=bnds,
                          options={'disp': False, 'eps': 1.4901161193847656e-08,
                                   'maxiter': 2000, 'ftol': 1e-06})
    # minimized = minimize(fun, c_norm0, method='TNC', bounds=bnds,
    #                      options={'rescale': -1, 'gtol': -1,
    #                               'eps': 1e-08, 'eta': -1, 'maxiter': None, 'maxCGit': -1, 'ftol': -1,
    #                               'xtol': -1, 'stepmx': 0, 'accuracy': 0})


    [c_norm, error_trng] = [minimized.x, fun(minimized.x)]
    return [c_norm, error_trng]
