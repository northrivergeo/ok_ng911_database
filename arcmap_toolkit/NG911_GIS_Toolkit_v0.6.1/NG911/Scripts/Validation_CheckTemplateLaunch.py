#-------------------------------------------------------------------------------
# Name:        NG911_CheckTemplateLaunch
# Purpose:     Launches script to check NG911 template
#
# Author:      kristen (KS), Baker (OK)
#
# Created:     24/11/2014
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------
from NG911_GDB_Objects import NG911_Session
from arcpy import GetParameterAsText
from NG911_DataCheck import main_check

def main():

    #get parameters
    gdb = GetParameterAsText(0)
    checkLayerList = GetParameterAsText(1)
    checkRequiredFields = GetParameterAsText(2)
    checkRequiredFieldValues = GetParameterAsText(3)
    checkSubmissionNumbers = GetParameterAsText(4)
    findInvalidGeometry = GetParameterAsText(5)
    gdbDomainCheck = GetParameterAsText(6)

    session_object = NG911_Session(gdb)

    #create check list
    checkList = [checkLayerList, checkRequiredFields, checkRequiredFieldValues, checkSubmissionNumbers, findInvalidGeometry, gdbDomainCheck]

    #set object parameters
    checkType = "template"
    session_object.checkList = checkList


    #launch the data check
    main_check(checkType, session_object)

if __name__ == '__main__':
    main()
