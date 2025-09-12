#-------------------------------------------------------------------------------
# Name:        NG911_CheckRoadsLaunch
# Purpose:     Launches script to check NG911 road centerlines
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     25/11/2014
# Modified:    July 07, 2020
#-------------------------------------------------------------------------------

def main():
    from arcpy import GetParameterAsText
    from NG911_DataCheck import main_check
    from NG911_GDB_Objects import NG911_Session, NG911_Session_obj, __NG911_GDB_Object

    try:
        from typing import Union, List, Tuple
    except:
        pass

    #get parameters
    gdb = GetParameterAsText(0)
    checkValuesAgainstDomain = GetParameterAsText(1)
    checkFeatureLocations = GetParameterAsText(2)
    checkRoadFrequency = GetParameterAsText(3)
    checkUniqueIDs = GetParameterAsText(4)
    checkCutbacks = GetParameterAsText(5)
    checkDirectionality = GetParameterAsText(6)
    # checkRoadAliases = GetParameterAsText(7)
    checkAddressRanges = GetParameterAsText(7)#(8)

    #create check list
    checkList = [checkValuesAgainstDomain, checkFeatureLocations, checkRoadFrequency, checkUniqueIDs, checkCutbacks, checkDirectionality, #checkRoadAliases,
                    checkAddressRanges]  # type: List[str]

    session_object = NG911_Session(gdb)  # type: NG911_Session_obj
    gdbObject = session_object.gdbObject  # type: __NG911_GDB_Object
    roadFile = gdbObject.RoadCenterline  # type: str
    # aliasFile = gdbObject.RoadAlias

    # fcList = [roadFile, aliasFile]
    fcList = [roadFile]  # type: List[str]

    #set object parameters
    checkType = "Roads"
    session_object.gdbObject.fcList = fcList
    session_object.gdbObject.esbList = []
    session_object.checkList = checkList

    #launch the data check
    main_check(checkType, session_object)

if __name__ == '__main__':
    main()
