import os
import shutil

def update_oec_xml(system_name, category, attribute, new_value, source):
    '''
    Precondition:
      system_name is the name of an existing Exoplanet system name in OEC.
      category is one of ['system', 'star', 'planet'].
      attribute is the name of the attribute (XML tag) to be updated (e.g. magV).
      new_value is the new value to replace the old value with.
      
    Updates the value for a given attribute (XML tag format) under a given
    category in <system_name>.xml file in OEC with new_value. The original
    <system_name>.xml file will remain unchanged if the given attribute in 
    XML tag format does not exist.
    '''
    cwd = os.getcwd()                                          # current working directory
    systems_dir = os.path.join(cwd, "systems")                 # OEC systems folder path
    all_xml = os.path.join(cwd, "all_xml")                     # all_xml folder path
    xml_path = os.path.join(systems_dir, source)               # xml file path
    new_xml_path = os.path.join(all_xml, source)               # new xml file path
    attr_list = attribute.split(' ')                           # separating words in attribute
    attribute = '<' + attr_list[0]                             # base attribute
    updated = False                                            # flag to check if data is updated
    
    # initialize all_xml folder if it doesn't exist
    if not os.path.exists(all_xml):
        os.mkdir(all_xml)
    
    # try to open specified xml file
    try:
        old_xml = open(xml_path)                               # old file
        new_xml = open(new_xml_path, 'w')                      # updated file
    except:
        print("XML file \"" + source + "\" not found")
        return
    
    # target xml file is found
    # check that category is valid
    if category not in ['system', 'star', 'planet']:
        print("Invalid category specified")
        return
    else:
        # format category into xml tag for error-prone searching
        category = '<' + category + '>'
    
    # category is valid
    # look for <category> section to update in xml file
    for line in old_xml:
        if category in line:
            new_xml.write(line)
            break
        else:
            new_xml.write(line)
            
    # look for section with correct <system_name> to update in xml file
    system_name = '>' + system_name + '<'
    
    for line in old_xml:
        if system_name in line:
            new_xml.write(line)
            break
        else:
            new_xml.write(line)
    
    # found <category> section to update
    for line in old_xml:
        if ((attribute in line) and (updated == False)):
            if 'errorminus' in attr_list:
                # updating 'errorminus' value
                line_offset = line.find('errorminus') + 10     # 10 == len('errorminus')
                data_offset = line_offset + 2                  # len('errorminus') + 2
                end_offset = line[data_offset:].find('\"')     # offset after data value
                
                # write line with new value
                new_xml.write(line[0:line_offset] + '=\"' + 
                              str(new_value) + 
                              line[(data_offset + end_offset):])
                
                # set updated flag to True to stop checking remaining lines
                updated = True
                
            elif 'errorplus' in attr_list:
                # updating 'errorplus' value
                line_offset = line.find('errorplus') + 9       # 9 == len('errorplus')
                data_offset = line_offset + 2                  # len('errorplus') + 2
                end_offset = line[data_offset:].find('\"')     # offset after data value
                
                # write line with new value
                new_xml.write(line[0:line_offset] + '=\"' + 
                              str(new_value) +
                              line[(data_offset + end_offset):])
                
                # set updated flag to True to stop checking remaining lines
                updated = True
                
            elif 'lowerlimit' in attr_list:
                # updating 'lowerlimit' value
                line_offset = line.find('lowerlimit') + 10     # 10 == len('lowerlimit')
                data_offset = line_offset + 2                  # len('lowerlimit') + 2
                end_offset = line[data_offset:].find('\"')     # offset after data value
                
                # write line with new value
                new_xml.write(line[0:line_offset] + '=\"' + 
                              str(new_value) +
                              line[(data_offset + end_offset):])
                
                # set updated flag to True to stop checking remaining lines
                updated = True
                
            elif 'upperlimit' in attr_list:
                # updating 'upperlimit' value
                line_offset = line.find('upperlimit') + 10     # 10 == len('upperlimit')
                data_offset = line_offset + 2                  # len('upperlimit') + 2
                end_offset = line[data_offset:].find('\"')     # offset after data value
                
                # write line with new value
                new_xml.write(line[0:line_offset] + '=\"' + 
                              str(new_value) +
                              line[(data_offset + end_offset):])
                
                # set updated flag to True to stop checking remaining lines
                updated = True
                
            else:
                # not updating any of the above subtag values
                line_offset = line.find('>') + 1
                end_offset = line[line_offset:].find('<')
                
                # write line with new value
                new_xml.write(line[0:line_offset] + 
                              str(new_value) +
                              line[(line_offset + end_offset):])
                
                # set updated flag to True to stop checking remaining lines
                updated = True
                
        else:
            # attribute not in line
            new_xml.write(line)
            
    # done writing new xml file
    # replace old xml file with new xml file
    old_xml.close()
    new_xml.close()
    shutil.copy2(new_xml_path, xml_path)
    
# Example test cases / usage
# Note: create a test file first with "<system_name>.xml" as file name
#       and populate the test file with existing OEC data.
#       (e.g. open "Com 11.xml" and copy+paste the data into the test file)
#
#       the test file should be located in systems folder.
#       
#       update_oec_xml.py should be located in one directory above systems folder
#       (e.g. same directory as OEC_main.py)

'''
update_oec_xml("11 Com", "system", "name", "test name", "0test.xml")
update_oec_xml("11 Com", "system", "distance", 0.00, "0test.xml")
update_oec_xml("11 Com", "system", "distance errorplus", 1.0, "0test.xml")
update_oec_xml("11 Com", "system", "magV", 0.00, "0test.xml")
update_oec_xml("11 Com", "system", "magB", 0.00, "0test.xml")
update_oec_xml("11 Com", "system", "mass errorplus", 12.34, "0test.xml")
update_oec_xml("11 Com", "system", "mass errorminus", 43.21, "0test.xml")
update_oec_xml("11 Com", "star", "name", "test name", "0test.xml")
update_oec_xml("11 Com", "planet", "name", "test name", "0test.xml")
update_oec_xml("1RXS1609 b", "planet", "mass upperlimit", 789.012, "01test.xml")
update_oec_xml("1RXS1609 b", "planet", "mass lowerlimit", 123.456, "01test.xml")
update_oec_xml("Gliese 667 B", "star", "age errorminus", "TESTVALUE1", "Gliese 667.xml")
update_oec_xml("Gliese 667 C h", "planet", "eccentricity errorminus", "TESTVALUE2", "Gliese 667.xml")
update_oec_xml("24 Sex c", "planet", "semimajoraxis", "TESTVALUE3", "24 Sex.xml")
'''