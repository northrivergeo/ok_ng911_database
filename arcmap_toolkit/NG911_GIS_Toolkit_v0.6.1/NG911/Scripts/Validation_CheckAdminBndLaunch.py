#-------------------------------------------------------------------------------
# Name:        NG911_CheckAdminBndLaunch
# Purpose:     Launches script to check NG911 administrative boundaries
#
# Author:      kristen (KS), Baker (OK)
#
# Created:     25/11/2014
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------

def main():
    from arcpy import GetParameterAsText, Exists
    from os.path import join
    from NG911_DataCheck import main_check
    from NG911_GDB_Objects import NG911_Session

    #get parameters
    gdb = GetParameterAsText(0)
    checkValuesAgainstDomain = GetParameterAsText(1)
    checkFeatureLocations = GetParameterAsText(2)
    checkUniqueIDs = GetParameterAsText(3)

    #create check list
    checkList = [checkValuesAgainstDomain,checkFeatureLocations,checkUniqueIDs]

    #set object parameters
    checkType = "admin"
    session_object = NG911_Session(gdb)
    NG911_Session.checkList = checkList
    gdbObject = session_object.gdbObject

    adminList = gdbObject.AdminBoundaryList
    fcList = []
    for admin in adminList:
        path = join(gdb, admin)
        if Exists(path):
            fcList.append(path)

    #redo various settings to limit what is checked
    session_object.gdbObject.fcList = fcList
    session_object.gdbObject.esbList = []
    session_object.checkList = checkList

    #launch the data check
    main_check(checkType, session_object)

if __name__ == '__main__':
    main()
