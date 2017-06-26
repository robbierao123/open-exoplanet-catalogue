import ntpath

def standardize_csv(input_csv):
    """
    Input: Takes in a string that is the name of the csv file including ".csv"
    Output: Returns nothing, but generates a standardized csv file of the input
    
    Deals with :
    
        (1) ' ; [ ] { } ~ ` & ^ % $ # @ ! = ? > < : _ "
        (2) Uppercase
           
    """    
    # All the ascii values of the special characters.
    ascii_cases = [39, 59, 91, 93, 123, 125, 126, 96, 38, 94, 37, 36, 35, 64,
                   33, 61, 63, 62, 60, 42, 95, 32, 58]
        
    # Open the input csv file
    csv_input = open(input_csv, "r")
    # Gets Output csv file name and creates and opens output file to write to.
    output_name = "standardize_" + ntpath.basename(input_csv)
    csv_output = open(output_name, "w")
    # Used to check if its the firs tline, 
    first_line = True
    
    # PART 2: Read from input_csv,and write to csv_output.
    for readline in csv_input.readlines():
        # Writes the first line (Attributes) to csv_output unchanged
        if (first_line):
            csv_output.write(readline)
            # Switch case to False
            first_line = False
        # Past the first line.
        else:
            # Used the  check if its the last column
            last_column = False
            # Used to get the rest of the string in readline after last ","
            current_index = readline.find(',') + 1
            csv_output.write(readline[0: current_index])
            # Checks each character on the current line read.
            while current_index < len(readline):
                char = readline[current_index]
                # Case: If last column, write the rest of the line in.
                if (("," in readline[current_index:]) == False):
                    csv_output.write(readline[current_index:])
                    break

                # Case: If the characters are uppercase
                elif ((ord(char) >= 65) and (ord(char) <= 90)):
                    csv_output.write(char.lower())
                
                # Case: Not a special char to remove
                elif not (ord(char) in ascii_cases):
                    csv_output.write(char)


                current_index += 1

    # PART 3: Close the files.
    csv_input.close()
    csv_output.close()

    return

'''
if (__name__ == "__main__"):
    standardize_csv("OEC_planet.csv")
    standardize_csv("OEC_star.csv")
    standardize_csv("OEC_system.csv")
    standardize_csv('EU_Catalogue_Data.csv')
'''


def standardize_data(input_data):
    """
    Input: Takes in a string that is the name of the csv file including ".csv"
    Output: Returns nothing, but generates a standardized csv file of the input
    
    Deals with :
    
        (1) ' ; [ ] { } ~ ` & ^ % $ # @ ! = ? > < : _ "
        (2) Uppercase
           
    """    
    # All the ascii values of the special characters.
    ascii_cases = [39, 59, 91, 93, 123, 125, 126, 96, 38, 94, 37, 36, 35, 64,
                   33, 61, 63, 62, 60, 42, 95, 32, 58]

    # Case: If the characters are uppercase
    output_data = ''
    for char in input_data:
        if ((ord(char) >= 65) and (ord(char) <= 90)):
            output_data = output_data + char.lower()
        elif not (ord(char) in ascii_cases):
            output_data = output_data + char

    return output_data

