import numpy as np

def temp_solve(t_initial, c, data, rownumber, MODE_HVAC, n):

    ##########################################################
    # 1) This function calculates the nodal temperatures for rownumber given
    #       the known conditions for rownumber-1 (which is in the input 'data'
    #
    # 2) Calculations for nodal temperature in this function are made
    #       for rownumber row and NOT for rownumber+1
    #
    ################################################################

    t_w = np.zeros((1, n))  # T_w(n)=0; Preallocate an array of zeros

    for i in range(0, n):
        t_w[0][i] = t_initial[0][i]

    t_a = t_initial[0][n]
    t_m = t_initial[0][n + 1]
    t_inf = data[rownumber][2]
    u_inf = data[rownumber][7]
    q_s = data[rownumber][6]

    h_i = 5         # heat transfer coefficient inside the building (W / m2 - K)
    h_m = h_i
    if(data[rownumber][1] - data[rownumber - 1][1] == 0):
        dt = data[rownumber][1] - data[rownumber - 2][1]
    else:
        dt = data[rownumber][1] - data[rownumber - 1][1]
    Cp_a = 1000                                         # Specific heat capacity of air
    # % h_inf = 16.58 * u_inf + 1.37; % heat transfer coefficient outside the building (W / m2 - K)
    h_inf = 4 * u_inf + 5.6                             # h_inf = 4 * u_inf + 5.6; % W.Jurges correlation for the
    #print("c = " + str(c))                                                    # exterior of the bldgs (The heat transfer at a flat wall)
    # # # #    Energy balance for control volume 1   # # # #
    c_w = c[0]
    c_k = c[1]
    c_ACH = c[2]
    c_Aw = c[3]
    c_ma = 7.2 * c_Aw - 500
    c_Am = 8 * c_Aw

    c_HVAC = 0.5 * c_Aw ** 2
    c_Qint = 500
    c_MmCp = 1400 * 90 * c_Aw
    c_f = 0
    c_Rglass = 0
    c_sw = c[4]
    c_sg = 0

    A = np.zeros((n + 2, n + 2))  # Initialize A
    b = np.zeros((n + 2, 1))      # Initialize b

    A[0, 0] = h_inf + c_k + c_w / (2 * dt)
    A[0, 1] = -c_k

    # % b(1, 1)=h_inf * T_inf+q_s * 2 * c_sw+ c_w / (2 * dt) * T_w(1);

    b[0, 0] = h_inf * t_inf + q_s * c_sw + c_w / (2 * dt) * t_w[0][0]

    # # # #    Energy balances for internal control volumes    # # # #
    for j in range(1, n - 1):
        A[j, j] = 2 * c_k + c_w / dt
        A[j, j - 1] = -c_k
        A[j, j + 1] = -c_k
        b[j, 0] = c_w / dt * t_w[0][j]

    # # # #    Energy balance for control volume 'n'    # # # #
    A[n - 1, n - 1] = c_k + h_i + c_w / (2 * dt)
    A[n - 1, n - 2] = -c_k
    A[n - 1, n] = -h_i
    b[n - 1, 0] = c_w / (2 * dt) * t_w[0][n - 1]

    # # # #    Energy balance for control volume 'n+1' or 'Indoor air'    # # # #
    A[n, n] = c_ma * Cp_a / dt + h_i * c_Aw + h_m * c_Am + c_f * c_Aw / (
        1 / h_i + 1 / h_inf + c_Rglass) + c_ACH * c_ma * Cp_a / 3600 * (
        1 + u_inf)
    A[n, n - 1] = -h_i * c_Aw
    A[n, n + 1] = -h_m * c_Am
    b[n, 0] = c_HVAC * MODE_HVAC + c_Qint + q_s * c_sg + (c_f * c_Aw / (
        1 / h_i + 1 / h_inf + c_Rglass) + c_ACH * c_ma * Cp_a / 3600 * (
                                                              1 + u_inf)) * t_inf + c_ma * Cp_a / dt * t_a

    # # # #     Energy balance for control volume 'n+2'     # # # #
    A[n + 1, n + 1] = (c_MmCp / dt + h_m * c_Am)
    A[n + 1, n] = -h_m * c_Am
    b[n + 1, 0] = c_MmCp / dt * t_m

    X = np.linalg.solve(A, b)   # solve the system of linear equations and store in in X (which is returned by temp_solve
    return X   # end of TempSolve
