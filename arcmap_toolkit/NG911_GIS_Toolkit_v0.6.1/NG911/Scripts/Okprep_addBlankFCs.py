#-------------------------------------------------------------------------------
# Name:        Okprep_addBlankFCs.py
# Purpose:     Adds a standard compliant blank feature class to a standard compliant GDB
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     April 26, 2021
# Modified:    April 26, 2021
# Copyright:   (c) Emma Marie Baker 2021, Riley Baird, 2021
#-------------------------------------------------------------------------------

## Imports
from arcpy import GetParameterAsText, Delete_management
from os.path import join
from NG911_User_Messages import *
from Okprep_createBlankFC import create_blank_feature_class
from NG911_GDB_Objects import NG911_Session


try:
    from typing import List
except:
    pass


def main():
    # type:  None
    """
    Adds a standards-compliant blank feature class to a standards-compliant GDB. In order, this function:

    * Gets standard field information from a text file
    * Creates feature class based on standards

    """

    # gdb path
    input_gdb = GetParameterAsText(0)
    # str: true/false
    address = GetParameterAsText(1)
    road = GetParameterAsText(2)
    discrepancy = GetParameterAsText(3)
    esz_layer = GetParameterAsText(4)
    esb_fire = GetParameterAsText(5)
    esb_law = GetParameterAsText(6)
    esb_ems = GetParameterAsText(7)
    psap_layer = GetParameterAsText(8)

    geometry = ""
    layer_creation = [address, road, discrepancy, esz_layer, esb_fire, esb_law, esb_ems, psap_layer]
    layer_name = ["ADDRESS_POINT", "ROAD_CENTERLINE", "DISCREPANCYAGENCY_BOUNDARY", "ESZ_BOUNDARY", "ESB_FIRE_BOUNDARY", "ESB_LAW_BOUNDARY", "ESB_EMS_BOUNDARY", "PSAP_BOUNDARY"]

    session = NG911_Session(input_gdb)
    fields_folder = session.fieldsFolderPath

    for key, layer in enumerate(layer_creation):
        if layer == "true":
            if key == 0:
                geometry = "POINT"
            elif key == 1:
                geometry = "POLYLINE"
            elif key > 1:
                geometry = "POLYGON"
            field_file = join(fields_folder, layer_name[key] + ".txt")
            correct_name = layer_name[key]
            blank_result = create_blank_feature_class(geometry, field_file, input_gdb, correct_name, required=True)
            if blank_result == "FIELD ISSUE":
                userWarning("Failed to create blank feature class %s. Deleting FC; please check GDB." % correct_name)
                Delete_management(join(input_gdb, correct_name))
            elif blank_result == "NAME ISSUE":
                userWarning("Failed to create blank feature class %s. Feature class name already exists." % correct_name)
                continue
            elif blank_result == "SUCCESS":
                userMessage("Blank Feature Class %s has been added to the GDB." % correct_name)

    # userMessage("Blank Feature Class(es) has(ve) been added to the GDB.")

if __name__ == "__main__":
    main()