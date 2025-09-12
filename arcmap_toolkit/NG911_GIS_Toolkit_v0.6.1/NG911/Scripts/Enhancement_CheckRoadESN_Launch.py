#-------------------------------------------------------------------------------
# Name:        Enhancement_CheckRoadESN_Launch
# Purpose:     Launches script to check ESN values of NG911 road centerlines
#
# Author:      kristen (KS), Baker(OK)
#
# Created:     November 16, 2018
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------

def main():
    from arcpy import GetParameterAsText
    from NG911_DataCheck import checkRoadESN, checkRoadESNOK
    from NG911_GDB_Objects import NG911_Session

    #get parameters
    gdb = GetParameterAsText(0)
    advanced_check = GetParameterAsText(1)
    session_object = NG911_Session(gdb)

    #launch the data check
    if advanced_check == "true":
        checkRoadESNOK(session_object)
    else:
        checkRoadESN(session_object)

if __name__ == '__main__':
    main()
