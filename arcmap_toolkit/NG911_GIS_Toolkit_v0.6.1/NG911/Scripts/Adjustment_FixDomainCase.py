#-------------------------------------------------------------------------------
# Name:        Adjustment_FixDomainCase
# Purpose:     Fix domain errors where just the case is wrong
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     21/10/2015
# Modified:    December 4, 2020
#-------------------------------------------------------------------------------
from arcpy import GetParameterAsText
from NG911_DataFixes import FixDomainCase
from NG911_GDB_Objects import NG911_Session
from arcpy.da import Editor


def main():
    gdb = GetParameterAsText(0)

    edit = Editor(gdb)
    edit.startEditing(False, False)

    FixDomainCase(gdb, NG911_Session(gdb))

    edit.stopEditing(True)

if __name__ == '__main__':
    main()
