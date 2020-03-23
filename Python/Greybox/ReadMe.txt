READ.me
Thermodynamic Model usage overview:

The data that is fed into the model must follow the following format:
1) It must be a .csv
2) It must have no headers
3) It must have the following data in each column: ['0', 'Unix Time', 'Outdoor Temp', 'Indoor Temp', 'Tstat Setpoint', 'HVAC Mode', 'Solar Irradiation', 'Wind Speed']

Notes on data:
1)'HVAC Mode' can be one of three values (either -1, 0, or 1). -1 = AC on, 0 = no hvac, 1 = heat on

Telemetry file formatter:
The python file csv_formatter.py contains the formatter for telemetry files, it assumes that all telemetry files have the same headers. 
The formatter takes a telemetry file, formats it to be used in the model, and then saves it at the specified save location.
Weather data in between intervals is interpolated. Non consistent intervals only apply in the case of missing thermostat data or new rows generated
by a non-zero hvac runtime; for instance:

time	hvac_runtime_minutes
t1	0
t2	1
t3	0

becomes:

time	hvac_mode	
t1	0
t2	-1
t2+1minute 0
t3	0
