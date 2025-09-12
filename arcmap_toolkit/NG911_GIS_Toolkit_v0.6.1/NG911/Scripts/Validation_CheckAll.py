#-------------------------------------------------------------------------------
# Name:        Validation_CheckAll
# Purpose:     Check all validation scripts
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     20/10/2015
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------
from NG911_DataCheck import sanityCheck
from arcpy import GetParameterAsText, Exists
from Conversion_ZipNG911Geodatabase import createNG911Zip
from NG911_GDB_Objects import NG911_Session
from os.path import basename
import os
from NG911_arcpy_shortcuts import hasRecords
from NG911_User_Messages import *
from datetime import datetime


def validateAllPrep(gdb, zipFlag, zipPath):
    """
    Performs sanity check for check-all validation or for preparation for submission of the geodatabase.

    Parameters
    ----------
    gdb : str
        Full path to the geodatabase
    zipFlag : str
        Either "true" or "false" as strings, not as booleans
    zipPath : str
        Path to which the geodatabase should be exported as a zip file
    """
    #get session object
    session_object = NG911_Session(gdb)

    #make sure all existing layers are checked
    fcPossList = session_object.gdbObject.fcList

    fcList = []
    for fc in fcPossList:
        if Exists(fc):
            if hasRecords(fc):
                fcList.append(fc)
            else:
                userMessage(basename(fc) + " has no records and will not be checked.")
    userMessage("Layers to check: %s" % ", ".join(fcList))

    session_object.gdbObject.fcList = fcList

    #run sanity checks
    sanity = 0
    sanity = sanityCheck(session_object)

    if sanity == 1 and zipFlag == "true":
        createNG911Zip(gdb, zipPath)

    if sanity == 0 and zipFlag == "true":
        userMessage("Several issues with the data need to be addressed prior to submission. Data will not be zipped.")

    # Write pass/fail textfile to the directory containing the gdb
    textfile_path = gdb.strip(".gdb") + ".txt"
    if os.path.isfile(textfile_path):
        os.remove(textfile_path)
    # folder = dirname(gdb)
    # gdb_basename = basename(gdb)
    # if gdb_basename[-4:] == ".gdb":
    #     textfile = "%s.txt" % gdb_basename[:-4]
    #     userMessage(textfile)
    # else:
    #     textfile = gdb_basename
    #     userMessage(textfile)
    # textfile_path = join(folder, textfile)
    lines = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "\n",
        "PASS" if sanity is 1 else "FAIL"
    ]
    with open(textfile_path, "w") as f:
        f.writelines(lines)

def main():
    import time

    startTime = time.time()
    gdb = GetParameterAsText(0)
    validateAllPrep(gdb, "false", "")
    endTime = time.time()
    print("Running time was %g minutes\n" % round(((endTime - startTime)/60.0),1))

if __name__ == '__main__':
    main()
