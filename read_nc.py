# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 18:26:51 2022

@author: lasse
"""
#Importing necessary libraries
from scipy import io
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

print("[PROMPT] Choose file to extract XYZ data from: ")
for idx in fileList_dict:
    #Printing each filename in the filepath
    print('[%s] %s' % (idx, fileList_dict[idx]))
    
print("")
print('[%d] All' % (len(fileList_dict)))

#User chooses which of the files to retrieve XYZ from. All is an option.
choice = input("[PROMPT] Choose option: ")


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



def extract_xyz(filepath):
    
    print("[INFO] LOADING FIRST FILE ...")
    data = io.netcdf_file(filepath, mode='r')
    
    #Retrieving filename without .filetype extension.
    filename = os.path.basename(filepath).split('.')[0]
    print("[INFO] FILE: %s" % filename)
    
    #setting default keys for x, y and z
    x_key = 'lat'
    y_key = 'lon'
    z_key = 'lat'
    
    #Creating while loop that runs until a valid key is chosen for x, y and z data.
    
    invalidKey = 1
    while invalidKey:
        try:
            x = data.variables[x_key][:].copy()
            invalidKey = 0
        except KeyError:
            print("")
            print("[ERROR] %s not a variable in the data..." % x_key)
            print("[INFO] List of variables: ")
            
            # Prompts user to type in a desired key for the X-data
            print([variable for variable in data.variables.keys()])
            x_key = input("[PROMPT] Choose new X var: ")
            
    invalidKey = 1    
    while invalidKey:
        try:
            y = data.variables[y_key][:].copy()
            invalidKey = 0
        except KeyError:
            print("")
            print("[ERROR] %s not a variable in the data..." % y_key)
            print("[INFO] List of variables: ")
            
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
            print("")
            print("[ERROR] %s not a variable in the data..." % z_key)
            print("[INFO] List of variables: ")
            
            # Prints list of valid variable keys to choose
            print([variable for variable in data.variables.keys()])
            
            # Prompts user to type in a desired key for the Z-data
            z_key = input("[PROMPT] Choose new Z var: ")
    

    #Checking if X, Y and Z are of equal length
    varListEqualLength = sameNumVariables(x, y, z)
    if varListEqualLength:

        #Creating dataframe
        df = pd.DataFrame(list(zip(x, y, z)), columns=[x_key, y_key, z_key])
        
        #Exporting values to csv file
        df.to_csv(xyz_filepath + '/' + filename + '_xyz.csv', index=False)  
        print("====================================")
        print("[SUCCES] %s_xyz.csv printed to %s" % (filename, xyz_filepath))
        print("====================================")
        
    else:
        print("[ERROR] List of variables for export are not equal length ... Values were not exported")  
        print("   X: %d values" % len(x))  
        print("   Y: %d values" % len(y))  
        print("   Z: %d values" % len(z))

        

# Perform extraction task based on file-prompt.
if int(choice) < len(fileList_dict):
    extract_xyz(os.path.join('%s/%s' % (nc_filepath, fileList_dict[choice]) 
                              ) 
                )
elif int(choice) >= len(fileList_dict): #Performs extraction on all files in nc_files/
    [extract_xyz(os.path.join('%s/%s' % (nc_filepath, fileList_dict[str(idx)]))) for idx in range(0, len(fileList_dict))]

    
