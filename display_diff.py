import os
import csv
import collections
import itertools
import operator

def sort_combined(input_csv):
    '''
    sorts the input csv by (source, category, name)
    '''
    sort_list = []
    final_data = []
    with open(os.path.join(os.getcwd(), input_csv), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        header = next(reader)
        #sort list
        sort_list = sorted(reader, key=operator.itemgetter(6))
        sort_list.sort(key=operator.itemgetter(1), reverse = True)
        sort_list.sort(key=operator.itemgetter(2))
        sort_list.sort(key=operator.itemgetter(0))
    csvfile.close()
    final_data.append(header)
    # input_csv is now the sprted data
    for row in range(0, len(sort_list)):
        final_data.append(sort_list[row])
    with open(os.path.join(os.getcwd(), input_csv), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_data)
    csvfile.close()
    return 
        
def add_data(data, name, category, attribute, oec_value, other_value, source, nasa_eu):
    data.append(name)
    data.append(category)
    data.append(attribute)
    data.append(oec_value)
    if nasa_eu == "eu":
       data.append(other_value)
       data.append("")
    else:
       data.append("")
       data.append(other_value)
    data.append(source)
    return data

def combined_format(output_csv):
    '''
    output_csv: name of the output_csv file

    Precondition: you created all of ["diff_result_nasa_star.csv", 
                 "diff_result_eu_star.csv", "diff_result_nasa.csv", "diff_result_eu.csv",
                 "diff_result_nasa_system.csv", "diff_result_eu_system.csv"]
    '''
    final_data = []
    file_list = ["diff_result_nasa_star.csv", "diff_result_eu_star.csv",
                 "diff_result_nasa.csv", "diff_result_eu.csv",
                 "diff_result_nasa_system.csv", "diff_result_eu_system.csv"]
    put_header = False
    # append each file to the output file
    for i in file_list:
        input_data = []
        with open(os.path.join(os.getcwd(), i), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                input_data.append(row)
        csvfile.close()
        # put the header in
        header = input_data[0]
        if put_header == False:
            final_data.append(header)
            put_header = True
        for j in range(1, len(input_data)):
            row = input_data[j]
            final_data.append(row)
    with open(os.path.join(os.getcwd(), output_csv), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_data)
        csvfile.close()
    return       
    
def format_diff(input_csv):
    '''
    input_csv: name of the first csv file, can be either relative or absolute path.
    
    Precondition:
      input_csv is output file of the function display_diff.
      
    For row in the input file,
        if one of the attributes is empty, add a 0
        and write the row to the output file.
    '''
    input_data = []
    # this list determines shows the values that are the same even though,
    # the spelling is different
    discover_method = [["rv", "radialvelocity"],
                       ["transit", "primarytransit"]]
    # Read through the csv data file for input_file1 and insert each row into a list,
    # so we will have a list of rows of the csv data file. 
    with open(os.path.join(os.getcwd(), input_csv), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data.append(row)
    csvfile.close()
    header = input_data[0]
    final_data = []
    final_data.append(header)
    for i in range(1, len(input_data)):
        temp_data= []
        row = input_data[i]
        name = row[0]
        category = row[1]
        attribute = row[2]
        oec_value = row[3]
        eu_value = row[4]
        nasa_value = row[5]
        source = row[6]
    # checks if values are the same using the list above  
        if attribute == "Discovery method":  
            standard_oec = oec_value.replace(" ", "").lower()
            if eu_value == "":
                standard_other = nasa_value.replace(" ", "").lower()
            else:
                standard_other = eu_value.replace(" ", "").lower()
            if [standard_oec, standard_other] not in discover_method and standard_oec != standard_other:
                if oec_value != "" and eu_value != "": 
                    add_data(temp_data, name, category, attribute, oec_value,
                             eu_value, source, "eu")
                    final_data.append(temp_data)
                elif oec_value != "" and nasa_value != "":
                    add_data(temp_data, name, category, attribute, oec_value,
                             nasa_value, source, "nasa")
                    final_data.append(temp_data)
    # add the data in either oec,eu is empty or oec,nasa is empty
        else:
            if oec_value != "" and eu_value != "":  
                add_data(temp_data, name, category, attribute, oec_value,
                         eu_value, source, "eu")
                final_data.append(temp_data)
            elif oec_value != "" and nasa_value != "":
                add_data(temp_data, name, category, attribute, oec_value,
                         nasa_value, source, "nasa")
                final_data.append(temp_data)
    # Save the final result into a csv file.    
    with open(os.path.join(os.getcwd(), input_csv), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_data)
        csvfile.close()
    return   

def display_diff(category, input_csv, output_csv):
    '''
    category: name of the category
    input_csv: name of the second csv file, can be either relative or absolute path.
    output_csv: name of the output csv file, can be either relative or absolute path.
    
    Precondition:
      category is either planet,system or star
      input_csv is output file of the program compare_csv.py.
      
    Checks for differences each row in the input file.
    For each difference, display the difference as a row in the output file.
    '''
    input_data = []
    # declaring the header of the output file
    diff_header = ["Name", "Category", "Attribute", "OEC value", "EU value", "NASA value", "source"]
    # Read through the csv data file for input_file1 and insert each row into a list,
    # so we will have a list of rows of the csv data file.     
    with open(os.path.join(os.getcwd(), input_csv), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data.append(row)
    csvfile.close()
    # the header of the input file
    header = input_data[0]
    # the category
    if input_csv[-8:] == "star.csv":
        diff_data = [2, 44]
        source_index = 44
    elif input_csv[-10:] == "system.csv":
        diff_data = [2, 12]
        source_index = 12
    else:
        diff_data = [4, 58]
        source_index = 60
    # finds the name of the catalogue
    if category == "planet":
        underscore1 = input_csv.find("_")
        underscore2 = input_csv[underscore1 + 1:].find("_") + underscore1 + 1
        catalogue = input_csv[underscore2 + 1:-4]    
    else:
        underscore1 = input_csv.find("_")
        underscore2 = input_csv[underscore1 + 1:].find("_") + underscore1 + 1
        underscore3 = input_csv[underscore2 + 1:].find("_") + underscore2 + 1
        catalogue = input_csv[underscore2 + 1:underscore3]
    # start and end index of the columns we check
    final_data = []
    final_data.append(diff_header)
    # checks each row for differences then adds each difference as a new row
    # of the output file
    for i in range(1, len(input_data)):
        row = input_data[i]
        name = row[0]
        source = row[source_index]
        for j in range(diff_data[0], diff_data[1], 2):
            temp_data = []
            # finds the attribute in the jth row of header
            bracket = header[j].find("(")
            attribute = header[j][:bracket]
            oec_value = row[j]
            other_value = row[j + 1]
            if oec_value != other_value:
                temp_data = add_data(temp_data, name, category, attribute,
                                     oec_value, other_value, source, catalogue)
                final_data.append(temp_data)
    # Save the final result into a csv file. 
    with open(os.path.join(os.getcwd(), output_csv), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_data)
        csvfile.close()
    return
'''
display_diff("planet", "result_oec_nasa.csv", "diff_result_nasa.csv")
display_diff("planet", "result_oec_eu.csv", "diff_result_eu.csv")
display_diff("star", "result_oec_nasa_star.csv", "diff_result_nasa_star.csv")
display_diff("star", "result_oec_eu_star.csv", "diff_result_eu_star.csv")
display_diff("system", "result_oec_eu_system.csv", "diff_result_eu_system.csv")
display_diff("system", "result_oec_nasa_system.csv", "diff_result_nasa_system.csv")
format_diff("diff_result_nasa_star.csv")
format_diff("diff_result_eu_star.csv")
format_diff("diff_result_eu.csv")
format_diff("diff_result_nasa.csv")
format_diff("diff_result_eu_system.csv")
format_diff("diff_result_nasa_system.csv")
combined_format("combined.csv")
sort_combined("combined.csv")
'''
