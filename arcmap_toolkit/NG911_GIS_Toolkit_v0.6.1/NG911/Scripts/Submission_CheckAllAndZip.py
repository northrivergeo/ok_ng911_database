#-------------------------------------------------------------------------------
# Name:        Submission_CheckAllAndZip
# Purpose:     Runs all data checks and zips geodatabase if it passes
#
# Author:      kristen (KS), Baker(OK), Baird (OK)
#
# Created:     20/10/2015
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------
from Validation_CheckAll import validateAllPrep
from NG911_User_Messages import userMessage
from arcpy import GetParameterAsText

def main():
    gdb = GetParameterAsText(0)
    zipOutput = GetParameterAsText(1)

    if zipOutput[-3:] != "zip":
        userMessage("Output zip file is not valid. Make sure it ends in '.zip' and please try again.")

    else:
        validateAllPrep(gdb, "true", zipOutput)

if __name__ == '__main__':
    main()
