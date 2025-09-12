#-------------------------------------------------------------------------------
# Name:        NG911_ClearOldResults
# Purpose:     Delete rows indicating past errors
#
# Author:      kristen (KS), Baker (OK)
#
# Created:     09/12/2014
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------
from arcpy import GetParameterAsText, DeleteRows_management, Exists
from os.path import basename
from NG911_GDB_Objects import getGDBObject
from NG911_User_Messages import *


def main():
    """
    Clears the results tables.
    """
    gdb = GetParameterAsText(0)
    templateTableClear = GetParameterAsText(1)
    fieldValuesTableClear = GetParameterAsText(2)

    ClearOldResults(gdb, templateTableClear, fieldValuesTableClear)

def ClearOldResults(gdb, templateTableClear, fieldValuesTableClear):
    """
    Clears the selected table(s). Options include *TemplateCheckResults* and *FieldValuesCheckResults*. See parameters
    `

    Parameters
    ----------
    gdb : str
        Full path to geodatabase
    templateTableClear : str
        String representation of a boolean, either `"true"` or `"false"`. If `"true"`, the *TemplateCheckResults* table
        will be cleared.
    fieldValuesTableClear : str
        String representation of a boolean, either `"true"` or `"false"`. If `"true"`, the *FieldValuesCheckResults*
        table will be cleared.
    """
    gdbObject = getGDBObject(gdb)

    if templateTableClear == "true":
        templateTable = gdbObject.TemplateCheckResults
        if Exists(templateTable):
            DeleteRows_management(templateTable)
            userMessage(basename(templateTable) + " cleared")

    if fieldValuesTableClear == "true":
        fieldValuesTable = gdbObject.FieldValuesCheckResults
        if Exists(fieldValuesTable):
            DeleteRows_management(fieldValuesTable)
            userMessage(basename(fieldValuesTable) + " cleared")

if __name__ == '__main__':
    main()
