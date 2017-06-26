import os
import csv
from display_diff import * 
from update_oec_xml import *
import sys
import datetime

def category_convert(attribute):
    category_convert = [["Mass [Mjup]", "mass"], 
                        ["Mass [Mjup] errorminus", "mass errorminus"],
                        ["Mass [Mjup] errorplus", "mass errorplus"],
                        ["Mass [Mjup] lowerlimit", "mass lowerlimit"],
                        ["Mass [Mjup] upperlimit", "mass upperlimit"],
                        ["Mass [MSun]", "mass"], 
                        ["Mass [MSun] errorminus", "mass errorminus"],
                        ["Mass [MSun] errorplus", "mass errorplus"],
                        ["Radius [Rjup]", "radius"], 
                        ["Radius [Rjup] errorminus", "radius errorminus"],
                        ["Radius [Rjup] errorplus", "radius errorplus"],
                        ["Radius [Rjup] lowerlimit", "radius lowerlimit"],
                        ["Radius [Rjup] upperlimit", "radius upperlimit"],
                        ["Radius [RSun]", "radius"], 
                        ["Radius [RSun] errorminus", "radius errorminus"],
                        ["Radius [RSun] errorplus", "radius errorplus"],
                        ["Orbital period [days]", "period"], 
                        ["Orbital period [days] errorminus", "period errorminus"],
                        ["Orbital period [days] errorplus", "period errorplus"],
                        ["Orbital period [days] lowerlimit", "period lowerlimit"],
                        ["Orbital period [days] upperlimit", "period upperlimit"],
                        ["Eccentricity", "eccentricity"], 
                        ["Eccentricity errorminus", "eccentricity errorminus"],
                        ["Eccentricity errorplus", "eccentricity errorplus"],
                        ["Eccentricity lowerlimit", "eccentricity lowerlimit"],
                        ["Eccentricity upperlimit", "eccentricity upperlimit"],
                        ["Equilibrium temperature [K]", "temperature"], 
                        ["Equilibrium temperature [K] errorminus", "temperature errorminus"],
                        ["Equilibrium temperature [K] errorplus", "temperature errorplus"],
                        ["Equilibrium temperature [K] lowerlimit", "temperature lowerlimit"],
                        ["Equilibrium temperature [K] upperlimit", "temperature upperlimit"],
                        ["Discovery method", "discoverymethod"],
                        ["Discovery year", "discoveryyear"],
                        ["Age [Gyr]", "age"],
                        ["Age [Gyr] errorminus", "age errorminus"],
                        ["Age [Gyr] errorplus", "age errorplus"],
                        ["Age [Gyr] lowerlimit", "age lowerlimit"],
                        ["Age [Gyr] upperlimit", "age upperlimit"],
                        ["Metallicity [Fe/H]", "metallicity"],
                        ["Metallicity [Fe/H] errorminus", "metallicity errorminus"],
                        ["Metallicity [Fe/H] errorplus", "metallicity errorplus"],
                        ["Temperature [K]", "temperature"],
                        ["Temperature [K] errorminus", "temperature errorminus"],
                        ["Temperature [K] errorplus", "temperature errorplus"],
                        ["Spectral type", "spectraltype"]
                        ["Visual magnitude", "magV"],
                        ["Visual magnitude errorminus", "magV errorminus"],
                        ["Visual magnitude errorplus", "magV errorplus"],
                        ["Right ascension", "rightascension"],
                        ["Declination", "declination"],
                        ["Distance [parsec]", "distance"],
                        ["Distance errorminus", "distance errorminus"],
                        ["Distance errorplus", "distance errorplus"]]
    new_attribute = ""
    for i in category_convert:
        if i[0] == attribute:
            new_attribute = i[1]
            break
    return new_attribute

def accept(array_index, input_csv):
    input_data = [] 
    # Read through the csv data file for input_csv and insert each row into a list,
    # so we will have a list of rows of the csv data file. 
    with open(os.path.join(os.getcwd(), input_csv), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            input_data.append(row)
    csvfile.close()
    final_data = []
    final_data.append(input_data[0])
    for i in range(1, len(input_data)):
        temp_data = []
        row = input_data[i]
        name = row[0]
        category = row[1]
        attribute = row[2]
        oec_value = row[3]
        eu_value = row[4]
        nasa_value = row[5]
        source = row[6]
        if eu_value == "":
            other_value = nasa_value
        else:
            other_value = eu_value
        if i in array_index:
            update_oec_xml(source[:-4], category, category_convert(attribute), other_value)
            update_oec_xml(source[:-4], category, "lastupdate", datetime.datetime.today().strftime('%y/%m/%d'))
        else:
            final_data.append(row)
    # Save the final result into a csv file.    
    with open(os.path.join(os.getcwd(), input_csv), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_data)
        csvfile.close()
    return 

                
                        
                    
            