#-------------------------------------------------------------------------------
# Name:        Conversion_AP_RCLMATCH_NO_MATCH
# Purpose:     Auto-populates any empty RCLMatch 2.1 address point records with "NO_MATCH"
#
# Author:      kristen (KS), Emma Baker (OK), Riley Baird (OK)
#
# Created:     10/11/2017
# Modified:    June 17, 2022
#
# Copyright:   (c) kristen 2017
#-------------------------------------------------------------------------------
from arcpy import GetParameterAsText, Exists

from NG911_GDB_Objects import getGDBObject, getFCObject, NG911_Address_Object
from NG911_arcpy_shortcuts import hasRecords, fieldExists
from NG911_User_Messages import *
from arcpy.da import Editor, UpdateCursor

def main():
    gdb = GetParameterAsText(0)
    overwrite_ties = GetParameterAsText(1)  # type: str  # Boolean as string

    gdb_object = getGDBObject(gdb)
    ap_path = gdb_object.AddressPoints
    ap_obj = getFCObject(ap_path)  # type: NG911_Address_Object

    rclmatch_field = ap_obj.RCLMatch  # type: str
    ties_value = "TIES"  # Value used in RCLMatch field for ties
    no_match_value = "NO_MATCH"  # Value used in RCLMatch field when no match is found

    # Make sure the address point file exists and has records, otherwise return
    if not Exists(ap_path) or not hasRecords(ap_path):
        userWarning("Address point file does not exist or does not have records. Please check " + gdb)
        return

    # Make sure the address point file has an RCLMatch field, otherwise return
    elif not fieldExists(ap_path, rclmatch_field):
        userWarning("Address point feature class does not have %s field." % rclmatch_field)
        return

    # Determine appropriate where clause based on overwrite_ties
    if overwrite_ties == "true":
        # Where clause will include nulls and ties
        wc = "%s IN (NULL, '', ' ', '%s')" % (rclmatch_field, ties_value)
    else:
        # Where clause will include only nulls, not ties
        wc = "%s IN (NULL, '', ' ')" % rclmatch_field

    updated_null_count = 0  # type: int
    updated_ties_count = 0  # type: int
    edit = Editor(gdb)
    edit.startEditing(False, False)
    with UpdateCursor(ap_path, (rclmatch_field, ), wc) as cursor:
        for row in cursor:
            if row[0] == ties_value:  # Only ever true when where clause includes ties
                updated_ties_count += 1
            else:
                updated_null_count += 1
            row[0] = no_match_value
            cursor.updateRow(row)

    edit.stopEditing(True)

    if overwrite_ties == "true":
        userMessage('%i null values and %i "%s" values were overwritten with "%s".' % (updated_null_count, updated_ties_count, ties_value, no_match_value))
    else:
        userMessage('%i null values were overwritten with "%s".' % (updated_null_count, no_match_value))


if __name__ == '__main__':
    main()
