#-------------------------------------------------------------------------------
# Name:        Okprep_RDCL.py
# Purpose:     Converts ArcGIS field inputs from an RoadCenterline Polyline layer to correct field names.
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     February 13, 2020
# Modified:    July 16, 2020
# Copyright:   (c) Emma Marie Baker, Riley Baird, 2020
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
    gdbpath = GetParameterAsText(1)
    piter = 78
    fieldNames = []
    for val in range(2, piter + 2):
        # userMessage(val)
        fieldNames.append(GetParameterAsText(val))

    correct_name = "ROAD_CENTERLINE"

    session = NG911_Session(gdbpath)
    fields_folder = session.fieldsFolderPath
    file_name = "ROAD_CENTERLINE.txt"
    fieldFile = join(fields_folder, file_name)

    create_feature_class("POLYLINE", inputLayer, fieldFile, fieldNames, gdbpath, correct_name, True)

if __name__ == '__main__':
    main()

