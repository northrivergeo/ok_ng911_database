# -*- #################
# ---------------------------------------------------------------------------
# Script for assigning a NENA unique identifier to a field in an Esri feature class
# Author:  Emma Baker, Riley Baird, Oklahoma DOT GIS
# Created: January 3, 2020
# Modified: December 4, 2020
# ---------------------------------------------------------------------------

# Import arcpy module
from arcpy import GetParameterAsText, MakeFeatureLayer_management, SelectLayerByAttribute_management, CalculateField_management
from NG911_User_Messages import *
from arcpy.da import UpdateCursor, SearchCursor, Editor
from os.path import dirname
import arcpy
import re

def assign_id():
    # Set the parameters and variables
    layertype = GetParameterAsText(0)  # type: str  # will be one of the standard feature class names
    input_FC = GetParameterAsText(1)
    Field_Name = GetParameterAsText(2)
    Source_Name = GetParameterAsText(3)
    UniqueID_Name = GetParameterAsText(4)
    overwrite_command = GetParameterAsText(5)

    gdb = dirname(dirname(input_FC))
    edit = Editor(gdb)
    edit.startEditing(False, False)

    # AddMessage(FC)
    # AddMessage(streetname_field_name)
    # userMessage(UniqueID_Name)

    # Calculate the value of the Unique ID field using UpdateCursor (arcpy.da)
    # with UpdateCursor(FC,[streetname_field_name,"DiscrpAgID"]) as cursor:

    # Checks for overwrite command provided by user. If overwrite command is false, create a subset of data where Field_Name
    # (Unique NENA ID) is null.
    if overwrite_command == "true":
        FC = input_FC
    else:
        FC = 'feature_layer'
        arcpy.MakeFeatureLayer_management(input_FC, FC, where_clause="%s IS NULL" % Field_Name)

    # Creates cursors for NENA ID update. If UniqueID_Name (Local ID) is provided, then cursor include the UniqueID_Name field.
    # If UniqueID_Name is not provided, then two cursors are created: one for NENA ID updates and one for find existing maximum.
    if UniqueID_Name is not "":
        cursor = UpdateCursor(FC, [Field_Name, Source_Name, UniqueID_Name, "OID@"])
        cursor2 = None
    else:
        cursor = UpdateCursor(FC, [Field_Name, Source_Name, "OID@"])
        cursor2 = SearchCursor(input_FC, [Field_Name, "OID@"])

    # Search for current_max if UniqueID_Name is not provided. Current_max remains 0 if UniqueID_Name is provided (i.e. cursor2
    # is None).
    current_max = 0
    if overwrite_command == "false":
        if cursor2 is not None:
            for row in cursor2:
                if row[0] in [None, "", " "]:
                    continue
                current_number = row[0][row[0].rindex("_")+1:row[0].index("@")]
                # userMessage(current_number)
                regex = "^[{}A-Za-z\d-]+$"
                if re.match(regex, unicode(current_number)) is None:
                    userWarning("Current NENA ID %s is not valid for Object ID %s." % (unicode(row[0]), unicode(row[1])))
                    continue
                try:
                    if long(current_number) >= current_max:
                        current_max = long(current_number)
                except:
                    # this id is not a number
                    pass


    # with UpdateCursor(FC,[streetname_field_name,Source_Name,Steward_Name]) as cursor:
    with cursor:
        # Layer Identifier
        word = input_FC.upper()
        debugMessage(word)
        FCName = input_FC.split("\\")
        search = FCName[-1].upper()
        userMessage("----------------")
        userMessage("Add NENA Unique IDs to " + FCName[-1] + " layer.")


        rec = 0
        # Write Unique ID
        if UniqueID_Name == "":
            for row in cursor:
                pStart = current_max + 1
                pInterval = 1
                if (rec == 0):
                    rec = pStart
                else:
                    rec = rec + pInterval
                if row[1] is not None:
                    row[0] = layertype + "_" + unicode(rec) + "@" + row[1].replace(" ", "")
                else:
                    userWarning("Agency ID is null for Object ID %s. Not generating NENA ID for object." % unicode(row[2]))
                    continue
                cursor.updateRow(row)
        else:
            for row in cursor:
                regex = "^[{}A-Za-z\d-]+$"
                if re.match(regex, unicode(row[2])) is None:
                    userWarning("Local unique ID %s is not valid for Object ID %s. Not generating NENA ID for object." % (unicode(row[2]), unicode(row[3])))
                    continue
                if row[1] is not None:
                    row[0] = layertype + "_" + unicode(row[2]) + "@" + unicode(row[1]).replace(" ", "")
                else:
                    userWarning("Agency ID is null for Object ID %s. Not generating NENA ID for object." % unicode(row[3]))
                    continue
                # userMessage(row[0])
                cursor.updateRow(row)

        userMessage("----------------")

    edit.stopEditing(True)

if __name__ == "__main__":
    assign_id()