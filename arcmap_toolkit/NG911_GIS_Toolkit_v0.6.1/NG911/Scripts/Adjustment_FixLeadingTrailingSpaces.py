#-------------------------------------------------------------------------------
# Name:        Adjustment_FixLeadingTrailingSpaces
# Purpose:     Removes leading and trailing spaces from all MSAGCO fields
#
# Author:      kristen (KS), Emma Baker (OK), Riley Baird (OK)
#
# Created:     09/28/2017
# Modified:    December 4, 2020
#-------------------------------------------------------------------------------
from arcpy import GetParameterAsText
from arcpy.da import Editor
from NG911_DataFixes import FixMSAGCOspaces

def main():
    gdb = GetParameterAsText(0)
    ap_check = GetParameterAsText(1)
    road_check = GetParameterAsText(2)

    check_list = [ap_check, road_check]

    edit = Editor(gdb)
    edit.startEditing(False, False)

    FixMSAGCOspaces(gdb, check_list)

    edit.stopEditing(True)

if __name__ == '__main__':
    main()
