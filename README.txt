This is a complete package to compare the data from OEC to exoplanet.eu. 

et_xmlfile-1.0.1
jdcal-1.3
openpyxl-2.4.0
  These three are modules for opening xlsx files in python. 
  
Unidecode-0.04.19
  This module is to translate Greek letters to the closest English letters. 
  
systems
  This is all the data in OEC, stored in xml files. 
  
Data_Organize.xlsx
  This is a spreadsheet for column aligning and reordering. DO NOT CHANGE THE CONTENTS! This file is opened in parse_csv.py
  
OEC_main.py
  Main function for this package. It goes as the following:
  1. Convert the xml files in 'systems' folder into three csv files. 
  2. Download the raw csv data from exoplanet.eu. 
  3. Reorder the columns in the raw csv file and output a new csv file with exactly the same column ordering as the OEC csv data file. 
  4. Standardize all csv data files. 
  5. Compare the csv files and generate a new csv file containing the differences. 
  6. The generated file is called 'result.csv' for now. 
  
