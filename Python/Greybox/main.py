def main():
    import numpy as np
    from Greybox import unicon, normalizer, error_to, optimize, prediction_to, csv_formatter
    import matplotlib.pyplot as plt
    import csv
    from os import listdir, path
    import time
    import random

    # --------START Initializations-------#
    global itr
    itr = 0

    season = 'summer'  # 'summer' or 'winter'
    wb_result = 'no'  # 'yes' or 'no'

    date_start_pred = '2017-06-05 00:00:00'
    training_days = 2
    prediction_days = 10
    startrow = 0

    unix_start_pred = unicon.convert_date_to_unix_time(date_start_pred)
    unix_end_pred = unix_start_pred + (prediction_days * 3600 * 24)
    unix_start_trng = unix_start_pred - (3600 * 24 * training_days)

    temphys = [[0.5, 0], [0.5, 0]]  # np.matrix('0.5, 0; 0.5, 0')

    # Wall, Kw/dx, ACH, A_w, solar
    # a = random.randint(700, 10000)
    # b = random.randint(10, 197)
    # c = float(random.randint(15, 80))/100
    # d = random.randint(60, 380)
    # e = float(random.randint(5, 20))/100

    c_min = [700, 10, 0.15, 60, 0.05]
    c_max = [10000, 197, 0.8, 380, 0.2]
    c0 = [10000, 170, 0.5, 150,
          0.1]  # [1908.0699999999999, 116.3656, 0.45511000000000001, 63.808, 0.10056500000000002]  # [a, b, c, d, e]
    # print("c0 = " + str(c0))
    # Read in data, 'folderpath' should be where you store your data. 'filesname' reads in all the files located @
    # folderpath and the if statement filters out all non '.csv' files
    folderpath = 'C:/Users/dwood/Documents/Data/Thermodynamic Model/'  # location of data
    filesname = [f for f in listdir(folderpath) if path.splitext(f)[1] == '.csv']
    # --------END Initializations-------#

    num_files = len(filesname)  # number of data files in the folderpath that you wish to analyze
    result = np.zeros((num_files, 25))

    #If you want to read in and format Telemetry data files:
    telemetrypath = 'C:/Users/dwood/Documents/Data/Thermodynamic Model/pytest_in/'
    filesname_telemetry = [f for f in listdir(telemetrypath) if path.splitext(f)[1] == '.csv']
    savefile_loc = 'C:/Users/dwood/Documents/Data/Thermodynamic Model/python_test/'

    print(path.splitext(filesname_telemetry[0])[0])
    #Sift through every saved telemetry file in the telemetrypath and format it so it can be used, then save the result as a .csv in the folderpath
    # for i in range(0, len(filesname_telemetry)):
    #     csv_formatter.csv_formatter(telemetrypath + filesname_telemetry[i], savefile_loc, path.splitext(filesname_telemetry[i])[0], season)

    for i in range(0, 1):  # iterate through every file in 'filesname'
        #----------------------Data Initializations----------------------#
        # read in the data from the csv file and store it as a list, comment out if you wish to view formatted telemetry files
        #ifile = open(folderpath + filesname[i], newline='')
        #data = csv.reader(ifile)  # read in the current dataset as a 'csvreader' object


        # Reads in the formatted telemetry files, comment out if you wish to view other data
        ifile = open(savefile_loc + filesname_telemetry[i], newline='')
        data = csv.reader(ifile)  # read in the current dataset as a 'csvreader' object

        data_ghost = []  # Initialize a ghost list (will serve as a placeholder)

        # iterate through each row in data and create a list of lists which whill become data_ghost
        for row in data:
            data_ghost.append(row)

        # iterate through each sublist of data_ghost and fill any unfilled values with '0'
        for row in data_ghost:
            for val in row:
                if val == '':
                    val = 0

        # give the current dataset the attributes of data_ghost
        data = list(data_ghost)

        # convert all the string values of data into floats so that mathematical and logical operations can be carried
        # out
        data = [[float(j) for j in i] for i in data]
        #--------------------END data Initializations-----------------#


        #--------------------Timeline Initializations------------------#
        t_res = (data[198][1] - data[197][1]) #time resolution of data
        t_scale = (t_res) / (3600 * 24)
        t_trng = training_days / t_scale
        t_predicted = t_trng + (prediction_days/t_scale)
        t_missing = 1000

        # print("first date = " + str(unicon.convert_unix_to_date(data[0][1])))
        # print("final date = " + str(unicon.convert_unix_to_date(data[len(data) - 1][1])))
        print("start pred date = " + str(unicon.convert_unix_to_date(unicon.convert_date_to_unix_time(date_start_pred))))
        print("end pred date = " + str(unicon.convert_unix_to_date(unix_end_pred)))
        print("date_start_trng = " + str(unicon.convert_unix_to_date(unix_start_trng)))

        # if the data is sufficiently large to carry out prediction and training:
        if len(data) >= t_predicted:

            # date to unix conversion


            # for loop below to locate the first time step for the start_pred variable
            for j in range(0, len(data)):
                if data[j][1] >= unix_start_pred:
                    startrow_pred = j
                    break

            # put a scheme to validate that enough data is available for training
            for k in range(0, len(data)):
                if data[k][1] >= unix_start_trng:
                    startrow_trng = k
                    break

            # estimation of number of time steps for training
            t_trng = startrow_pred - startrow_trng

            # estimation of number of timesteps for prediction


            endrow_pred = 0
            for k in range(0, len(data)):

                if data[k][1] >= unix_end_pred:
                    endrow_pred = k + 1
                    break

            # startrow_pred = 99
            # endrow_pred = 399
            # startrow_trng = 0

            t_pred = endrow_pred - startrow_pred
            t_total = t_pred + t_trng
            t_scale = (training_days + prediction_days)/t_total

            #-------------------------------End Timeline Initializations-------------------------#

            # print("t_pred = " + str(t_pred))
            #----------------------------Optimization---------------------------#
            [c_norm, error_trng] = optimize.optimize(data, c0, c_max, c_min, t_missing,
                                                     startrow_trng, startrow_pred)

            print("c_norm = " + str(c_norm))
            # A = np.zeros(17, 1)
            # for k in range(0, 5):
            #     A[k, 0] = hessian[k, k]
            #     A[k + 6, 0] = lamb_da.lower(k)
            #     A[k + 12, 0] = lamb_da.upper(k)

            # print("c_norm = " + str(c_norm))
            # print("error_trng = " + str(error_trng))

            # Prediction
            cc = normalizer.denormalize_c(c_norm, c_max, c_min)
            t_a_measured = []
            t_a_set = []
            t_a_wb = []

            for k in range(startrow_trng, endrow_pred + 1):
                t_a_measured.append(data[k][3])
                t_a_set.append(data[k][4])
                #t_a_wb.append(data[k][8])

            [t_a_runtime, t_a_tempmode, error_t_runtimemode, error_t_tempmode, runtime_predicted,
             runtime_actual] = prediction_to.prediction_to(data, c_norm, c_max, c_min, temphys, season, t_missing,
                                                           startrow_trng, startrow_pred, endrow_pred)
            print("error_t_runtimemode = " + str(error_t_runtimemode))

            # -------------------------Plotting---------------------------#
            x1 = np.linspace(startrow_trng, startrow_pred,
                             (startrow_pred + 1) - startrow_trng)*t_scale  # akin to startrow_trng:1:startrow_pred in Matlab
            print("startrow_pred = " + str(startrow_pred))
            print("endrow_pred = " + str(endrow_pred))
            x2 = np.linspace(startrow_pred, endrow_pred, (endrow_pred + 1) - startrow_pred)*t_scale

            x3 = np.linspace(startrow_trng, endrow_pred, (endrow_pred + 1) - startrow_trng)*t_scale

            # Error calculation for this current model and wb model
            #runtime_wb = abs(sum(row[9] for row in data) * 5 / 60)

            # runtime_error_pct = (runtime_actual - runtime_predicted) / runtime_actual * 100
            # runtime_error_pct_wb = (runtime_actual - runtime_wb) / runtime_actual * 100

            t_a_runtime_list = [item for sublist in t_a_runtime for item in sublist]
            t_a_tempmode_list = [item for sublist in t_a_tempmode for item in sublist]

            if 'yes' in wb_result:
                plt.plot(x2, t_a_runtime_list, color='blue', linewidth=2.5, linestyle="-",
                         label="t_a_runtime")  # Plots all of the temperatures
                plt.plot(x3, t_a_measured, color='green', linewidth=2.5, linestyle="-", label="t_a_measured")
                plt.plot(x3, t_a_set, color='red', linewidth=2.5, linestyle="-", label="t_a_set")
                plt.plot(x1, t_a_wb, color='yellow', linewidth=2.5, linestyle="-", label="t_a_wb")
                plt.legend(loc='upper left')
                plt.show()

                # result[i][0] = error_trng
                # result[i][1] = error_t_tempmode
                # result[i][2] = error_t_runtimemode
                # result[i][3] = runtime_predicted
                # result[i][4] = runtime_actual
                # result[i][5] = runtime_error_pct
                # result[i][6] = runtime_wb
                # result[i][7] = runtime_error_pct_wb
            else:
                plt.plot(x2, t_a_runtime, color='blue', linewidth=2.5, linestyle="-", label="T model")
                plt.plot(x3, t_a_measured, color='red', linewidth=2.5, linestyle="-", label="T actual")
                plt.plot(x3, t_a_set, color='yellow', linewidth=2.5, linestyle="-", label="T set")
                plt.legend(loc='upper left')
                # print("i = " + str(i))
                figurename = path.splitext(filesname[i])[0][0:14]
                figuretitle = figurename + ': Measured vs Predicted Indoor Temperature'
                plt.title(figuretitle)
                plt.xlabel("Time (days)")
                plt.ylabel("Temperature (C)")
                plt.show()

            # result[i][6] = error_trng
            #     result[i][1] = error_t_tempmode
            #     result[i][2] = error_t_runtimemode
            #     result[i][4] = runtime_predicted
            #     result[i][3] = runtime_actual
            #     result[i][5] = runtime_error_pct
            # result[i][8: 12] = cc[0: 4]
            # result[i][12: 16] = c_norm[0: 4]
            # result[i][16: 20] = c_min[0: 4]
            # result[i][20: 24] = c_max[0: 4]
            # result[i][24] = t_trng



            # ----------------More Plotting--------------------------------#

            hvac_mode = [i[5] for i in
                         data[startrow_trng:startrow_pred + 1]]  # hvac_mode = data[startrow_trng:startrow_pred + 1][5]
            t_outdoor = [i[2] for i in
                         data[startrow_trng:endrow_pred + 1]]  # t_outdoor = data[startrow_trng:endrow_pred + 1][2]
            solar_irradiation = [i[6] for i in data[
                                               startrow_trng:endrow_pred + 1]]  # solar_irradiation = data[startrow_trng:endrow_pred + 1][6]
            solar_irradiation_fix = [x / 60 + 20 for x in solar_irradiation]  # scales solar irradiation

            # print("xx1 = " + str(len(xx1)))
            # print("xx2 = " + str(len(xx2)))
            # print("xx3 = " + str(len(xx3)))
            #
            # print("solar_irratiation_fix = " + str(len(solar_irratiation_fix)))
            # print("t_a_runtime_list = " + str(len(t_a_runtime_list)))
            # print("t_a_tempmode_list = " + str(len(t_a_tempmode_list)))
            # print("t_a_measured = " + str(len(t_a_measured)))
            # print("t_a_set = " + str(len(t_a_set)))
            # print("t_outdoor = " + str(len(t_outdoor)))
            # print("hvac_mode = " + str(len(hvac_mode)))
            # print(data)

            plt.plot(x2, t_a_runtime_list, color='blue', linewidth=2.5, linestyle="-", label="T runtime mode")
            plt.plot(x3, t_a_measured, color='red', linewidth=2.5, linestyle="-", label="T actual")
            plt.plot(x3, t_a_set, color='green', linewidth=2.5, linestyle="-", label="T set")
            plt.plot(x1, t_a_tempmode_list, color='purple', linewidth=2.5, linestyle="-", label="T tempmode")
            plt.plot(x1, hvac_mode, color='orange', linewidth=2.5, linestyle="-", label="MODE")
            plt.plot(x3, t_outdoor, color='cyan', linewidth=2.5, linestyle="-", label="T_outdoor")
            plt.plot(x3, solar_irradiation_fix, color='yellow', linewidth=2.5, linestyle="-", label="Sol_irr")
            plt.legend(loc="upper left")
            plt.show()

            # figuretitle = [figurename, ': Measured vs Predicted Indoor Temperature'];
            # title(figuretitle)
            # xlabel('time step')
            # ylabel('Temperature')

            # t_a_actual_tempmode = data[startrow_trng:startrow_pred + 1][3]

            # data[startrow_pred:endrow_pred][12] = t_a_runtime
            # data[startrow_trng:startrow_pred][13] = t_a_tempmode

            data_result = data[startrow_trng:endrow_pred][0:14]


main()
