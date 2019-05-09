# filename: csvformatter
# contains various functions that correct incomming data to be utilized by the ANN; gaps in data must be appropriately
# filled, data with higher temporal resolutions are resolved to standard 5 minute intervals

import numpy as np
import csv


def cell2csv(file_name, cell_array, separator, excel_year, decimal):
    # function cell2csv(fileName, cellArray, separator, excelYear, decimal)
    # % Writes cell array content into a *.csv file.
    # % CELL2CSV(fileName, cellArray, separator, excelYear, decimal)
    # %
    # % fileName = Name of the file to save.[i.e. 'text.csv']
    # % cellArray = Name of the Cell Array where the data is in
    # % separator = sign separating the values(default=';')
    # % excelYear = depending on the Excel version, the cells are put into
    # % quotes before they are written to the file.The separator
    # % is set to semicolon(;)
    # % decimal = defines the decimal separator(default='.')
    # %
    # % by Sylvain Fiedler, KA, 2004
    # % updated by Sylvain Fiedler, Metz, 06
    # % fixed the logical - bug, Kaiserslautern, 06 / 2008, S.Fiedler
    # % added the choice of decimal separator, 11 / 2010, S.Fiedler

    # % % Checking für optional Variables
    if separator not in locals():   # if ~exist('separator', 'var')
        separator = ','             #     separator = ',';
                                    # end

    if excel_year not in locals():  # if ~exist('excelYear', 'var')
        excel_year = 1997           #     excelYear = 1997;
                                    # end

    if decimal not in locals():     # if ~exist('decimal', 'var')
        decimal = '.'               #     decimal = '.';
                                    # end

    # % % Setting separator
    # for newer excelYears
    if excel_year > 2000:            #     if excelYear > 2000
        separator = ';'             #         separator = ';';
                                    # end

    # % % Write file
    datei = open(file_name, 'w')    # datei = fopen(fileName, 'w');

    for z in range(0, cell_array.shape[0]):     # for z=1:size(cellArray, 1)
        for s in range(0, cell_array.shape[1]): # for s=1:size(cellArray, 2)

            var = eval('cell_array[z, s]')  # var = eval(['cellArray{z,s}']);
            # % If zero, then empty cell
            if var.shape[0] == 0:       # if size(var, 1) == 0
                var = ''                #     var = '';
                                        # end
            # % If numeric -> String
            if var.isnumeric():         # if isnumeric(var)
                var = str(var)          #     var = num2str(var);
                #     % Conversion of decimal separator(4 Europe & South America)
                #     % http: // commons.wikimedia.org / wiki / File: DecimalSeparator.svg
                if decimal != '.':                      #     if decimal ~= '.'
                    var = var.replace('.', decimal)     #     var = strrep(var, '.', decimal);
                                                        # end
                                        # end
            # % If logical -> 'true' or 'false'
            if var == bool:     # if islogical(var)
                if var:     #     if var == 1
                    var = 'TRUE'    #         var = 'TRUE';
                else:               #     else
                    var = 'FALSE'   #         var = 'FALSE';
                                    #     end
                                # end
            # % If newer version of Excel -> Quotes 4 Strings
            if excel_year > 2000:       # if excelYear > 2000
                var = ['"', var, '"']   #     var = ['"' var '"'];
                                        # end

            # % OUTPUT value
            datei.write(var)   # fprintf(datei, '%s', var);

            # % OUTPUT separator
            if s != cell_array.shape[1]:    # if s ~= size(cellArray, 2)
                datei.write(separator)      # fprintf(datei, separator);
                                            # end
                                        # end
        if z != cell_array.shape[0]:    # if z ~= size(cellArray, 1) % prevent a empty line at EOF
            # % OUTPUT newline
            datei.write('/n')       # fprintf(datei, '\n');
                                    # end
                                # end
    # % Closing file
    datei.close()
    # % END of cell2csv


def csvwrite_with_headers(filename, m, headers, r=0, c=0):
    # function csvwrite_with_headers(filename, m, headers, r, c)
    #
    # % % initial checks on the inputs
    if type(filename) is not str:                   # if ~ischar(filename)
        print('ERROR! Filename must be a string')   #     error('FILENAME must be a string');
                                                    # end

    if headers.count(type(headers[0])) == len(headers) and type(headers) is str:     # checks to see if the first instance in the headers list
        print('HEADER myst be a list of strings')           # is a string, and checks the whole list to see if there
                                                            # are any elements of the lest that are not the same type
                                                            # as the first elements of headers
                                                            # # if ~iscellstr(headers)
                                                            #     error('Header must be cell array of strings')
                                                            # end

    if len(headers) != m.shape[1]:      # if length(headers) ~= size(m, 2)
        print('number of header entries must match the number of columns in the data')  # error('number of header
                                        # entries must match the number of columns in the data')
                                        # end

    # % % write the header string to the file

    # % turn the headers into a single comma seperated string if it is a cell
    # % array,
    header_string = headers[0]      # header_string = headers{1};
    for i in range(1, len(headers)):        # for i = 2:length(headers)
        header_string = [header_string, ',', headers[i]]    # header_string = [header_string, ',', headers{i}];
                                                            # end
    # % if the data has an offset shifting it right then blank commas must
    # % be inserted to match
    if r > 0:     # if r > 0
        for i in range(0, r):               #     for i=1:r
            header_string.insert(0, ',')    #header_string = [',', header_string];
                                                    # end
                                                 # end

    # % write the string to a file
    fid = open(filename, 'w')       # fid = fopen(filename, 'w');
    fid.write(header_string)        # fprintf(fid, '%s\r\n', header_string);
    fid.close()                     # fclose(fid);

    # % % write the append the data to the file


    # % Call dlmwrite with a comma as the delimiter

    # dlmwrite(filename, m, '-append', 'delimiter', ',', 'roffset', r, 'coffset', c);
    # # newfilename = filesname(i).name; % removes.csv from the filename
    # # % saveas(h, figurename, 'pdf')
    # newfolder = 'formatted data\';
    # # newfolderpath = [folderpath, newfolder];
    # # newfullfilename = [newfolderpath, newfilename];
    # # % mkdir(folderpath, newfolder);
    # # csvwrite(newfullfilename, data_new);
    # # end
    #
