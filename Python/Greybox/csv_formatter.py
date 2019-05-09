#   filename: csv_formatter
#   package: Greybox
#   Author: David Wood (July 20, 2017)
#   Converts input (CSV file with appropriate headers) from the Earth Networks Telemetry Report system
#   and saves a new csv file in the specified folder that is properly formatted
#   into the following format to allow it to be used by the modeling script:
#  ['',Unix Time, 'Outdoor Temp', 'Indoor Temp', 'Tstat Setpoint', 'HVAC Mode', 'Solar Irradiation', 'Wind Speed']
# requires the following mapping:
# ------

import csv
import numpy as np
from Greybox import unicon


def csv_formatter(file, save_location, savefile_name, season):
    ifile = open(file, newline='')
    data = csv.reader(ifile)

    # Read through the headers of each column to identify what data is where in the input CSV file
    data_ghost = []

    for row in data:
        data_ghost.append(row)

    for row in data_ghost:
        for val in row:
            if val == '':
                val = 0

    data = list(data_ghost)
    good_data = []


    # --datetime, coolset, heatset, solirr, tempIN, tempOUT, windspeed, humidity, coolinterval, heatinterval--#
    input_headers_loc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    count = 0 #identifies how many rows are nonzero
    # This loop maps out the location of each column of interest from the input file (Make sure the headers match!)
    for i in range(0, len(data[0])):

        if (data[0][i] == 'TargetCoolSetPoint'):
            input_headers_loc[1] = i

        if (data[0][i] == 'TargetHeatSetPoint'):
            input_headers_loc[2] = i

        if (data[0][i] == 'CoolIntervalMinutes'):
            input_headers_loc[8] = i
            for k in range(1, len(data)):
                if data[k][i] != '':
                    data[k][i] = float(data[k][i])
                if data[k][i] != 0:
                    count = count + 1

        if (data[0][i] == 'HeatIntervalMinutes'):
            input_headers_loc[9] = i
            for k in range(1, len(data)):
                if data[k][i] != '':
                    data[k][i] = float(data[k][i])
                if data[k][i] != 0:
                    count = count + 1

        if (data[0][i] == 'DateTimeLocal'):
            input_headers_loc[0] = i

        if (data[0][i] == 'OutdoorTemp'):
            input_headers_loc[5] = i

        if (data[0][i] == 'IndoorTemp'):
            input_headers_loc[4] = i

        if (data[0][i] == 'SolarIrradiance'):
            input_headers_loc[3] = i

        if (data[0][i] == 'WindSpeedMps'):
            input_headers_loc[6] = i

        if (data[0][i] == 'OutdoorHumidity'):
            input_headers_loc[7] = i

            # resolve NA's and missing numbers
    for row in range(0, len(data)):
        flag = False
        for element in input_headers_loc:
            if data[row][element] == '':
                flag = True
        if flag == False:
            good_data.append(data[row])

    data = good_data


    data_place = np.zeros((len(data)-1 + count, 8))
    data_place = np.ndarray.tolist(data_place)
    #print(unicon.convert_telemetry_date_to_unix_time(data[1][input_headers_loc[0]])+50)
    #print(data[1][input_headers_loc[8]])

    #Formats the file, taking into account delta data
    row = 0
    for i in range(1, len(data)):
        #print("i = " + str(i))
        data_place[row][0] = 0
        data_place[row][1] = unicon.convert_telemetry_date_to_unix_time(data[i][input_headers_loc[0]])
        data_place[row][2] = data[i][input_headers_loc[5]]
        data_place[row][3] = data[i][input_headers_loc[4]]
        data_place[row][6] = data[i][input_headers_loc[3]]
        data_place[row][7] = data[i][input_headers_loc[6]]
        if season == 'summer':
            data_place[row][4] = data[i][input_headers_loc[1]]

            if data[i][input_headers_loc[8]] == 0:
                data_place[row][5] = 0
            elif data[i][input_headers_loc[8]] == 5:
                data_place[row][5] = -1
                row = row + 1
                data_place[row][0] = 0
                data_place[row][1] = unicon.convert_telemetry_date_to_unix_time(data[i][input_headers_loc[0]]) + (
                60 * data[i][input_headers_loc[8]])
                data_place[row][2] = data[i][input_headers_loc[5]]
                data_place[row][3] = data[i][input_headers_loc[4]]
                data_place[row][6] = data[i][input_headers_loc[3]]
                data_place[row][7] = data[i][input_headers_loc[6]]
                data_place[row][5] = -1
                data_place[row][4] = data[i][input_headers_loc[1]]
            else:
                data_place[row][5] = -1
                row = row + 1
                data_place[row][0] = 0
                data_place[row][1] = unicon.convert_telemetry_date_to_unix_time(data[i][input_headers_loc[0]]) + (60 * data[i][input_headers_loc[8]])
                data_place[row][2] = data[i][input_headers_loc[5]]
                data_place[row][3] = data[i][input_headers_loc[4]]
                data_place[row][6] = data[i][input_headers_loc[3]]
                data_place[row][7] = data[i][input_headers_loc[6]]
                data_place[row][5] = 0
                data_place[row][4] = data[i][input_headers_loc[1]]
        else:
            data_place[row][4] = data[i][input_headers_loc[2]]

            if data[i][input_headers_loc[9]] == 0:
                data_place[row][5] = 0
            else:
                data_place[row][5] = 1
                row = row + 1
                data_place[row][0] = 0
                data_place[row][1] = unicon.convert_telemetry_date_to_unix_time(data[i][input_headers_loc[0]]) + (60 * data[i][input_headers_loc[9]])
                data_place[row][2] = data[i][input_headers_loc[5]]
                data_place[row][3] = data[i][input_headers_loc[4]]
                data_place[row][6] = data[i][input_headers_loc[3]]
                data_place[row][7] = data[i][input_headers_loc[6]]
                data_place[row][5] = 0
                data_place[row][4] = data[i][input_headers_loc[2]]
        row = row + 1

    # #Delete possible duplicate rows
    # for i in range(0, len(data_place)-1):
    #     if data_place[i][1] == data_place[i+1][1]:
    #         print("GOT ONE!")
    #         data_place.pop(i+1)

    final_data = []
    for row in range(0, len(data_place)-1):
        if data_place[row][1] == data_place[row+1][1]:
            print("found a dupe!")
            #del data[row]
        else:
            final_data.append(data_place[row])

    with open(save_location + "formatted/" + savefile_name + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(final_data)

#csv_formatter('C:/Users/dwood/Documents/Data/Thermodynamic Model/pytest_in/TstatTelemetry_48b5742b-a91e-4a7c-b19e-0c94e56a685d_3_311054139225.csv', 'C:/Users/dwood/Documents/Data/Thermodynamic Model/python_test/', 'summer')
