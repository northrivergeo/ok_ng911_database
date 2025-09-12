#-------------------------------------------------------------------------------
# Name:        NG911_CheckAddressPointsLaunch
# Purpose:     Launches script to check NG911 address points
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     24/11/2014
# Modified:    July 8, 2020
#-------------------------------------------------------------------------------

def main():
    from arcpy import GetParameterAsText
    from NG911_DataCheck import main_check
    from NG911_GDB_Objects import NG911_Session, NG911_Session_obj

    try:
        from typing import List
    except:
        pass

    #get parameters
    gdb = GetParameterAsText(0)
    checkValuesAgainstDomain = GetParameterAsText(1)
    checkFeatureLocations = GetParameterAsText(2)
    checkAddressPointFrequency = GetParameterAsText(3)
    checkUniqueIDs = GetParameterAsText(4)
    checkESZ = GetParameterAsText(5)

    #create check list
    checkList = [
        checkValuesAgainstDomain, checkFeatureLocations, checkAddressPointFrequency, checkUniqueIDs, checkESZ
    ]  # type: List[str]

    #set object parameters
    checkType = "ADDRESS_POINT" # Changed to OK Fields/Layer
    session_object = NG911_Session(gdb)  # type: NG911_Session_obj
    session_object.checkList = checkList
    session_object.gdbObject.fcList = [session_object.gdbObject.AddressPoints] #make sure fcList is limited to just address points
    session_object.gdbObject.esbList = []

    #launch the data check
    main_check(checkType, session_object)

if __name__ == '__main__':
    main()