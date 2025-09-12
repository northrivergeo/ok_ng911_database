"""
------------------------------------------------------------------------------
Name:        Validation_CheckNENAIDFormat
Purpose:     Checks to ensure that the NENA unique ID is correctly-formatted.

Author:      Baker (OK), Baird (OK)

Created:     April 27, 2021
Modified:    April 27, 2021
Copyright:   (c) Emma Marie Baker, Riley Baird
------------------------------------------------------------------------------
"""

from os.path import join

import arcpy
from arcpy import GetParameterAsText
from arcpy.da import InsertCursor

from NG911_DataCheck import checkUniqueIDFormat
from NG911_User_Messages import *


def main():
    """
    Checks to ensure that the NENA unique ID is correctly-formatted.
    Format: (LayerName)_(Local911UniqueID)@(Agency_ID)
    """

    layer_name = GetParameterAsText(0)  # type: str  # will be one of the standard feature class names
    input_fc = GetParameterAsText(1)  # type: str
    input_field = GetParameterAsText(2)  # type: str
    results_folder = GetParameterAsText(3)  # type: str

    table_path = join(results_folder, "NENAIDCheckResults.dbf")
    if arcpy.Exists(table_path):
        arcpy.Delete_management(table_path)

    bad_ids, null_ids, good_ids = checkUniqueIDFormat(input_fc, layer_name, input_field, False)


    if len(bad_ids) > 0:
        arcpy.CreateTable_management(results_folder, "NENAIDCheckResults.dbf")
        arcpy.AddField_management(table_path, "NENA_ID", "TEXT", field_length=254)
        arcpy.DeleteField_management(table_path, "Field1")

        with InsertCursor(table_path, "NENA_ID") as cursor:
            for bad_id in bad_ids:
                cursor.insertRow((bad_id, ))

        userWarning("There were %i feature(s) with incorrectly-formatted NENA unique IDs. Consider running Enhancement - Assign Unique NENA ID." % len(bad_ids))

    if null_ids > 0:
        userWarning("There were %i feature(s) with null NENA unique IDs. Consider running Enhancement - Assign Unique NENA ID." % null_ids)

    if len(bad_ids) == 0 and null_ids == 0:
        userMessage("All NENA Unique IDs are formatted correctly.")



if __name__ == "__main__":
    main()
