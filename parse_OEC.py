import xml.etree.ElementTree as ET
import os
import glob
import csv
import sys
from standardize import standardize_data
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.getcwd(), 'Unidecode-0.04.19'))
#unidecode is an external module that replace greek letters to the closest english letters
from unidecode import unidecode

#Initialize global variables for the final data.
final_system_data = []
final_star_data = []
final_planet_data = []

system_header = ['Primary system name',
                 'All system names',
                 'Right ascension',
                 'Declination',
                 'Distance [parsec]',
                 'Distance errorminus',
                 'Distance errorplus',
                 'source (xml)']
star_header = ['Primary star name',
               'All star names',
               'Mass [MSun]',
               'Mass [MSun] errorminus',
               'Mass [MSun] errorplus', 
               'Radius [RSun]',
               'Radius [RSun] errorminus',
               'Radius [RSun] errorplus', 
               'Age [Gyr]',
               'Age [Gyr] errorminus',
               'Age [Gyr] errorplus',
               'Age [Gyr] lowerlimit',
               'Age [Gyr] upperlimit', 
               'Metallicity [Fe/H]',
               'Metallicity [Fe/H] errorminus',
               'Metallicity [Fe/H] errorplus', 
               'Temperature [K]',
               'Temperature [K] errorminus',
               'Temperature [K] errorplus', 
               'Spectral type',
               'Visual magnitude',
               'Visual magnitude errorminus',
               'Visual magnitude errorplus', 
               'source (xml)']
planet_header = ['Primary planet name',
                 'All planet names',
                 'Lists',
                 'Mass [Mjup]',
                 'Mass [Mjup] errorminus',
                 'Mass [Mjup] errorplus',
                 'Mass [Mjup] lowerlimit',
                 'Mass [Mjup] upperlimit', 
                 'Radius [Rjup]',
                 'Radius [Rjup] errorminus',
                 'Radius [Rjup] errorplus',
                 'Radius [Rjup] lowerlimit',
                 'Radius [Rjup] upperlimit', 
                 'Orbital period [days]',
                 'Orbital period [days] errorminus',
                 'Orbital period [days] errorplus',
                 'Orbital period [days] lowerlimit',
                 'Orbital period [days] upperlimit', 
                 'Eccentricity',
                 'Eccentricity errorminus',
                 'Eccentricity errorplus',
                 'Eccentricity lowerlimit',
                 'Eccentricity upperlimit', 
                 'Equilibrium temperature [K]',
                 'Equilibrium temperature [K] errorminus',
                 'Equilibrium temperature [K] errorplus',
                 'Equilibrium temperature [K] lowerlimit',
                 'Equilibrium temperature [K] upperlimit', 
                 'Discovery method',
                 'Discovery year',
                 'Last updated [yy/mm/dd]',
                 'source (xml)']


#This function returns the value of root.tag.
#If root.tag is None, then return an empty string.
def _find_text_from_root(root, tag):
    node = root.find(tag)
    if node is None or node.text is None:
        return ''
    else:
        return node.text


#This function returns the value of root.tag.attribute.
#If root.tag or root.tag.attribute is None, then return an empty string.
def _find_attrib_from_root(root, tag, attrib):
    node = root.find(tag)
    if node is None or node.get(attrib) is None:
        return ''
    else:
        return node.get(attrib)


#This function replaces greek letters to the closest english letters.
def _ignore_unicode(text):
    #\u03c8 = psi, appeared in system, star, planet names
    #\u03b3 = gamma, appeared in star spectral type
    #\u03c0 = pi, appeared in star names
    #\u03c1 = rho, appeared in star, planet names
    #\u03bd = nu, appeared in star names
    #\u03b1 = alpha, appeared in star names
    #\u03b2 = beta, appeared in star names
    #\u03b5 = nu, appeared in star names
    return unidecode(text)
    

