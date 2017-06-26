import os

def reject(line_index_list):
    '''
    Precondition: row is a line of comma-separated values from a CSV file.
    Appends row to the file rejected_updates.csv.
    '''
    cwd = os.getcwd()

    lines_returned = ""
    all_rejected = ""
    # initialize rejected_updates file if it doesn't exist (add attribute headers)
    if not os.path.isfile(os.path.join(cwd, "rejected_updates.csv")):    
        rejected = open(os.path.join(cwd, "rejected_updates.csv"), 'w')
        results = open(os.path.join(cwd, "combined.csv"), 'r')
        lines_returned = results.readline()
        rejected.write(lines_returned)
        rejected.close()
        results.close()
    # get attribute headers of formatted_results.
    else:
        #reduce_cycle()
        rejected = open(os.path.join(cwd, "rejected_updates.csv"), 'r')
        results = open(os.path.join(cwd, "combined.csv"), 'r')
        lines_returned = results.readline()
        all_rejected = rejected.read()
        rejected.close()
        results.close()
        

    # file exists or has just been initialized above, so append row to rejected file
    rejected = open(os.path.join(cwd, "rejected_updates.csv"), 'a')
    results = open(os.path.join(cwd, "combined.csv"), 'r')
    current_line = 0
    current_row = 0
    # converts the list of indexes (str) to list of indexes (int)
    line_index_list = list(map(int, line_index_list))
    # gets all the lines after the attribute headers of formatted_result.csv
    for line in results.readlines()[1:]:
        # Case: if current_line index is equal to a row we selected to reject
        if (current_line == line_index_list[current_row]):
            # Write to the rejected_updates.csv file
            if not (line.rstrip('\n') in all_rejected):
                rejected.write(line.rstrip('\n') + ',31\n')
            # Used to make sure index error doesn't happen, stops counting.
            if (current_row < (len(line_index_list) - 1)):
                current_row += 1
            current_line += 1
        else:
            lines_returned = lines_returned + line
            current_line += 1
    rejected.close()
    results.close()
    # Required to rewrite the formatted_results.csv without the rejected rows
    results = open(os.path.join(cwd, "combined.csv"), 'w')
    results.write(lines_returned)
    results.close()
# Example usage
# reject("11 Com b,11 Com b,confirmedplanets,,,,,,,,,1.5,,1.5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,rv,radialvelocity,,,15/09/20,2015-08-21,11 Com.xml,")