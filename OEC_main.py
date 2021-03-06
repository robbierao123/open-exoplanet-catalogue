import download_eu, standardize, parse_OEC, parse_csv, compare_csv, display
import os
from display_diff import *
import platform
if platform.system == 'Windows':
	os.system('fetch_oec')
else:
	os.system('sh fetch_oec.sh')
print('Converting XML data from OEC to a CSV file...')
path = os.path.join(os.getcwd(), 'systems')
parse_OEC.xml_to_csv(path)
print('CSV file for OEC data successfully created...')

print('Downloading CSV data file from http://exoplanet.eu ...')
download_eu.download_csv('http://exoplanet.eu/catalog/csv/', os.path.join(os.getcwd(), 'EU_Catalogue_Data_Raw.csv'))
print('CSV data file successfully downloaded...')
print('Downloading CSV data file from http://exoplanetarchive.ipac.caltech.edu ...')
download_eu.download_csv('http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=*', os.path.join(os.getcwd(), 'NASA_Catalogue_Data_Raw.csv'))
print('CSV data file successfully downloaded...')

print('Parsing the data from exoplanet.eu to match with the format of OEC...')
parse_csv.parse_csv_eu('EU_Catalogue', 'EU_Catalogue_Data_Raw.csv', 'EU_Catalogue_Data.csv')
print('Parsing the data from NASA to match with the format of OEC...')
parse_csv.parse_csv_nasa('NASA_Catalogue', 'NASA_Catalogue_Data_Raw.csv', 'NASA_Catalogue_Data.csv')
print('Parsing the star data from exoplanet.eu to match with the format of OEC...')
parse_csv.parse_csv_eu_star('EU_Catalogue_Star', 'EU_Catalogue_Data_Raw.csv', 'EU_Catalogue_Star_Data.csv')
print('Parsing the data from NASA to match with the format of OEC...')
parse_csv.parse_csv_nasa_star('NASA_Catalogue_Star', 'NASA_Catalogue_Data_Raw.csv', 'NASA_Catalogue_Star_Data.csv')
print('Parsing the system data from exoplanet.eu to match with the format of OEC...')
parse_csv.parse_csv_eu_star('EU_Catalogue_System', 'EU_Catalogue_Data_Raw.csv', 'EU_Catalogue_System_Data.csv')
print('Parsing the system data from NASA to match with the format of OEC...')
parse_csv.parse_csv_nasa_system('NASA_Catalogue_System', 'NASA_Catalogue_Data_Raw.csv', 'NASA_Catalogue_System_Data.csv')

print('Standardizing the CSV data...')
standardize.standardize_csv("OEC_planet.csv")
standardize.standardize_csv("OEC_star.csv")
#standardize.standardize_csv("OEC_system.csv")
standardize.standardize_csv('EU_Catalogue_Data.csv')
standardize.standardize_csv('NASA_Catalogue_Data.csv')
standardize.standardize_csv('EU_Catalogue_Star_Data.csv')
standardize.standardize_csv('NASA_Catalogue_Star_Data.csv')
standardize.standardize_csv('EU_Catalogue_System_Data.csv')

print('Comparing data between OEC and exoplanet.eu...')
compare_csv.compare_csv('standardize_OEC_planet.csv', 'standardize_EU_Catalogue_Data.csv', 'result_oec_eu.csv')
print('Comparing data between OEC and NASA...')
compare_csv.compare_csv('standardize_OEC_planet.csv', 'standardize_NASA_Catalogue_Data.csv', 'result_oec_nasa.csv')
print('Comparing star data between OEC and exoplanet.eu...')
compare_csv.compare_csv('standardize_OEC_star.csv', 'standardize_EU_Catalogue_Star_Data.csv', 'result_oec_eu_star.csv')
print('Comparing star data between OEC and NASA...')
compare_csv.compare_csv('standardize_OEC_star.csv', 'standardize_NASA_Catalogue_Star_Data.csv', 'result_oec_nasa_star.csv')
print('Comparing system data between OEC and exoplanet.eu...')
compare_csv.compare_csv('OEC_system.csv', 'standardize_EU_Catalogue_System_Data.csv', 'result_oec_eu_system.csv')
print('Comparing system data between OEC and NASA...')
compare_csv.compare_csv_nasa_system('OEC_system.csv', 'NASA_Catalogue_System_Data.csv', 'result_oec_nasa_system.csv')

print('Generating differences')
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
os.system('python display.py')