def prediction_to(data, c_norm, c_max, c_min, temphys, season, t_missing, startrow_trng, startrow_pred, endrow_pred):
    import numpy as np
    import Greybox as gr

    # % % ** ** ** ** ** ** * Prediction code (RUNTIME MODE) ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    max_missing_duration = t_missing  # maximum duration of missing data to trigger the missing data sequence

    c = gr.normalizer.denormalize_c(c_norm, c_max, c_min)
    t_pred = endrow_pred - startrow_pred + 1
    T_a_runtime = np.zeros((t_pred, 1))

    T_a_set = np.zeros((t_pred, 1))
    Error_T_runtimemode = 0

    n = 20

    T = gr.initialize.initialize(data[startrow_pred][2], data[startrow_pred][3], n)
    T_a_runtime[0] = T[0, n]

    MODE_HVAC = 0
    MODE_HVAC_actual = 0
    runtime_predicted = 0
    runtime_actual = 0

    for j in range(1, t_pred):

        rownumber = j + startrow_pred - 1
        T_a_set[j][0] = data[rownumber][4]

        if (data[rownumber][1] - data[rownumber - 1][1]) >= max_missing_duration:

            T = gr.initialize.initialize(data[rownumber][2], data[rownumber][3], n)
            T_a_runtime[j] = T[0, n]
            MODE_HVAC = data[rownumber][5]

        else:

            if season == 'summer':

                if T_a_runtime[j - 1] >= (data[rownumber][4] + temphys[0][0]):
                    MODE_HVAC = -1

                if MODE_HVAC == -1 and T_a_runtime[j - 1] < (data[rownumber][4] - temphys[0][1]):
                    MODE_HVAC = 0

            else:

                if T_a_runtime[j - 1] <= (data[rownumber][4] - temphys[1][0]):
                    MODE_HVAC = 1

                if MODE_HVAC == 1 and T_a_runtime[j - 1] >= (data[rownumber][4] + temphys[1][1]):
                    MODE_HVAC = 0

            Z = gr.temp_solve.temp_solve(T, c, data, rownumber, MODE_HVAC, n)
            T = np.transpose(Z)
            T_a_runtime[j] = T[0, n]

            if data[rownumber][5] == data[rownumber - 1][5]:
                MODE_HVAC_actual = data[rownumber][5]
            else:
                MODE_HVAC_actual = data[rownumber - 1][5]

            runtime_predicted = runtime_predicted + abs(MODE_HVAC * (data[j][1] - data[j - 1][1]) / 3600)
            runtime_actual = runtime_actual + abs(MODE_HVAC_actual * (data[j][1] - data[j - 1][1]) / 3600)

        e = (abs(T_a_runtime[j] - data[rownumber][3])) / data[rownumber][3]
        Error_T_runtimemode = e + Error_T_runtimemode

    Error_T_runtimemode = Error_T_runtimemode / t_pred * 100
    T_a_runtime[0] = data[startrow_pred - 1][3]

    # % TEMPERATURE PREDICTION MODE
    #
    # % % ** ** ** ** ** ** * Training code (Temp prediction MODE) ** ** ** ** ** **  ** *
    t_trng = startrow_pred - startrow_trng + 1


    T_a_tempmode = np.zeros((t_trng, 1))  # preallocating memory for variable
    Error_T_tempmode = 0
    T = gr.initialize.initialize(data[startrow_trng - 1][2], data[startrow_trng - 1][3], n)

    for j in range(1, t_trng):

        rownumber = j + startrow_trng - 1

        if (data[rownumber][1] - data[rownumber - 1][1]) >= max_missing_duration:
            T = gr.initialize.initialize(data[rownumber][2], data[rownumber][3], n)
            T_a_tempmode[j] = T[0, n]

        else:
            if data[rownumber][5] == data[rownumber - 1][5]:
                MODE_HVAC2 = data[rownumber][5]

            else:
                MODE_HVAC2 = data[rownumber - 1][5]


            Z = gr.temp_solve.temp_solve(T, c, data, rownumber, MODE_HVAC2, n)
            T = np.transpose(Z)

            T_a_tempmode[j] = T[0, n]

            e2 = (abs(T_a_tempmode[j] - data[rownumber][3])) / data[rownumber][3]
            Error_T_tempmode = e2 + Error_T_tempmode

    Error_T_tempmode = Error_T_tempmode / t_trng * 100
    T_a_tempmode[0] = data[startrow_trng][3]
    return T_a_runtime, T_a_tempmode, Error_T_runtimemode, Error_T_tempmode, runtime_predicted, runtime_actual
    # end of PredictionTo
