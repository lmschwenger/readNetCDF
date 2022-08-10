# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 18:26:51 2022

@author: lasse
"""
#Importing necessary libraries
import netCDF4 as nc
import pandas as pd
import os

#Retrieving absolute path of this file and setting it to current directory.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Setting input filepath
nc_filepath = os.path.join(os.getcwd()+'/nc_files')
# Setting output filepath
xyz_filepath = os.path.join(os.getcwd()+'/xyz_files')
#Creating dict of filenames in input path.
fileList_dict = {str(idx):file for idx,file in enumerate(os.listdir(nc_filepath))}

""" Shows list of files in /nc_files/ that can be converted """

print("[INFO] FILES FOUND IN /nc_files/: ")
[print('[%s] %s' % (i, fileList_dict[i])) for i in fileList_dict.keys()] #Printing files
print("")
print('[%d] All' % (len(fileList_dict)))
#User chooses which of the files to retrieve XYZ from. All is an option.
choice = input("[PROMPT] Choose file to extract XYZ data from: ")


#Creating folder for converted files
if not os.path.isdir(dname+'/xyz_files'):
    os.mkdir(os.path.join(dname+r'\xyz_files'))
    print("Created folder for xyz files (%s)" % os.path.join(dname+r'\xyz_files'))

def sameNumVariables(x, y, z):
    """    Checks if X, Y and Z are of equal length     """
    if len(x) == len(y) and len(x) == len(z):
        return 1
    else:
        return 0

def invalidKeyMsg(key):
    """  
        Returns an error message to cmd if specified 
        key is not a variable in the dataset 
                                                    """
    print("")
    print("[ERROR] %s not a variable in the data..." % key)
    print("[INFO] List of variables: ")
    

def extract_xyz(filepath):
    
    print("[INFO] LOADING FILE ...")
    data = nc.Dataset(filepath, mode='r')
    #Retrieving filename without .filetype extension.
    filename = os.path.basename(filepath).split('.')[0]
    print("[INFO] FILE: %s" % filename)
    #setting default keys for x, y and z
    x_key = 'latitude'
    y_key = 'longitude'
    z_key = 'latitude'
    
    #Creating while loop that runs until a valid key is chosen for x, y and z data.
    invalidKey = 1
    while invalidKey:
        try:
            x = data.variables[x_key][:].copy()
            invalidKey = 0
        except KeyError:
            #Returns cmd message stating key (variable) is not in dataset
            invalidKeyMsg(x_key)
            # Prompts user to type in a desired key for the X-data
            print([variable for variable in data.variables.keys()])
            x_key = input("[PROMPT] Choose new X var: ")
            
    invalidKey = 1    
    while invalidKey:
        try:
            y = data.variables[y_key][:].copy()
            invalidKey = 0
        except KeyError:
            #Returns cmd message stating key (variable) is not in dataset
            invalidKeyMsg(y_key)
            # Prints list of valid variable keys to choose
            print([variable for variable in data.variables.keys()])
            # Prompts user to type in a desired key for the Y-data
            y_key = input("[PROMPT] Choose new Y var: ")   
    
    invalidKey = 1
    while invalidKey:
        try:
            z = data.variables[z_key][:].copy()
            invalidKey = 0
        except KeyError:
            #Returns cmd message stating key (variable) is not in dataset
            invalidKeyMsg(z_key)
            # Prints list of valid variable keys to choose
            print([variable for variable in data.variables.keys()])
            # Prompts user to type in a desired key for the Z-data
            z_key = input("[PROMPT] Choose new Z var: ")
    
    

    #Checking if X, Y and Z are of equal length
    varListEqualLength = sameNumVariables(x, y, z)
    if varListEqualLength:
        """ If all variables have same number of values --> Start compiling export files """
        #Creating dataframe
        df = pd.DataFrame(list(zip(x, y, z)), columns=[x_key, y_key, z_key])
        #Exporting values to csv file
        df.to_csv(xyz_filepath + '/' + filename + '_xyz.csv', index=False)
        #Creating .txt file with units of the exported data.
        with open(xyz_filepath + '/' + filename + '_units.txt', 'w') as writer:
            writer.write('Variable,Unit\n')   
            writer.write('%s,%s\n%s,%s\n%s,%s\n' % (x_key, data.variables[x_key].units, 
                                                  y_key, data.variables[y_key].units, 
                                                  z_key, data.variables[z_key].units))
        writer.close()
        print("====================================")
        print("[SUCCES] %s_xyz.csv printed to %s" % (filename, xyz_filepath))
        print("[SUCCES] %s_units.csv printed to %s" % (filename, xyz_filepath))
        print("====================================")
    else:
        print("[ERROR] List of variables for export are not equal length ... Values were not exported")  
        print("   X: %d values" % len(x))  
        print("   Y: %d values" % len(y))  
        print("   Z: %d values" % len(z))
    #Closing file
    data.close()        

# Perform extraction task based on file-prompt.
if int(choice) < len(fileList_dict) and int(choice) >= 0:
    extract_xyz(os.path.join('%s/%s' % (nc_filepath, fileList_dict[choice]) 
                              ) 
                )
elif int(choice) >= len(fileList_dict): #Performs extraction on all files in nc_files/
    [extract_xyz(os.path.join('%s/%s' % (nc_filepath, fileList_dict[str(idx)]))) for idx in range(0, len(fileList_dict))]

else:
    print("Invalid index for file. Try over and only choose values between 0 and %s" % len(fileList_dict))
