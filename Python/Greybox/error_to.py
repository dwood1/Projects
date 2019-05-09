import numpy as np
from Greybox import temp_solve, initialize, normalizer as nor


def error_to(data, c_norm, c_max, c_min, t_missing, startrow_trng,
             startrow_pred):
    # main.itr = main.itr + 1
    # print(main.itr)
    # The code is designed to take the first data as starting point and not t_strt.
    # Change the code to accomodate the starting point provided by the user.

    # Initial nodal temperature distribution
    n = 20  # number of node points
    T = initialize.initialize(data[startrow_trng][2], data[startrow_trng][3], n)
    c = nor.denormalize_c(c_norm, c_max, c_min)

    error = 0
    error_abs = 0

    max_missing_duration = t_missing  # seconds, maximum duration of missing data to trigger the missing data
    # sequence

    t_trng = startrow_pred - startrow_trng + 1

    for j in range(1, t_trng):
        rownumber = j + startrow_trng - 1

        if (data[rownumber][1] - data[rownumber - 1][1]) >= max_missing_duration:
            T = initialize.initialize(data[rownumber][2], data[rownumber][3], n)
            if data[rownumber][5] == data[rownumber - 1][5]:
                MODE_HVAC = data[rownumber][5]
            else:  # else
                MODE_HVAC = data[rownumber - 1][5]
        else:
            # Taking care of data recording issues arising due to the recording only when there is a change.
            # (only the change value is shown and not the previous value)
            if data[rownumber][5] == data[rownumber - 1][5]:
                MODE_HVAC = data[rownumber][5]
            else:  # else
                MODE_HVAC = data[rownumber - 1][5]


        Z = temp_solve.temp_solve(T, c, data, rownumber, MODE_HVAC, n)
        T = np.transpose(Z)  # T=Z.';
        T_a = T[0][n]  # T_a=T(1, n+1);
        T_a_measured = data[rownumber][3]  # T_a_measured=data(rownumber, 4);
        e = abs(T_a - T_a_measured)  # e = abs(T_a - T_a_measured) # e=abs(T_a-T_a_measured);
        error = e + abs(error)  # Error = e + abs(Error)  # Error=e+abs(Error);
        error_abs = abs(error)  # Error_abs=abs(Error);
    return error_abs  # end
