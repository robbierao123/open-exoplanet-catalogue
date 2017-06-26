import xml.etree.ElementTree as ET
import os
import glob
import csv
import sys
from math import log10, floor

class ColumnOrderingException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Input csv files must have exactly the same number of columns')

        

def compare_csv(input_file1, input_file2, output_file):
    '''
    input_file1: name of the first csv file, can be either relative or absolute path.
    input_file2: name of the second csv file, can be either relative or absolute path.
    output_file: name of the output csv file, can be either relative or absolute path.
    
    For the usage, input_file1 is always OEC data, and input_file2 can be either exoplanet.eu data or NASA data
    '''
    
    #Create a list to keep track of all alternative names for a planet. 
    name_list = []
    input_data1 = []
    #Read through the csv data file for input_file1 and insert each row into a list,
    #so we will have a list of rows of the csv data file. 
    with open(os.path.join(os.getcwd(), input_file1), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data1.append(row)
            #All alternative names are stored in the second column of the csv file. 
            name_list.append(row[1])
    csvfile.close()

    #Since input_file2 will have only one name per planet, so we don't need to maintain a name list. 
    input_data2 = []
    #Read through the csv data file for input_file2 and insert each row into a list,
    #so we will have a list of rows of the csv data file. 
    with open(os.path.join(os.getcwd(), input_file2), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data2.append(row)
    csvfile.close()

    #Get the headers for input_file1 and input_file2.
    #The header is the first row of the input file. 
    output_data = []
    header1 = input_data1[0]
    header2 = input_data2[0]
    #Remove the second column of the header, since this is 'Alternative names', and we don't need it in the result. 
    header1.remove(header1[1])
    header2.remove(header2[1])

    #Throw an exception if the two headers have different length.
    if len(header1) != len(header2):
        raise ColumnOrderingException()

    #Combine the two headers into one header.
    #Since these two csv files are required to have exactly the same number of columns,
    #we can simply put each column name side by side, and add a tag at the end of the original name.
    output_header = []
    for i in range(0, len(header1)):
        #i.e., 'Mass' will be 'Mass (from OEC_Data.csv)'
        output_header.append(header1[i] + '(from ' + input_file1 + ')')
        output_header.append(header2[i] + '(from ' + input_file2 + ')')
    output_data.append(output_header)
    
    #This list is more for debugging in later stage. 
    not_found = []

    #Loop through each row in input_file2,
    #get the planet name for that row,
    #search this name in input_file1 in all the alternative names,
    #if there is a match, then we know that the matching row is the planet we are looking for,
    #compare the data in these two rows
    for i in range(1, len(input_data2)):
        row2 = input_data2[i]
        name = row2[1]
        j = 1
        #Try to find the planet name from input_file2 in input_file1. 
        while j < len(name_list):
            if name_list[j].find(name) != -1:
                break
            j += 1
        #If there is no match, then note down this planet name, and move to the next row in input_file2. 
        if j == len(name_list):
            not_found.append(name)
            continue
        #If there is a match, then get this row in input_file1. 
        row1 = input_data1[j]

        #Throw an exception when the two rows have different length.
        if len(row1) != len(row2):
            print(row1)
            print(len(row1))
            print(row2)
            print(len(row2))
            raise ColumnOrderingException()

        #Initialize a list to keep the result after comparison between these two rows. 
        temp_output_data = []
        #Add the planet names directly into the temp list, since the raw planet names might not be the same. 
        temp_output_data.append(row1[0])
        temp_output_data.append(row2[0])
        #Loop through these two rows and compare the data.
        #If they have the same value, then discard them. (add empty values in the temp list.
        #If they have different values, then append them into the temp list. 
        for j in range(2, len(row1)):
            try:
                value1 = float(row1[j])
                value2 = float(row2[j])
            except ValueError:
                value1 = row1[j]
                value2 = row2[j]
                
            if value1 != value2:
                temp_output_data.append(row1[j])
                temp_output_data.append(row2[j])
            else:
                temp_output_data.append('')
                temp_output_data.append('')
        #Add the result of comparison to the final output data. 
        output_data.append(temp_output_data)

    #Save the final result into a csv file. 
    with open(os.path.join(os.getcwd(), output_file), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_data)
    csvfile.close()
    
    return

'''
compare_csv('standardize_OEC_planet.csv', 'standardize_EU_Catalogue_Data.csv', 'result.csv')
'''

def compare_csv_nasa_system(input_file1, input_file2, output_file):
    '''
    input_file1: name of the first csv file, can be either relative or absolute path.
    input_file2: name of the second csv file, can be either relative or absolute path.
    output_file: name of the output csv file, can be either relative or absolute path.
    
    For the usage, input_file1 is always OEC data, and input_file2 can be either exoplanet.eu data or NASA data
    '''
    
    #Create a list to keep track of all alternative names for a planet. 
    name_list = []
    input_data1 = []
    #Read through the csv data file for input_file1 and insert each row into a list,
    #so we will have a list of rows of the csv data file. 
    with open(os.path.join(os.getcwd(), input_file1), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data1.append(row)
            #All alternative names are stored in the second column of the csv file. 
            name_list.append(row[1])
    csvfile.close()

    #Since input_file2 will have only one name per planet, so we don't need to maintain a name list. 
    input_data2 = []
    #Read through the csv data file for input_file2 and insert each row into a list,
    #so we will have a list of rows of the csv data file. 
    with open(os.path.join(os.getcwd(), input_file2), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data2.append(row)
    csvfile.close()

    #Get the headers for input_file1 and input_file2.
    #The header is the first row of the input file. 
    output_data = []
    header1 = input_data1[0]
    header2 = input_data2[0]
    #Remove the second column of the header, since this is 'Alternative names', and we don't need it in the result. 
    header1.remove(header1[1])
    header2.remove(header2[1])

    #Throw an exception if the two headers have different length.
    if len(header1) != len(header2):
        raise ColumnOrderingException()

    #Combine the two headers into one header.
    #Since these two csv files are required to have exactly the same number of columns,
    #we can simply put each column name side by side, and add a tag at the end of the original name.
    output_header = []
    for i in range(0, len(header1)):
        #i.e., 'Mass' will be 'Mass (from OEC_Data.csv)'
        output_header.append(header1[i] + '(from ' + input_file1 + ')')
        output_header.append(header2[i] + '(from ' + input_file2 + ')')
    output_data.append(output_header)
    
    #This list is more for debugging in later stage. 
    not_found = []

    #Loop through each row in input_file2,
    #get the planet name for that row,
    #search this name in input_file1 in all the alternative names,
    #if there is a match, then we know that the matching row is the planet we are looking for,
    #compare the data in these two rows
    for i in range(1, len(input_data2)):
        row2 = input_data2[i]
        name = row2[1]
        j = 1
        #Try to find the planet name from input_file2 in input_file1. 
        while j < len(name_list):
            if name_list[j].find(name) != -1:
                break
            j += 1
        #If there is no match, then note down this planet name, and move to the next row in input_file2. 
        if j == len(name_list):
            not_found.append(name)
            continue
        #If there is a match, then get this row in input_file1. 
        row1 = input_data1[j]

        #Throw an exception when the two rows have different length.
        if len(row1) != len(row2):
            print(row1)
            print(len(row1))
            print(row2)
            print(len(row2))
            raise ColumnOrderingException()

        #Initialize a list to keep the result after comparison between these two rows. 
        temp_output_data = []
        #Add the planet names directly into the temp list, since the raw planet names might not be the same. 
        temp_output_data.append(row1[0])
        temp_output_data.append(row2[0])
        #Loop through these two rows and compare the data.
        #If they have the same value, then discard them. (add empty values in the temp list.
        #If they have different values, then append them into the temp list. 
        for j in range(2, len(row1)):
            try:
                value1 = float(row1[j])
                value2 = float(row2[j])
            except ValueError:
                value1 = row1[j]
                value2 = row2[j]

            if (j == 2) and (value1 != '') and (value2 != ''):
                temp_value1 = value1[6: len(value1)]
                temp_value2 = value2[6: len(value2)]
                value1_digits = find_significant_digits(temp_value1)
                value2_digits = find_significant_digits(temp_value2)
                if value1_digits > value2_digits:
                    temp_value1 = round_to_digits(temp_value1, value2_digits)
                else:
                    temp_value2 = round_to_digits(temp_value2, value1_digits)
                value1 = value1[0: 6] + temp_value1
                value2 = value2[0: 6] + temp_value2
            elif (j == 3) and (value1 != '') and (value2 != ''):
                temp_value1 = value1[7: len(value1)]
                temp_value2 = value2[7: len(value2)]
                value1_digits = find_significant_digits(temp_value1)
                value2_digits = find_significant_digits(temp_value2)
                if value1_digits > value2_digits:
                    temp_value1 = round_to_digits(temp_value1, value2_digits)
                else:
                    temp_value2 = round_to_digits(temp_value2, value1_digits)
                value1 = value1[0: 7] + temp_value1
                value2 = value2[0: 7] + temp_value2
                          
            if value1 != value2:
                temp_output_data.append(row1[j])
                temp_output_data.append(row2[j])
            else:
                temp_output_data.append('')
                temp_output_data.append('')
        #Add the result of comparison to the final output data. 
        output_data.append(temp_output_data)

    #Save the final result into a csv file. 
    with open(os.path.join(os.getcwd(), output_file), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_data)
    csvfile.close()
    
    return

'''
compare_csv_nasa_system('OEC_System.csv', 'NASA_Catalogue_System_Data.csv', 'result.csv')
'''

def find_significant_digits(input_string):
    dot = input_string.find('.')
    if dot == -1:
        return 0
    output_digits = len(input_string) - dot - 1
    i = len(input_string) - 1
    '''
    while input_string[i] != '.':
        if input_string[i] == '0':
            output_digits -= 1
        else:
            break
        i = i - 1
    '''
    return output_digits

def round_to_digits(input_string, sig_digits):
    try:
        temp = float(input_string)
    except ValueError:
        return 0
    temp = round(temp, sig_digits)
    if sig_digits == 0:
        temp = int(temp)
    temp = str(temp)
    if (temp.find('.') == -1) and (len(temp) == 1):
        temp = '0' + temp
    elif (temp.find('.') != -1) and (len(temp[0: temp.find('.')]) == 1):
        temp = '0' + temp
        
    return temp
    
    

