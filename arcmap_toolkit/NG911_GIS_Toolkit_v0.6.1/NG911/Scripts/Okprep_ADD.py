#-------------------------------------------------------------------------------
# Name:        Okprep_ADD.py
# Purpose:     Converts ArcGIS field inputs from an Address Point layer to correct field names.
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     February 10, 2020
# Modified:    July 17
# , 2020
# Copyright:   (c) Emma Marie Baker, Riley Baird, 2020
#-------------------------------------------------------------------------------
## Imports
from arcpy import GetParameterAsText
from Okprep_createFC import create_feature_class
from os.path import join
from NG911_GDB_Objects import NG911_Session


def main():

    ## Get Parameters from ArcGIS Inputs
    inputLayer = GetParameterAsText(0)
    # fieldFile = GetParameterAsText(1)
    output_gdb = GetParameterAsText(1)
    piter = 62
    fieldNames = []
    for val in range(2, piter + 2):
        fieldNames.append(GetParameterAsText(val))

    correct_name = "ADDRESS_POINT"

    session = NG911_Session(output_gdb)
    fields_folder = session.fieldsFolderPath
    file_name = "ADDRESS_POINT.txt"
    fieldFile = join(fields_folder, file_name)

    create_feature_class("POINT", inputLayer, fieldFile, fieldNames, output_gdb, correct_name, True)

if __name__ == '__main__':
    main()
