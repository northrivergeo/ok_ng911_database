#-------------------------------------------------------------------------------
# Name:        Validation_VerifyTopologyExceptions
# Purpose:     Double check that all road centerline topology errors are noted as exceptions
#
# Author:      kristen (KS), Baker (OK)
#
# Created:     03/09/2015
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------
# from arcpy import (ExportTopologyErrors_management, AddJoin_management, GetParameterAsText,
#                    MakeFeatureLayer_management, RemoveJoin_management, Delete_management, Exists)
# from arcpy.da import SearchCursor
# from NG911_DataCheck import RecordResults
# from os.path import join, basename
# from time import strftime
# from NG911_GDB_Objects import getFCObject, getGDBObject
# from NG911_arcpy_shortcuts import fieldExists, getFastCount
# from NG911_User_Messages import userMessage

from arcpy import GetParameterAsText
from NG911_GDB_Objects import getGDBObject
# from NG911_User_Messages import *
from NG911_DataCheck import checkTopology


def main():

    gdb = GetParameterAsText(0)
    # cleanUpTopology = GetParameterAsText(1)
    gdbObject = getGDBObject(gdb)

    # userMessage("Validating topology exceptions...")

    # if cleanUpTopology == "true":
    #     cleanUpTopology = True
    # else:
    #     cleanUpTopology = False

    checkTopology(gdbObject, True, True)

    # #export topology errors as feature class
    # topology = gdbObject.Topology
    # out_basename = "NG911"
    # road = gdbObject.RoadCenterline
    # rc_obj = getFCObject(road)
    #
    # userMessage("Exporting topology errors...")
    # ExportTopologyErrors_management(topology, gdb, out_basename)
    #
    # #exporting the topology creates three layers (pt, lines, polys)
    # #we want to work with the line & point layers
    # lineErrors = out_basename + "_line"
    # pointErrors = out_basename + "_point"
    #
    # #create feature layer from the road centerline file
    # rd = "rd"
    # MakeFeatureLayer_management(road, rd)
    # rd_did_have_join = False  # This will get set to True if rd has something joined to it. If nothing is ever joined to it, attempting to remove a join will cause an error.
    #
    # if fieldExists(road, rc_obj.TopoExcept):
    #
    #     try:
    #         # try/finally blocks ensure that any necessary cleanup of intermediate feature classes can take place (if so
    #         # chosen by the user) even if something fails part of the way through
    #
    #         #set variables for working with the data
    #         recordType = "fieldValues"
    #         today = strftime("%m/%d/%y")
    #         filename = basename(road)
    #         values = []
    #         count = 0
    #
    #         #join lines & points to centerline
    #         #topology.OriginObjectID = RoadCenterline.OBJECTID
    #         for errors in (lineErrors, pointErrors):
    #             fullDataset = join(gdb, errors)
    #             #create feture layer
    #             e = "e"
    #             wc = "OriginObjectClassName = 'RoadCenterline'"
    #             MakeFeatureLayer_management(fullDataset, e, wc)
    #
    #             i = getFastCount(e)
    #             if i > 0:
    #
    #                 #add join
    #                 AddJoin_management(rd, "OBJECTID", e, "OriginObjectID")
    #                 rd_did_have_join = True
    #
    #                 #for this, only make sure dangles & outside authoritative boundary are marked as exceptions in both the topology & the road centerline
    #                 rules = ('esriTRTLineNoDangles','esriTRTLineInsideArea')
    #
    #                 #set query and field variables
    #                 qry = errors + ".OriginObjectID IS NOT NULL"
    #                 fields = ("ROAD_CENTERLINE." + rc_obj.UNIQUEID, "ROAD_CENTERLINE." + rc_obj.TopoExcept, errors + ".RuleType", errors + ".RuleDescription", errors + ".isException") # Changed to OK standards
    #
    #                 try:
    #                     #set up search cursor to loop through records
    #                     with SearchCursor(rd, fields, qry) as rows:
    #                         for row in rows:
    #                             msg = ""
    #                             segID = row[0]
    #
    #                             rule = row[2]
    #                             if rule in rules:
    #                                 #means it's really an exception
    #                                 if row[1] == "NOT EXCEPTION" and row[4] == 1:
    #                                     #not marked as an exception in the road centerline file
    #                                     msg = "Needs to be marked as a topology exception in the road centerline file"
    #                                 elif row[1] != "NOT EXCEPTION" and row[4] == 0:
    #                                     #not marked in the topology or incorrectly marked in the road centerline
    #                                     msg = "Either marked incorrectly in the road centerline or needs to be marked as an exception in the topology"
    #                             else:
    #                                 #note other exceptions in FieldValuesCheckResults table, access the real SEGID (just roads)
    #                                 msg = "Feature has topology error: " + row[3]
    #
    #                             #if an error was generated, add it to the error list
    #                             if msg != "":
    #                                 val = (today, msg, filename, "", segID, "VerifyTopology")
    #                                 values.append(val)
    #
    #                 except:
    #                     userMessage("Error attempting topology validation.")
    #
    #             Delete_management(e)
    #             del e
    #
    #         #report records
    #         count = 0
    #         if values != []:
    #             count = len(values)
    #             RecordResults(recordType, values, gdb)
    #
    #         #clean up & reset
    #         if rd_did_have_join:
    #             RemoveJoin_management(rd)
    #
    #         #give the user some feedback
    #         message = "Topology check complete. " + str(count) + " issues found."
    #         if count > 0:
    #             message = message + " Results in FieldValuesCheckResults."
    #         userMessage(message)
    #
    #     finally:
    #         #clean up topology export if desired by the user
    #         # Inside finally block so as to clean up as necessary even if something in the try block fails
    #         if cleanUpTopology == "true":
    #             polyErrors = out_basename + "_poly"
    #             for topE in (lineErrors, pointErrors, polyErrors):
    #                 full = join(gdb, topE)
    #                 if Exists(full):
    #                     Delete_management(full)
    # else:
    #     userMessage("Road Centerline does not have an exception field. Cannot check topology.")

if __name__ == '__main__':
    main()