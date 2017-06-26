
import xml.etree.ElementTree as ET
import os
import glob
import csv
import sys

#FIELD_SIZE_LIMIT = 1000000000


def read_csv(input_filename):
    '''
    sheet_name: the name of the sheet that this function needs to read in Data_Organize.xlsx
    input_filename: name of the input csv file, can be either relative or absolute path.
    output_filename: name of the output csv file, can be either relative or absolute path.
    '''
    #csv.field_size_limit(FIELD_SIZE_LIMIT)
    input_data = []
    with open(os.path.join(os.getcwd(), input_filename), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data.append(row)

    csvfile.close()

    #Loop through each row in the input file, and reorder them by the orders given in column_order

        # print(row)
    return input_data


# if __name__ == "__main__":
#     read_csv('result.csv')