#This function parses all the xml data into csv format. 
def xml_to_csv(path):
    final_system_data.append(system_header)
    final_star_data.append(star_header)
    final_planet_data.append(planet_header)
    count = 0
    
    for filename in os.listdir(path):
        count += 1
        f = open(os.path.join(path, filename), 'rt', encoding='utf8')
        root = ET.parse(f).getroot()

        #-----  Construct system data  -----
        temp_system_data = []
        #Primary system name
        system_name_list = root.findall('name')
        temp_system_data.append(system_name_list[0].text)

        #All system names
        alt_system_name = ''
        for i in range(0, len(system_name_list)):
            alt_system_name += _ignore_unicode(system_name_list[i].text) + '|'
        alt_system_name = alt_system_name[0: len(alt_system_name) - 1]
        alt_system_name = standardize_data(alt_system_name)
        temp_system_data.append(alt_system_name)

        #Right ascension
        temp_system_data.append(_find_text_from_root(root, 'rightascension'))

        #Declination
        temp_system_data.append(_find_text_from_root(root, 'declination'))

        #Distance [parsec]
        temp_system_data.append(_find_text_from_root(root, 'distance'))

        #Distance errorminus
        temp_system_data.append(_find_attrib_from_root(root, 'distance', 'errorminus'))

        #Distance errorplus
        temp_system_data.append(_find_attrib_from_root(root, 'distance', 'errorplus'))

        #source (xml)
        temp_system_data.append(filename)

        final_system_data.append(temp_system_data)
        #-----  End of system data  -----

        #-----  Construct star data  -----
        star_list = root.findall('.//star')
        for star in star_list:
            temp_star_data = []
            
            #Primary star name
            star_name_list = star.findall('name')
            temp_star_data.append(star_name_list[0].text)

            #All star names
            alt_star_name = ''
            for i in range(0, len(star_name_list)):
                alt_star_name += _ignore_unicode(star_name_list[i].text) + '|'
            alt_star_name = alt_star_name[0: len(alt_star_name) - 1]
            temp_star_data.append(alt_star_name)

            #Mass [MSun]
            temp_star_data.append(_find_text_from_root(star, 'mass'))

            #Mass [MSun] errorminus
            temp_star_data.append(_find_attrib_from_root(star, 'mass', 'errorminus'))

            #Mass [MSun] errorplus
            temp_star_data.append(_find_attrib_from_root(star, 'mass', 'errorplus'))

            #Radius [RSun]
            temp_star_data.append(_find_text_from_root(star, 'radius'))

            #Radius [RSun] errorminus
            temp_star_data.append(_find_attrib_from_root(star, 'radius', 'errorminus'))

            #Radius [RSun] errorplus
            temp_star_data.append(_find_attrib_from_root(star, 'radius', 'errorplus'))

            #Age [Gyr]
            temp_star_data.append(_find_text_from_root(star, 'age'))

            #Age [Gyr] errorminus
            temp_star_data.append(_find_attrib_from_root(star, 'age', 'errorminus'))

            #Age [Gyr] errorplus
            temp_star_data.append(_find_attrib_from_root(star, 'age', 'errorplus'))

            #Age [Gyr] lowerlimit
            temp_star_data.append(_find_attrib_from_root(star, 'age', 'lowerlimit'))

            #Age [Gyr] upperlimit
            temp_star_data.append(_find_attrib_from_root(star, 'age', 'upperlimit'))

            #Metallicity [Fe/H]
            temp_star_data.append(_find_text_from_root(star, 'metallicity'))

            #Metallicity [Fe/H] errorminus
            temp_star_data.append(_find_attrib_from_root(star, 'metallicity', 'errorminus'))

            #Metallicity [Fe/H] errorplus
            temp_star_data.append(_find_attrib_from_root(star, 'metallicity', 'errorplus'))

            #Temperature [K]
            temp_star_data.append(_find_text_from_root(star, 'temperature'))

            #Temperature [K] errorminus
            temp_star_data.append(_find_attrib_from_root(star, 'temperature', 'errorminus'))

            #Temperature [K] errorplus
            temp_star_data.append(_find_attrib_from_root(star, 'temperature', 'errorplus'))

            #Spectral type
            temp_star_data.append(_ignore_unicode(_find_text_from_root(star, 'spectraltype')))

            #Visual magnitude
            temp_star_data.append(_find_text_from_root(star, 'magV'))

            #Visual magnitude errorminus
            temp_star_data.append(_find_attrib_from_root(star, 'magV', 'errorminus'))

            #Visual magnitude errorplus
            temp_star_data.append(_find_attrib_from_root(star, 'magV', 'errorplus'))

            #source (xml)
            temp_star_data.append(filename)

            final_star_data.append(temp_star_data)
        #-----  End of star data  -----

        #-----  Construct planet data  -----
        planet_list = root.findall('.//planet')
        for planet in planet_list:
            temp_planet_data = []
            
            #Primary planet name
            planet_name_list = planet.findall('name')
            temp_planet_data.append(planet_name_list[0].text)

            #All planet names
            alt_planet_name = ''
            for i in range(0, len(planet_name_list)):
                alt_planet_name += _ignore_unicode(planet_name_list[i].text) + '|'
            alt_planet_name = alt_planet_name[0: len(alt_planet_name) - 1]
            temp_planet_data.append(alt_planet_name)

            #Lists
            lists_list = planet.findall('list')
            lists = ''
            for i in range(0, len(lists_list)):
                lists += lists_list[i].text + '|'
            lists = lists[0: len(lists) - 1]
            lists = lists.replace(',', '|')
            temp_planet_data.append(lists)

            #Mass [Mjup]
            temp_planet_data.append(_find_text_from_root(planet, 'mass'))

            #Mass [Mjup] errorminus
            temp_planet_data.append(_find_attrib_from_root(planet, 'mass', 'errorminus'))

            #Mass [Mjup] errorplus
            temp_planet_data.append(_find_attrib_from_root(planet, 'mass', 'errorplus'))

            #Mass [Mjup] lowerlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'mass', 'lowerlimit'))

            #Mass [Mjup] upperlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'mass', 'upperlimit'))

            #Radius [Rjup]
            temp_planet_data.append(_find_text_from_root(planet, 'radius'))

            #Radius [Rjup] errorminus
            temp_planet_data.append(_find_attrib_from_root(planet, 'radius', 'errorminus'))

            #Radius [Rjup] errorplus
            temp_planet_data.append(_find_attrib_from_root(planet, 'radius', 'errorplus'))

            #Radius [Rjup] lowerlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'radius', 'lowerlimit'))

            #Radius [Rjup] upperlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'radius', 'upperlimit'))

            #Orbital period [days]
            temp_planet_data.append(_find_text_from_root(planet, 'period'))

            #Orbital period [days] errorminus
            temp_planet_data.append(_find_attrib_from_root(planet, 'period', 'errorminus'))

            #Orbital period [days] errorplus
            temp_planet_data.append(_find_attrib_from_root(planet, 'period', 'errorplus'))

            #Orbital period [days] lowerlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'period', 'lowerlimit'))

            #Orbital period [days] upperlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'period', 'upperlimit'))

            #Eccentricity
            temp_planet_data.append(_find_text_from_root(planet, 'eccentricity'))

            #Eccentricity errorminus
            temp_planet_data.append(_find_attrib_from_root(planet, 'eccentricity', 'errorminus'))

            #Eccentricity errorplus
            temp_planet_data.append(_find_attrib_from_root(planet, 'eccentricity', 'errorplus'))

            #Eccentricity lowerlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'eccentricity', 'lowerlimit'))

            #Eccentricity upperlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'eccentricity', 'upperlimit'))

            #Equilibrium temperature [K]
            temp_planet_data.append(_find_text_from_root(planet, 'temperature'))

            #Equilibrium temperature [K] errorminus
            temp_planet_data.append(_find_attrib_from_root(planet, 'temperature', 'errorminus'))

            #Equilibrium temperature [K] errorplus
            temp_planet_data.append(_find_attrib_from_root(planet, 'temperature', 'errorplus'))

            #Equilibrium temperature [K] lowerlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'temperature', 'lowerlimit'))

            #Equilibrium temperature [K] upperlimit
            temp_planet_data.append(_find_attrib_from_root(planet, 'temperature', 'upperlimit'))

            #Discovery method
            temp_planet_data.append(_find_text_from_root(planet, 'discoverymethod'))

            #Discovery year
            temp_planet_data.append(_find_text_from_root(planet, 'discoveryyear'))

            #Last updated [yy/mm/dd]
            temp_planet_data.append(_find_text_from_root(planet, 'lastupdate'))

            #source (xml)
            temp_planet_data.append(filename)

            final_planet_data.append(temp_planet_data)
        #-----  End of planet data  -----

        f.close()
        if count % 100 == 0:
            print ('processed ' + str(count) + ' files...')

    with open(os.path.join(os.getcwd(), 'OEC_system.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_system_data)
    csvfile.close()

    with open(os.path.join(os.getcwd(), 'OEC_star.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_star_data)
    csvfile.close()

    with open(os.path.join(os.getcwd(), 'OEC_planet.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_planet_data)
    csvfile.close()

    return

#Main Script
'''
path = os.path.join(os.getcwd(), 'systems')
xml_to_csv(path)
'''
