#-------------------------------------------------------------------------------
# Name:        Okprep_MUNI.py
# Purpose:     Converts ArcGIS field inputs from aN ESB_EMS_Boundary Polygon layer to correct field names.
#
# Author:      Baker, Baird (OK)
#
# Created:     July 16, 2020
# Modified:    July 16, 2020
# Copyright:   (c) Emma Marie Baker 2020, Riley Baird, 2020
#-------------------------------------------------------------------------------
## Imports
from arcpy import GetParameterAsText
from Okprep_createFC import create_feature_class
from os.path import join
from NG911_GDB_Objects import NG911_Session


def main():

    ## Get Parameters from ArcGIS Inputs and assign ArcGIS inputs to a list
    inputLayer = GetParameterAsText(0)
    # fieldFile = GetParameterAsText(1)
    output_gdb = GetParameterAsText(1)
    piter = 18
    fieldNames = []
    for val in range(2, piter + 2):
        # userMessage(val)
        fieldNames.append(GetParameterAsText(val))

    correct_name = "ESB_EMS_BOUNDARY"

    session = NG911_Session(output_gdb)
    fields_folder = session.fieldsFolderPath
    file_name = "ESB_EMS_BOUNDARY.txt"
    fieldFile = join(fields_folder, file_name)

    create_feature_class("POLYGON", inputLayer, fieldFile, fieldNames, output_gdb, correct_name, True)

if __name__ == '__main__':
    main()
