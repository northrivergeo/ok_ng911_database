#-------------------------------------------------------------------------------
# Name: NG911_DataCheck
# Purpose: Collection of functions to check submitted NG911 data
#
# Author: Kristen Jordan Koenig, Kansas Data Access and Support Center, kristen@kgs.ku.edu
# Author: Emma Baker, Riley Baird, Oklahoma DOT GIS, ebaker@odot.org
#
# Created: 19/09/2014
# Modified: January 6, 2022
#-------------------------------------------------------------------------------

from arcpy import (AddField_management, CalculateField_management, CopyRows_management, Statistics_analysis,
                   CreateTable_management, Delete_management, Exists,
                   ListFields, MakeFeatureLayer_management, MakeTableView_management, SelectLayerByAttribute_management,
                   SelectLayerByLocation_management, env, ListDatasets,
                   AddJoin_management, RemoveJoin_management, CopyFeatures_management,
                   Dissolve_management, DeleteField_management, DisableEditorTracking_management, EnableEditorTracking_management,
                   ExportTopologyErrors_management, Buffer_analysis, Intersect_analysis, Point, SetProgressor, SetProgressorPosition,
                   ResetProgressor, SetProgressorLabel, Identity_analysis, Describe, FeatureClassToFeatureClass_conversion)
from arcpy.da import InsertCursor, SearchCursor, UpdateCursor, Editor
from os import path, remove
from os.path import basename, dirname, join, exists
from time import strftime
from collections import Counter

from NG911_GDB_Objects import NG911_Session_obj, __NG911_GDB_Object
from Validation_ClearOldResults import ClearOldResults
from Enhancement_AddTopology import add_topology
import NG911_GDB_Objects
from NG911_arcpy_shortcuts import deleteExisting, getFastCount, cleanUp, ListFieldNames, fieldExists, writeToText, delete_field_if_exists
from NG911_User_Messages import *
from MSAG_DBComparison import prep_roads_for_comparison
import arcpy, numpy

try:
    from typing import Union, List, Tuple, Dict, Set, Optional
except:
    pass


#import time
#from math import sin, cos, atan2, sqrt, asin, pi

def checkToolboxVersion():
    import json, urllib, sys
    from inspect import getsourcefile
    from os.path import abspath

    v = sys.version_info.major
    if v != 2:
        if exists(r"C:\Program Files\ArcGIS\Pro\bin\Python\Lib\urllib"):
            sys.path.append(r"C:\Program Files\ArcGIS\Pro\bin\Python\Lib\urllib")
            import urllib.request

#   set lots of variables
    message, toolData, toolVersion, response, mostRecentVersion = "", "", "0", "", "X"

#    get version in the .json file that is already present
    me_folder = dirname(abspath(getsourcefile(lambda:0)))
    jsonFile = join(me_folder, "ToolboxVersion.json")

#   make sure the local json file exists
    if exists(jsonFile):
        toolData = json.loads(open(jsonFile).read())
        toolVersion = toolData["toolboxVersion"]["version"]
        userMessage("You are using toolbox version: " + toolVersion)

#   get version of toolbox live online
    url = "https://raw.githubusercontent.com/kansasgis/NG911/master/Scripts/ToolboxVersion.json"

#   Error trapping in case the computer is offline or can't get to the internet
    try:

        try:
            response = urllib.request.urlopen(url).read()
            mostRecentData = json.loads(response.decode('utf-8'))
        except Exception as e:
##            userMessage(str(e))
            response = urllib.urlopen(url)
            mostRecentData = json.loads(response.read())

        mostRecentVersion = mostRecentData["toolboxVersion"]["version"]
        userMessage("Most current toolbox version: " + mostRecentVersion)
    except Exception as e:
        userMessage(str(e))
        message = "Unable to check toolbox version at this time."

#    compare the two
    if toolVersion == mostRecentVersion:
        message = "Your NG911 toolbox version is up-to-date."
    else:
        if mostRecentVersion != "X":
            message = """Your version of the NG911 toolbox is not the most recent version available.
            Your results might be different than results received upon data submission. Please
            download an up-to-date copy of the toolbox at
            https://github.com/kansasgis/NG911/raw/master/KansasNG911GISTools.zip"""

#   report back to the user
    return message


def getAddFieldInfo(table):
    # type: (str) -> List[Tuple]
    """

    Parameters
    ----------
    table : str
        Table fullpath to TemplateCheckResults, FieldValuesCheckResults, or DASC_Communication

    Returns
    -------
    list of tuple
        List of the fieldInfo tuples in order: path, fieldname, type, "", "", length

    """
    obj = NG911_GDB_Objects.getFCObject(table)

    lyr = basename(table)
    #field info
    if lyr == "TemplateCheckResults":
        fieldInfo = [(table, obj.DATEFLAGGED, "DATE", "", "", ""),(table, obj.DESCRIPTION, "TEXT", "", "", 250),(table, obj.CATEGORY, "TEXT", "", "", 25),
        (table, obj.CHECK, "TEXT", "", "", 40)]
    elif lyr == "FieldValuesCheckResults":
        fieldInfo = [(table, obj.DATEFLAGGED, "DATE", "", "", ""),(table, obj.DESCRIPTION, "TEXT", "", "", 250),
            (table, obj.LAYER, "TEXT", "", "", 50),(table, obj.FIELD, "TEXT", "", "", 25),(table, obj.FEATUREID, "TEXT", "", "", 254),
            (table, obj.CHECK, "TEXT", "", "", 40)]
    elif lyr == "DASC_Communication":
        fieldInfo = [(table, "NoteDate", "DATE", "", "", ""),(table, "Description", "TEXT", "", "", 250)]
        userWarning("CODING ERROR: CREATING DASC TABLE!")

    del lyr
    return fieldInfo

# Revised getAddFieldInfo function work from text-file-derived dict
# def getAddFieldInfo(table):
#     # type: (str) -> List[Tuple]
#     '''
#
#     Parameters
#     ----------
#     table : str
#         Table fullpath to TemplateCheckResults, FieldValuesCheckResults, or DASC_Communication
#
#     Returns
#     -------
#     list of tuple
#         List of the fieldInfo tuples in order: path, fieldname, type, "", "", length
#
#     '''
#     # TODO: Migrate this field information to a text file, create fields class object path
#     obj = NG911_GDB_Objects.getFCObject(table)
#     fieldDict = getTableFieldInfo(table)
#
#     for fieldName in fieldDict:
#         lyr = basename(table)
#         #field info
#         if lyr == "TemplateCheckResults":
#             fieldInfo = [(table, obj.DATEFLAGGED, "DATE", "", "", ""),(table, obj.DESCRIPTION, "TEXT", "", "", 250),(table, obj.CATEGORY, "TEXT", "", "", 25),
#             (table, obj.CHECK, "TEXT", "", "", 40)]
#         elif lyr == "FieldValuesCheckResults":
#             fieldInfo = [(table, obj.DATEFLAGGED, "DATE", "", "", ""),(table, obj.DESCRIPTION, "TEXT", "", "", 250),
#                 (table, obj.LAYER, "TEXT", "", "", 25),(table, obj.FIELD, "TEXT", "", "", 25),(table, obj.FEATUREID, "TEXT", "", "", 254),
#                 (table, obj.CHECK, "TEXT", "", "", 40)]
#         elif lyr == "DASC_Communication":
#             fieldInfo = [(table, "NoteDate", "DATE", "", "", ""),(table, "Description", "TEXT", "", "", 250)]
#
#     del lyr
#     return fieldInfo


def getResultsFieldList(table):
    #get field info
    fieldInfo = getAddFieldInfo(table)
    fieldList = []
    #loop through added fields
    for fi in fieldInfo:
        #append the field name
        fieldList.append(fi[1])

    return fieldList


def calcAngle(pt1, pt2, pt3):
    import math, decimal
    context = decimal.Context(prec=5, rounding="ROUND_DOWN")
    #get length of side A
    a = abs(abs(pt1[0]) - abs(pt2[0]))
    b = abs(abs(pt1[1]) - abs(pt2[1]))
    A = context.create_decimal_from_float(math.hypot(a,b))

    #get length of side B
    c = abs(abs(pt2[0]) - abs(pt3[0]))
    d = abs(abs(pt2[1]) - abs(pt3[1]))
    B = context.create_decimal_from_float(math.hypot(c,d))

    #get length of side C
    e = abs(abs(pt3[0]) - abs(pt1[0]))
    f = abs(abs(pt3[1]) - abs(pt1[1]))
    C = context.create_decimal_from_float(math.hypot(e,f))

    q = ((A*A) + (B*B) - (C*C))/(2*A*B)

    degrees = 0

    if -1 < q < 1:
        #get angle
        radian = math.acos(q)

##    radian = math.atan((pt3x - pt2x)/(pt1y - pt2y))
        degrees = radian * 180 / math.pi
    return degrees


def RecordResults(resultType, values, gdb): # Guessed on whitespace formatting here. -- DT
    # type: (str, List[Tuple], str) -> None
    if resultType == "template":
        tbl = "TemplateCheckResults"
    elif resultType == "fieldValues":
        tbl = "FieldValuesCheckResults"
    elif resultType == "DASCmessage":
        tbl = "DASC_Communication"
        userWarning("CODING ERROR: CREATING DASC TABLE!")

    table = join(gdb, tbl)
    fieldList = []

    if not Exists(table):
        CreateTable_management(gdb, tbl)

    fieldInfo = getAddFieldInfo(table)  # type: List[Tuple]

    for fi in fieldInfo:
        if not fieldExists(table, fi[1]):
        #add field with desired parameters if it doesn't already exist
            AddField_management(fi[0],fi[1],fi[2],fi[3],fi[4],fi[5])

    fieldList = getResultsFieldList(table)

    cursor = InsertCursor(table, fieldList)
    required_len_of_row = len(fieldInfo)  # Number of fields that should be in each row
    for row in values:
        if len(row) != required_len_of_row:
            raise Exception('''
            
            ========== SCRIPT ERROR: CONTACT DEVELOPERS ==========
            
            Email script developers with subject line "RecordResults Error".
            Please copy the text in this window and paste into the email.
            
            ''')
        # try:
        #     cursor.insertRow(row)
        cursor.insertRow(row)
        # except Exception as e:
        #     raise e
        #     userMessage(str(row))
    del cursor


def getParityReport(phrase):
    report = ""

    # create report based on what needs to be addressed
    if phrase[1:] == "00":
        report = "Address range is 0-0, but the parity is recorded as %s instead of Z" % (phrase[0])
    elif phrase[0] == "Z":
        report = "Parity is Z (zero), but the address range is filled in with non-zero numbers."
    elif phrase[0] in "EO" and phrase[1:] != "00":
        report = "Parity is marked as %s but the ranges filled in are %s and %s" % (phrase[0], phrase[1], phrase[2])

    if report == "":
        import random
        attack = random.choice(["Crevice", "Iron Maiden", "Antler Auger", "Absolute Chill"])
        report = "A wild error appeared! The wild error used %s! It's a one-hit KO! (%s)" % (attack, phrase)
    return report


def checkParities(currentPathSettings):
    # parity "E' must have even ranges
    # parity "O" must have odd ranges
    # Parity "Z" must have 00 ranges
    # ranges that are 00 must have "Z" marked as the parity

    # set variables
    gdb = currentPathSettings.gdbPath
    roads = currentPathSettings.gdbObject.RoadCenterline
    rc_obj = NG911_GDB_Objects.getFCObject(roads)

    fields = [rc_obj.UNIQUEID, rc_obj.PARITY_R, rc_obj.PARITY_L, rc_obj.Add_R_From, rc_obj.Add_R_To, rc_obj.Add_L_From, rc_obj.Add_L_To]
    # version = rc_obj.GDB_VERSION
    # if version == "21":

    values = []
    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")
    filename = "ROAD_CENTERLINE"  # Changed to OK Fields/Layer
    check = "Check Parity"

    # these combinations are acceptable and will be used for comparisons
    # "Parity-From-To"
    a_phrase = ["EEE", "OOO", "Z00", "BOE", "BEO", "BEE", "BOO", "B0O", "B0E"]

    # make sure we're only checking roads for submission
    wc = "SUBMIT = 'Y'"
    rds = "rds"
    MakeFeatureLayer_management(roads, rds, wc)

    # run a search cursor on the road layer
    with SearchCursor(rds, fields) as rows:
        for row in rows:
            if None not in [type(row[3]), type(row[4]), type(row[5]), type(row[6])]:

                # create a dictionary that will hold even/odd/zero status of r/l/to/from numbers
                pDict = {}
                starter = 3

                # loop through all r/l/to/from address numbers to get their even/odd/zero status
                while starter < 7:
                    if row[starter] is not None:
                        if row[starter] == 0:
                            eo = "0"
                        else:
                            if (row[starter] % 2 == 0):
                                eo = "E"
                            else:
                                eo = "O"

                        pDict[str(starter)] = eo
                    else:
                        userWarning("You have one or more parities set as null. Please populate those fields.")
                    starter += 1

                # create a phrase for each side of the road
                try:
                    r_phrase = row[1] + pDict["3"] + pDict["4"]

                    l_phrase = row[2] + pDict["5"] + pDict["6"]

                    # compare the road side phrases with the phrases that are acceptable
                    # report road segments that don't match up correctly
                    if r_phrase not in a_phrase:
                        r_report = getParityReport(r_phrase)
                        val = (today, "Notice: R Side- " + r_report, filename, "", row[0], check)
                        values.append(val)
                    if l_phrase not in a_phrase:
                        l_report = getParityReport(l_phrase)
                        val = (today, "Notice: L Side- " + l_report, filename, "", row[0], check)
                        values.append(val)
                except Exception as e:
                    if type(row[0]) is not None:
                        # userWarning("Could not process parity check for road segment " + row[0] + ". Please check address ranges and parities for null values.")
                        val = (today, "Error: Could not process parity check. Look for null values.", filename, "", row[0], check)
                        values.append(val)
                    else:
                        val = (today, "Error: Could not process parity check for a road segment with a null unique ID.", filename, "", "", check)
                        values.append(val)
                        # userWarning("Could not process parity check for a road segment. Please check address ranges and parities for null values.")
            else:
                if type(row[0]) is not None:
                    val = (today, "Error: One or more address ranges are null", filename, "", row[0], check)
                    values.append(val)

    # report records
    if values != []:
        RecordResults(recordType, values, gdb)
        userWarning("Completed parity check. There were %s issues. Results are in table FieldValuesCheckResults." % (str(len(values))))
    else:
        userMessage("Completed parity check. No issues found.")

def checkRoadESNOK(currentPathSettings):
    userMessage("Checking road ESN values...")
    gdb = currentPathSettings.gdbPath
    esz = currentPathSettings.gdbObject.ESZ
    rc = currentPathSettings.gdbObject.RoadCenterline

    esz_obj = NG911_GDB_Objects.getFCObject(esz)
    rc_obj = NG911_GDB_Objects.getFCObject(rc)

    # FEATURE LAYER from RCL where submit is Y
    # FEATURE LAYER from ESZ where submit is Y
    if Exists(rc) and Exists(esz):
        #set variables
        values = []
        recordType = "fieldValues"
        side_phrase = ""
        today = strftime("%Y/%m/%d")
        filename = "ROAD_CENTERLINE"  # Changed to OK Fields/Layer
        wc_road = rc_obj.SUBMIT + " = 'Y'"
        wc_esz = esz_obj.SUBMIT + " = 'Y'"

        road_submit_layer = "road_submit_layer"
        deleteExisting(road_submit_layer)
        MakeFeatureLayer_management(rc, road_submit_layer, wc_road)
        esz_submit_layer = "esz_submit_layer"
        deleteExisting(esz_submit_layer)
        MakeFeatureLayer_management(esz, esz_submit_layer, wc_esz)

        # IDENTITY tool on RCL FL & ESZ FL
        identity_output = join("in_memory", "identity_output")
        deleteExisting(identity_output)
        Identity_analysis(road_submit_layer, esz_submit_layer, identity_output, relationship=True)

        # FEATURE LAYER from identity output where tabular ESN does not equal geometric ESN
        wc_identity = "%s <> LEFT_%s OR %s <> RIGHT_%s" % (rc_obj.ESN_L, esz_obj.ESN, rc_obj.ESN_R, esz_obj.ESN)
        mismatch_layer = "mismatch_layer"
        deleteExisting(mismatch_layer)
        MakeFeatureLayer_management(identity_output, mismatch_layer, wc_identity)
        # SET of unique NGUID_RDCLs from Identity FL - These are *potential* problem features (all possible problem features)
        unique_rdcls = set()  # type: Set[unicode]
        with SearchCursor(mismatch_layer, rc_obj.UNIQUEID) as mismatch_cursor:
            for row in mismatch_cursor:
                unique_rdcls.add(unicode(row[0]))

        # FEATURE LAYER of RCL FL with NGUID_RDCLs from unique set
        wc_unique = ",".join(["'%s'" % val for val in unique_rdcls])
        wc_ids = "%s IN (%s)" % (rc_obj.UNIQUEID, wc_unique)  # queries road centerlines with any of the unique ids from the identity feature layer
        potential_problems_layer = "potential_problems_layer"
        deleteExisting(potential_problems_layer)
        MakeFeatureLayer_management(road_submit_layer, potential_problems_layer, wc_ids)  # FL of road centerlines where SUBMIT is Y and tabular ESN != geometric ESN

        # BUFFER LEFT uniques FL
        buffer_left_fc = join("in_memory", "buffer_left_fc")
        deleteExisting(buffer_left_fc)
        Buffer_analysis(potential_problems_layer, buffer_left_fc, "30 feet", "LEFT", "FLAT")
        # BUFFER RIGHT uniques FL
        buffer_right_fc = join("in_memory", "buffer_right_fc")
        deleteExisting(buffer_right_fc)
        Buffer_analysis(potential_problems_layer, buffer_right_fc, "30 feet", "RIGHT", "FLAT")

        # Blank SETs (left and right) for correct/matching NGUID_RDCLs (left matches and right matches)
        match_left = set()  # type: Set[unicode]
        match_right = set()  # type: Set[unicode]

        # SEARCHCURSOR from buffer left of NGUID_RDCL and Esn_L - FOR EACH buffer:
        with SearchCursor(buffer_left_fc, ["SHAPE@", rc_obj.UNIQUEID, rc_obj.ESN_L]) as buffer_cursor:
            with SearchCursor(esz_submit_layer, ["SHAPE@", esz_obj.UNIQUEID, esz_obj.ESN]) as esz_left_cursor:
                for buffer_row in buffer_cursor:
                    buffer_geometry = buffer_row[0]
                    esz_left_cursor.reset()  # Reset the ESZ cursor to the beginning
                    for esz_row in esz_left_cursor:
                        esz_geometry = esz_row[0]
                        if buffer_geometry.overlaps(esz_geometry):
                            # Could this be the ESZ feature?
                            if buffer_row[2] == esz_row[2]:
                                # Match!
                                match_left.add(buffer_row[1])
                                break

        with SearchCursor(buffer_right_fc, ["SHAPE@", rc_obj.UNIQUEID, rc_obj.ESN_R]) as buffer_cursor:
            with SearchCursor(esz_submit_layer, ["SHAPE@", esz_obj.UNIQUEID, esz_obj.ESN]) as esz_right_cursor:
                for buffer_row in buffer_cursor:
                    buffer_geometry = buffer_row[0]
                    esz_right_cursor.reset()  # Reset the ESZ cursor to the beginning
                    for esz_row in esz_right_cursor:
                        esz_geometry = esz_row[0]
                        if buffer_geometry.overlaps(esz_geometry):
                            # Could this be the ESZ feature?
                            if buffer_row[2] == esz_row[2]:
                                # Match!
                                match_right.add(buffer_row[1])
                                break

        both_matches = match_left & match_right  # (set intersect)
        problem_nguids = unique_rdcls - both_matches  # Mismatches on one or both sides
        mismatch_left = problem_nguids - match_left
        mismatch_right = problem_nguids - match_right
        mismatch_both = mismatch_left & mismatch_right

        if len(problem_nguids) > 0:
            for nguid in problem_nguids:
                if nguid in mismatch_both:
                    side_phrase = "%s|%s" % (rc_obj.ESN_L, rc_obj.ESN_R)
                    report = ("Notice: %s and %s of road segment %s may not be correct." % (rc_obj.ESN_L, rc_obj.ESN_R, nguid))
                elif nguid in mismatch_left:
                    side_phrase = rc_obj.ESN_L
                    report = ("Notice: %s of road segment %s may not be correct." % (rc_obj.ESN_L, nguid))
                elif nguid in mismatch_right:
                    side_phrase = rc_obj.ESN_R
                    report = ("Notice: %s of road segment %s may not be correct." % (rc_obj.ESN_R, nguid))
                else:
                    continue
                val = (today, report, filename, side_phrase, nguid, "Check Road ESN Values")
                values.append(val)

        if values != []:
            RecordResults(recordType, values, gdb)
            userWarning("Completed road ESN check (Advanced license version). There were %s issues. Results are in table FieldValuesCheckResults" % (str(len(values))))
        else:
            userMessage("Completed road ESN check (Advanced license version). No issues found.")


def checkRoadESN(currentPathSettings):
    userMessage("Checking road ESN values...")
    gdb = currentPathSettings.gdbPath
    esz = currentPathSettings.gdbObject.ESZ
    rc = currentPathSettings.gdbObject.RoadCenterline

    esz_obj = NG911_GDB_Objects.getFCObject(esz)
    rc_obj = NG911_GDB_Objects.getFCObject(rc)

    if Exists(rc) and Exists(esz):
        #set variables
        values = []
        recordType = "fieldValues"
        side_phrase = ""
        today = strftime("%Y/%m/%d")
        filename = "ROAD_CENTERLINE"  # Changed to OK Fields/Layer
        wc_submit = rc_obj.SUBMIT + " = 'Y'"

        # define ESZ fields to examine
        esz_fields = (esz_obj.UNIQUEID, esz_obj.ESN, "SHAPE@XY")

        # define road fields to examine
        # road_fields = [rc_obj.UNIQUEID, rc_obj.ESN_R, rc_obj.ESN_L, "OBJECTID", rc_obj.AUTH_L, rc_obj.AUTH_R, "SHAPE@", "SHAPE@XY"]
        road_fields = [rc_obj.UNIQUEID, rc_obj.ESN_R, rc_obj.ESN_L, "OBJECTID", "SHAPE@", "SHAPE@XY"]

        # make feature layer from roads
        rd_lyr = "rd_lyr"
        MakeFeatureLayer_management(rc, rd_lyr, wc_submit)

        # make feature layer from ESZ
        esz_lyr = "esz_lyr"
        MakeFeatureLayer_management(esz, esz_lyr, wc_submit)

        if Exists(rc) and Exists(esz):
            #set variables
            values = []
            recordType = "fieldValues"
            today = strftime("%Y/%m/%d")
            filename = "ROAD_CENTERLINE" # Changed to OK Fields/Layer
            wc_submit = rc_obj.SUBMIT + " = 'Y'"

            # go through esz by esz
            with SearchCursor(esz_lyr, esz_fields, wc_submit) as rows: # esz_obj.UNIQUEID, esz_obj.ESN, "SHAPE@XY"
                for row in rows:
                    # get ESZ variables & make a where clause
                    wc_esz = esz_obj.UNIQUEID + " = '" + row[0] + "' AND " + wc_submit

                    # single out this ESZ with a feature layer
                    eszf = "eszf"
                    MakeFeatureLayer_management(esz_lyr, eszf, wc_esz)

                    # select road features inside the current esz feature
                    SelectLayerByLocation_management(rd_lyr, "HAVE_THEIR_CENTER_IN", eszf)

                    # loop through the selected road features
                    with SearchCursor(rd_lyr, road_fields) as r_rows: # rc_obj.UNIQUEID, rc_obj.ESN_R, rc_obj.ESN_L, "OBJECTID", "SHAPE@", "SHAPE@XY"
                        for r_row in r_rows:

                            # get the road variables
                            segid = r_row[0]
                            esn_r = r_row[1]
                            esn_l = r_row[2]
                            # auth_l = r_row[4]
                            # auth_r = r_row[5]
##                            print("%s: Right side- %s, %s Left side- %s %s" % (segid, esn_r, auth_r, esn_l, auth_l))

                            # see if the sides really don't match and one side isn't 0
                            if esn_r != esn_l and esn_r != '0' and esn_l != '0':
                                esn_list = [esn_l, esn_r]

                                # get A & B points of the road segment
                                # A = r_row[6].firstPoint
                                A = r_row[4].firstPoint
                                # B = r_row[6].lastPoint
                                B = r_row[4].lastPoint

                                # make a feature layer of the road
                                road_wc = rc_obj.UNIQUEID + " = '" + segid + "'"
                                rd_buff_lyr = "rd_buff_lyr"
                                MakeFeatureLayer_management(rd_lyr, rd_buff_lyr, road_wc)

                                # make a second feature layer from ESZ
                                esz_lyr_select = "esz_lyr_select"
                                MakeFeatureLayer_management(esz_lyr, esz_lyr_select)

                                # select which ESZ zones are close
                                SelectLayerByLocation_management(esz_lyr_select, "INTERSECT", rd_buff_lyr)

                                esz_esn_list = [] # Intersect Score

                                # see which eszs intersect the road segment
                                with SearchCursor(esz_lyr_select, (esz_obj.ESN)) as ez_rows:
                                    for ez_row in ez_rows:
                                        # put the intersecting esns in a list
                                        esz_esn_list.append(ez_row[0])

                                # clean up esz selection layer
                                Delete_management(esz_lyr_select)

                                # set up scoring system
                                esn_score = 0 # number of ESZs that our particular Road Segment intersects with
                                l_score = 0
                                r_score = 0

                                # loop through the intersecting esz list, add points to the score
                                for ez_esn in esz_esn_list:
                                    if ez_esn in esn_list:
                                        esn_score += 1

                                # max esn_score here is 2

                                # create buffer of the line segment
                                temp_buffer = join("in_memory", "temp_buffer")
                                if Exists(temp_buffer):
                                    Delete_management(temp_buffer)

                                # buffer the particular road segment
                                Buffer_analysis(rd_buff_lyr, temp_buffer, "30 feet")

                                # intersect road buffer and esz boundaries
                                temp_buffer_intersect = join("in_memory", "temp_buffer_intersect")
                                if Exists(temp_buffer_intersect):
                                    Delete_management(temp_buffer_intersect)

                                Intersect_analysis([temp_buffer, esz], temp_buffer_intersect)

                                # run a search cursor on the intersection, weed out areas less than area 500
                                intersect_fields = [esz_obj.ESN, "SHAPE@TRUECENTROID", "SHAPE@AREA", "SHAPE@"]

                                esz_count = 0

                                with SearchCursor(temp_buffer_intersect, intersect_fields) as i_rows: # esz_obj.ESN, "SHAPE@TRUECENTROID", "SHAPE@AREA", "SHAPE@"
                                    for i_row in i_rows:

                                        if True:#i_row[2] > 1500.0:
                                            esz_count += 1

                                            # get esn value
                                            esn_value_buff = i_row[0]

                                            # add points to the esn score if the esn is in the esn list
                                            if esn_value_buff in esn_list:
                                                esn_score += 1

                                            # perfect score here is 4+

                                            # get the centroid of that particular feature
                                            p_list = list(i_row[1])
                                            P = Point(p_list[0], p_list[1])

                                            # see if it's on the left or right
                                            # see what side of the road the esz is on
                                            direction = directionOfPoint(A, B, P)
                                            # debugMessage("Direction: %s\nESN Value Buff: %s" % (direction, esn_value_buff))
                                            side_phrase = "ESN_" + direction

                                            # set variables based on that side of the road
                                            if direction == "R":
                                                # run a quick check
                                                if esn_value_buff == esn_r:
                                                    r_score += 1
                                            elif direction == "L":
                                                # run a quick check
                                                if esn_value_buff == esn_l:
                                                    l_score += 1

                                            esn_value_buff = ""

                                # work on generating proper reporting
                                reportStatus = False

                                # check scores
                                if esn_score == 0: # nothing matches
                                    reportStatus = True
                                    report = 'Notice: Segment ESN values %s and %s do not match ESNs of physical locations' % (esn_l, esn_r)
                                elif esn_score > 0 and esn_score <= 2:
                                    reportStatus = True
                                    if l_score == 0: # problem is maybe with the left side
                                        if r_score > 1: # problem might be on the right side actually
                                            report = 'Notice: One or both segment values does not match ESN of physical location'
                                        else:
                                            report = 'Notice: Segment ESN_L value %s does not match ESN of physical location' % (esn_l)
                                    elif r_score == 0: # problem is maybe with the right side
                                        if l_score > 1: # problem might be on the left side actually
                                            report = 'Notice: One or both segment values does not match ESN of physical location'
                                        else:
                                            report = 'Notice: Segment ESN_R value %s does not match ESN of physical location' % (esn_r)

                                    if l_score == 0 and r_score == 0:
                                        if esz_count > 1:
                                            report = 'Notice: Segment ESN values %s and %s may not match ESNs of physical locations' % (esn_l, esn_r)
                                        elif esz_count == 1:
                                            report = 'Notice: One or both segment values does not match ESN of physical location'
                                elif esn_score > 2:
                                    pass
                                    # this means things are probably fine

                                if reportStatus == True:
                                    val = (today, report, filename, side_phrase, segid, "Check Road ESN Values")
                                    values.append(val)

                                # clean up
                                Delete_management(rd_buff_lyr)
                                Delete_management(temp_buffer)
                                Delete_management(temp_buffer_intersect)

                            else:
                                esn_value = row[1]

                                # set issues to false to start with
                                L_issue = False
                                R_issue = False

                                # evaluate left side of the road considering authority
                                # the value is zero, skip it
                                # if auth_l == 'Y' and str(esn_l) != "0" and esn_value != esn_l:
                                if str(esn_l) != "0" and esn_value != esn_l:
                                    L_issue = True

                                # evaluate right side of the road considering authority
                                # the value is zero, skip it
                                # if auth_r == 'Y' and str(esn_r) != "0" and esn_value != esn_r:
                                if str(esn_r) != "0" and esn_value != esn_r:
                                    R_issue = True

                                # see which sides need to be reported (probably both)
                                sides = []

                                if L_issue == True:
                                    sides.append(rc_obj.ESN_L)
                                    esn_side = esn_l
                                if R_issue == True:
                                    sides.append(rc_obj.ESN_R)
                                    esn_side = esn_r

                                # report any issues that exist
                                if sides != []:
                                    side_phrase = "| ".join(sides)

                                    report = 'Notice: Segment %s value %s does not match ESN of physical location %s' % (side_phrase, esn_side, esn_value)
                                    val = (today, report, filename, side_phrase, segid, "Check Road ESN Values")
                                    values.append(val)

                                esn_side, esn_value, esn_l, esn_r, side_phrase = "", "", "", "", ""

                    # clean up feature class to repeat
                    Delete_management(eszf)

                del row, rows

        # clean up in memory esz
        Delete_management(esz_lyr)
        Delete_management(rd_lyr)

        #report records
        if values != []:
            RecordResults(recordType, values, gdb)
            userWarning("Completed road ESN check. There were %s issues. Results are in table FieldValuesCheckResults" % (str(len(values))))
        else:
            userMessage("Completed road ESN check. No issues found.")


def directionOfPoint(A, B, P):
    # code translated from https://www.geeksforgeeks.org/direction-point-line-segment/
    # subtracting co-ordinates of point A from
    # B and P, to make A as origin

    B.X -= A.X
    B.Y -= A.Y
    P.X -= A.X
    P.Y -= A.Y

    # Determining cross Product
    cross_product = B.X * P.Y - B.Y * P.X;

##    print(str(cross_product))

    # return RIGHT if cross product is positive
    if cross_product > 0:
        direction = "L"

    # return LEFT if cross product is negative
    elif cross_product < 0:
        direction = "R"

    # else, return zero
    else:
        direction = "Z"

    # return ZERO if cross product is zero.
    return direction


def checkDirectionality(fc, gdb):
    """
    Checks to see if a road segment's address range goes from low to high, rather than high to low. A notice is
    generated if the address ranges go from high to low.

    Parameters
    ----------
    fc : str
        Full path to road centerline feature class
    gdb : str
        Full path to the geodatabase
    """
    userMessage("Checking road directionality...")
    rc_obj = NG911_GDB_Objects.getFCObject(fc)

    if Exists(fc):
        #set variables
        values = []
        recordType = "fieldValues"
        today = strftime("%Y/%m/%d")
        filename = "ROAD_CENTERLINE" # Changed to OK Fields/Layer
        report = "Notice: Segment's address range is from high to low instead of low to high"

        fields = ["SHAPE@", rc_obj.UNIQUEID, rc_obj.Add_L_From, rc_obj.Add_L_To, rc_obj.Add_R_From, rc_obj.Add_R_To]

        # version = rc_obj.GDB_VERSION
        # if version == "21":

        lyr400 = "lyr400"

        #only check roads marked for submission
        MakeFeatureLayer_management(fc, lyr400, rc_obj.SUBMIT + "  = 'Y'")

        with SearchCursor(lyr400, fields) as rows:
            for row in rows:
                # checkR, checkL = "Y", "Y"
                # if version == "21":

                #get unique id and from/to values
                segid = row[1]
                addyList = [row[2],row[3],row[4],row[5]]

                #make sure it's not a blank road
                if addyList != [0,0,0,0]:

                    #set up values
                    lFrom = addyList[0]
                    lTo = addyList[1]
                    rFrom = addyList[2]
                    rTo = addyList[3]

                    check = "both"
                    issue = False

                    #see if we're working with any 0's
                    if lFrom == 0 or lTo == 0:
                        check = "right"
                    elif rFrom ==0 or rTo == 0:
                        check = "left"

                    #see if any road values don't follow low to high pattern
                    if check == "both":
                        if rTo < rFrom or lTo < lFrom:
                            issue = True
                    elif check == "right":
                        if rTo < rFrom:
                            issue = True
                    elif check == "left":
                        if lTo < lFrom:
                            issue = True

                    if issue == True:
                        val = (today, report, filename, "", segid, "Check Directionality")
                        values.append(val)

        Delete_management(lyr400)

    else:
        userWarning(fc + " does not exist")

    #report records
    if values != []:
        RecordResults(recordType, values, gdb)
        userWarning("Completed road directionality check. There were %s issues. Results are in table FieldValuesCheckResults." % (str(len(values))))
    else:
        userMessage("Completed road directionality check. No issues found.")

def checkESNandMuniAttribute(currentPathSettings):
    # type: (NG911_Session_obj) -> None
    """
    Called as part of the Check Address Points (Validation) tool.

    Parameters
    ----------
    currentPathSettings : NG911_Session_obj


    Returns
    -------

    """
    userMessage("Checking Address Point ESN/Municipality attributes...")

    gdb = currentPathSettings.gdbPath
    esz = currentPathSettings.gdbObject.ESZ
    address_points = currentPathSettings.gdbObject.AddressPoints
    muni = currentPathSettings.gdbObject.MunicipalBoundary

    esz_obj = NG911_GDB_Objects.getFCObject(esz)  # type: NG911_GDB_Objects.NG911_ESZ_Object
    mb_obj = NG911_GDB_Objects.getFCObject(muni)  # type: NG911_GDB_Objects.NG911_MunicipalBoundary_Object
    a_obj = NG911_GDB_Objects.getFCObject(address_points)  # type: NG911_GDB_Objects.NG911_Address_Object

    values = []
    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")
    filename = "ADDRESS_POINT" # Changed to OK Fields/Layer

    try:

        if Exists(address_points):

            # Make temporary layer of address points
            addy_lyr = "addy_lyr"
            wc = "%s = 'Y'" % a_obj.SUBMIT
            MakeFeatureLayer_management(address_points, addy_lyr, wc)

            # Makes dict of { fc path : ( fc-specific field, "UNIQUEID" field, address-point field) }
            searchDict = {esz: (esz_obj.ESN, esz_obj.UNIQUEID, a_obj.ESN), muni: (mb_obj.MUNI, mb_obj.UNIQUEID, a_obj.MUNI)}  # type: Dict[str, Tuple[str, str, str]]
            # OK fields equiv.:
            # {
            #     "[...].gdb/ESZ_Boundary":
            #         ("ESN", "NGUID_ESZ"),
            #     "[...].gdb/Municipal_Boundary":
            #         ("NAME", "NGUID_MUNI")
            # }

            for layer in searchDict.keys():
                # OK: searchDict.keys() -> full paths to "ESZ_Boundary" and "Address_Point" FCs
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # TODO: QUESTION - Is it AP, or is it actually muni boundary?
                # NOTE: Wrote Error Glossary assuming muni boundary -Baird 05/31/2022
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                fieldList = searchDict[layer]  # type: Tuple[str, str, str]
                if Exists(layer):

                    if "ESZ" in basename(layer):
                        wc = "%s = 'Y'" % esz_obj.SUBMIT
                    elif "MUNI" in basename(layer):
                        wc = "%s = 'Y'" % mb_obj.SUBMIT
                    else:
                        wc = None

                    with SearchCursor(layer, fieldList[0:2], wc) as polys:
                        for poly in polys:
                            feature = fieldList[0]  # type: str # Name of fc-specific field
                            ap_field_name = fieldList[2] # type: str # Name of the ap-specific field
                            feature_value = poly[0]  # type: str # Value of that field for particular feature

                            #make feature layer
                            lyr1 = "lyr1"
##                            qry = fieldList[1] + " = '" + str(poly[1]) + "'"
                            qryList = [fieldList[1], " = '", unicode(poly[1]), "'"]
                            qry = "".join(qryList)
                            # Create a feature layer consisting of one particular polygon
                            MakeFeatureLayer_management(layer, lyr1, qry)

                            #select by location
                            # Get all address points inside this particular polygon (in the feature layer created above)
                            SelectLayerByLocation_management(addy_lyr, "INTERSECT", lyr1)

                            #loop through address points
                            # with SearchCursor(addy_lyr, (feature, a_obj.UNIQUEID, "OBJECTID")) as address_point_rows:
                            with SearchCursor(addy_lyr, (ap_field_name, a_obj.UNIQUEID, "OBJECTID")) as address_point_rows:
                                for address_point_row in address_point_rows:
                                    #get value
                                    value_addy = address_point_row[0]  # Address Point [FC-specific field (OK: either ESN or NAME)]
                                    segID = address_point_row[1]  # Address Point Unique ID
                                    objectID = address_point_row[2]  # Address Point OBJECTID

                                    if segID is not None:
                                        try:
                                            #see if the values match
                                            if value_addy.strip().upper() != feature_value.strip().upper():
                                                #this issue has been demoted to a notice
                                                report = "Notice: Address point %s does not match %s in %s layer." % (unicode(objectID), feature, basename(layer))
                                                val = (today, report, filename, feature, segID, "Check ESN MUNI Attributes")
                                                values.append(val)
                                        except:
                                            userMessage("Issue comparing value for %s with OBJECTID: %s" % (feature, unicode(objectID)))
                                    else:
                                        userMessage("No NENA Unique ID for address point with OBJECTID %i. Its %s attribute was not checked against its containing %s polygon." % (objectID, feature, basename(layer)))
                                        report = "Notice: Address point with OBJECTID %s does not have a NENA Unique ID. Its %s attribute was not checked against its containing %s polygon." % (unicode(objectID), feature, basename(layer))  # TODO: Is this correct?
                                        val = (today, report, filename, feature, unicode(objectID), "Check ESN MUNI Attributes")
                                        values.append(val)

                            Delete_management(lyr1)
                            del lyr1

                    try:
                        del poly, polys
                    except:
                        userMessage("Poly/polys didn't exist in the Muni/ESN check. No worries.")
                else:
                    userMessage("%s layer does not exist. Check geodatabase dataset if this is incorrect." % basename(layer))
            Delete_management(addy_lyr)

        else:
            userWarning(address_points + " does not exist")

    except Exception as e:
        report = "Notice: ESN/Municipality check did not run. " + unicode(e)
        val = (today, report, filename, "", "", "Check ESN MUNI Attributes")
        values.append(val)

    #report records
    if values != []:
        RecordResults(recordType, values, gdb)
        userWarning("Address point ESN/Municipality check complete. %s issues found. Results are in the FieldValuesCheckResults table." % (str(len(values))))
    else:
        userMessage("Address point ESN/Municipality check complete. No issues found.")


def checkAddressPointGEOMSAG(currentPathSettings):
	# get address point & road centerline path & object
    userMessage("Checking address point GEOMSAG values...")
    gdb = currentPathSettings.gdbPath
    rc = currentPathSettings.gdbObject.RoadCenterline
    ap = currentPathSettings.gdbObject.AddressPoints

    rc_obj = NG911_GDB_Objects.getFCObject(rc)
    ap_obj = NG911_GDB_Objects.getFCObject(ap)

    # prep for error reporting
    values = []
    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")
    filename = "ADDRESS_POINT" # Changed to OK Fields/Layer

	# set where clause to just get address points where GEOMSAG = 'Y' and SUBMIT = 'Y'
    ap_wc = "%s = 'Y' AND %s = 'Y' AND %s <> 'NO_MATCH'" % (ap_obj.SUBMIT, ap_obj.GEOMSAG, ap_obj.RCLMatch)

	# get feature layer of those address points
    fl_ap = "fl_ap"
    MakeFeatureLayer_management(ap, fl_ap, ap_wc)

    # see if any of these exist
    count = getFastCount(fl_ap)

    if count > 0:

        # fields should include NGADDID, RCLMatch, & RCLSide
        ap_fields = [ap_obj.UNIQUEID, ap_obj.RCLMatch, ap_obj.RCLSide]

    	# set up a search cursor on those address points
        with SearchCursor(fl_ap, ap_fields) as rows:
            for row in rows:
                # set variables
                addid, segid, rclside = row[0], row[1], row[2]

                if rclside == "N":
                    report = "Error: RCLSide set to N while RCLMatch has a valid NGSEGID. RCLSide should be R or L."
                    val = (today, report, filename, "GEOMSAG", addid, "Check Address Point GEOMSAG")
                    values.append(val)
                else:
                    # set up road centerline where clause
                    rc_wc_list = [rc_obj.UNIQUEID, " = '", segid, "'"]
                    rc_wc = "".join(rc_wc_list)

                    # set up road centerline
                    rc_fields = [rc_obj.SUBMIT, "GEOMSAG" + rclside]
                    # set up a search cursor on the RCLMatch road segment
                    with SearchCursor(rc, rc_fields, rc_wc) as r_rows:
                        for r_row in r_rows:

                            # if GEOMSAG on the proper road side is "Y", mark that address point as an error
                            if r_row[0] == 'Y' and r_row[1] == 'Y':
                                report = "Error: Point duplicates GEOMSAG with RCLMatch record %s on %s side" % (unicode(segid), rclside)
                                val = (today, report, filename, "GEOMSAG", addid, "Check Address Point GEOMSAG")
                                values.append(val)


    #report records
    if values != []:
        RecordResults(recordType, values, gdb)
        userWarning("Address point GEOMSAG check complete. %s issues found. Results are in the FieldValuesCheckResults table." % (str(len(values))))
    else:
        userMessage("Address point GEOMSAG check complete. No issues found.")

    # clean up
    cleanUp([fl_ap])

def checkUniqueIDFormat(input_fc, layer_name, input_field, use_FieldValuesCheckResults=True):
    # type: (str, str, str, bool) -> Tuple[List[unicode], int, int]
    """
    Parameters
    ----------
    input_fc : str
        Input feature class that will be checked.
    layer_name : str
        Correct layer name to be used in the Unique NENA ID format check.
    input_field : str
        Unique NENA ID Field to be checked.
    use_FieldValuesCheckResults : bool
        True if export values to FieldValuesCheckResults table. False will only return values.

    Returns
    -------
    bad_ids : list of unicode
        List of incorrectly formatted Unique NENA IDs.
    null_ids : int
        Number of null Unique NENA IDs.
    good_ids : int
        Number of good Unique NENA IDs.
    """
    # imports
    import re

    # initial parameters
    bad_ids = []
    null_ids = 0
    good_ids = 0

    # prep for error reporting
    values = []
    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")

    # begin search of NENA IDs
    with SearchCursor(input_fc, input_field) as cursor:
        for row in cursor:
            uid = row[0] # NENA ID
            regex = "^" + layer_name + "_[{}A-Za-z\d-]+@[A-Za-z\d]+\.[A-Za-z\d]+\.ok\.gov$" # correct format
            if uid in [None, "", " "]:
                null_ids += 1 # Null value count
            elif re.search(regex, uid) is None:
                # NENA ID is not correctly formatted
                bad_ids.append(uid)
                if use_FieldValuesCheckResults:
                    report = "Error: Unique ID format wrong."
                    val = (today, report, basename(input_fc), input_field, uid, "Check Unique ID Format")
                    values.append(val)
            else:
                good_ids += 1
    # output to FieldValuesCheckResults table
    if use_FieldValuesCheckResults:
        if null_ids > 0:
            report = "Error: %i records with null Unique IDs." % null_ids
            val = (today, report, basename(input_fc), input_field, "", "Check Unique ID Format")
            values.append(val)
        if values != []:
            RecordResults(recordType, values, dirname(dirname(input_fc)))
            userWarning("There are %i records in %s with null or incorrectly-formatted unique IDs." % (len(bad_ids) + null_ids, layer_name))

    bad_ids = [unicode(x) for x in bad_ids]  # Ensure bad_ids is a list of unicode

    # returns values for additional use (check before GDB is created).
    return bad_ids, null_ids, good_ids

def checkUniqueIDFrequency(currentPathSettings):
    # type: (NG911_Session_obj) -> None
    '''
    Checks for any repeat Unique IDs.

    Parameters
    ----------
    currentPathSettings : NG911_Session_obj
        See class documentation

    Returns
    -------
    None
    '''
    gdb = currentPathSettings.gdbPath
    esbList = currentPathSettings.gdbObject.esbList
    fcList = currentPathSettings.gdbObject.fcList
    esb_uniqueid = "NGUID_ESB"

    layerList = []

    env.workspace = gdb
    table = "ESB_IDS"

    #create temp table of esbID's
    # if len(esbList) > 1 and esbList[0] != esbList[1]:
    #     layerList = ["ESB_IDS"]
    #
    #     deleteExisting(table)
    #
    #     CreateTable_management(gdb, table)
    #
    #     AddField_management(table, esb_uniqueid, "TEXT", "", "", 38)
    #     AddField_management(table, "ESB_LYR", "TEXT", "", "", 30)
    #
    #     esbFields = (esb_uniqueid)
    #
    #     #copy ID's & esb layer type into the table
    #     for esb in esbList:
    #         with SearchCursor(esb, esbFields) as rows:
    #             for row in rows:
    #                 typeEsb = basename(esb)
    #                 cursor = InsertCursor(table, (esb_uniqueid, 'ESB_LYR'))
    #                 cursor.insertRow((row[0], typeEsb))
    #
    #     try:
    #         #clean up
    #         del rows, row, cursor
    #     except:
    #         userMessage("objects cannot be deleted, they don't exist")
    #

    # make sure all the proper layers actually exist
    for fc in fcList:
        if Exists(fc):
            layerList.append(basename(fc))
        else:
            msg = "%s does not exist" % (fc)
            userWarning(msg)
            today = strftime("%Y/%m/%d")
            values = [(today, msg)]
            # RecordResults("DASCmessage", values, gdb)

    # set up reporting
    values = []
    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")

    #loop through layers in the gdb that aren't esb & ESB_IDS
    for key, layer in enumerate(layerList):
        obj = NG911_GDB_Objects.getFCObject(layer)

        # check unique NENA ID for format
        try:
            layer_path = fcList[key]
            checkUniqueIDFormat(layer_path, layer, obj.UNIQUEID, True)
        except Exception as e:
            userWarning(unicode(e))
            userMessage("Could not check unique ID format for " + layer)

        # check unique NENA ID frequency
        try:
            ids = []
            with SearchCursor(layer, (obj.UNIQUEID)) as rows:
                for row in rows:
                    if row[0] not in ids:
                        ids.append(row[0])
                    else:
                        #report duplicate IDs
                        report = "Error: %s is a duplicate ID" % (unicode(row[0]))
##                        if stringESBReport != "":
##                            report = report + " in " + stringESBReport
                        val = (today, report, layer, obj.UNIQUEID, row[0], "Check Unique IDs")
                        values.append(val)

##            freq_table = layer + "_freq"
##            deleteExisting(freq_table)
##            obj = NG911_GDB_Objects.getFCObject(layer)
##            Statistics_analysis(layer, freq_table, [[obj.UNIQUEID,"COUNT"]], obj.UNIQUEID)
##
##            #set parameters for the search cursor
##            where_clause = "FREQUENCY > 1"
##
##            fields = (obj.UNIQUEID, "FREQUENCY")
##
##            fl = "fl"
##
##            MakeTableView_management(freq_table, fl, where_clause)
##
##            if getFastCount(fl) > 0:
##
##                #set a search cursor with just the unique ID field
##                with SearchCursor(freq_table, fields, where_clause) as rows2:
##                    stringESBReport = ""
##                    for row2 in rows2:
##                        reportLayer = layer
##                        if layer == "ESB_IDS":
##                            reportLayer = "ESB"
##                            stringEsbInfo = []
##                            wc2List = [esb_uniqueid, " = '", str(row2[0]), "'"]
####                            wc2 = esb_uniqueid + " = '" + str(row2[0]) + "'"
##                            wc2 = "".join(wc2List)
##                            with SearchCursor("ESB_IDS", ("ESB_LYR"), wc2) as esbRows:
##                                for esbRow in esbRows:
##                                    stringEsbInfo.append(esbRow[0])
##
##                            stringESBReport = " and ".join(stringEsbInfo)
##
##                        #report duplicate IDs
##                        report = "Error: %s is a duplicate ID" % (str(row2[0]))
##                        if stringESBReport != "":
##                            report = report + " in " + stringESBReport
##                        val = (today, report, reportLayer, esb_uniqueid, row2[0], "Check Unique IDs")
##                        values.append(val)
##
##            cleanUp([freq_table, fl])

        except Exception as e:
            userWarning(unicode(e))
            userMessage("Issue with " + layer)

    #report duplicate records
    if values != []:
        RecordResults(recordType, values, gdb)
        userWarning("Checked unique ID frequency. There were %s issues. Results are in table FieldValuesCheckResults." % (str(len(values))))
    else:
        userMessage("All ID's are unique.")

    #if it exists, clean up table
    deleteExisting(table)

def checkFrequency(fc, freq, fields, gdb, fullFreq):
    # type: (str, str, str, str, str) -> None
    """
    I don't know yet, but I will know once we go through it.

    Parameters
    ----------
    fc : str
        Feature class fullpath
    freq : str
        Address point or road centerline frequency table fullpath
    fields : str
        String of semicolon delimited field names for frequency checking
    gdb : str
        Geodatabase fullpath
    fullFreq : str
        String that represents boolean (true or false)

    Returns
    -------
    None
    """
    # AP_freq = gdbObject.AddressPointFrequency -> freq
    # AP_fields = a_obj.FREQUENCY_FIELDS_STRING -> fields

    if fullFreq == "true":
        userMessage("Checking record frequency...")
    elif fullFreq == "false":
        userMessage("Checking dual carriageways...")

    obj = NG911_GDB_Objects.getFCObject(fc)

    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")
    values1 = []

    if Exists(fc):
        fl = "fl"
        fl1 = "fl1"
        wc = "FREQUENCY > 1"

        #remove the frequency table if it exists already
        try:
            deleteExisting(freq)
        except:
            userWarning("Please manually delete %s and then run the frequency check again." % freq)
            val1 = (today, "Error: Frequency table exists; please delete or close and rerun the check.", basename(freq), "", "", "Check %s Frequency" % basename(fc))
            values1 += [val1]


        if not Exists(freq):

            # set name of exported dbf
            folder = dirname(dirname(dirname(fc)))
            dbf = join(folder, "freq_shp_temp.dbf")

            # make sure the shp copy doesn't exist
            if Exists(dbf):
                Delete_management(dbf)

            # export the feature class to a shapefile
            CopyRows_management(fc, dbf)

            #set up parameters to report duplicate records
            filename = basename(fc)
            values = []
            hno_yes = 1

            #test to see if the Address field is a number or text
            if basename(freq) == "AP_Freq":
                ap_fields = ListFields(fc)

                for ap_field in ap_fields:
                    # if ap_field.name == "Address" and ap_field.type != "Integer":
                    if ap_field.name == "Address" and ap_field.type not in ["Integer", "Double"]: # Changed to OK Fields
                        hno_yes = 0

            if hno_yes == 1:

                # see if we're working with address points or roads, create a where clause
                if basename(freq) == "AP_Freq":
                    # wc1 = obj.Address + " <> 0 and " + obj.LOCTYPE + " = 'PRIMARY' AND SUBMIT = 'Y'"
                    # wc1List = [obj.Address, " <> 0 and ", obj.LOCTYPE, " = 'PRIMARY' AND ", obj.SUBMIT, " = 'Y'"]
                    wc1List = [obj.Address, " <> 0 AND ", obj.SUBMIT, " = 'Y'"]
                    # wc1List = [obj.Address, " <> 0 and ", obj.LOCTYPE, " = 'PRIMARY' AND SUBMIT = 'Y'"] # Changed to OK Fields
                elif basename(freq) == "Road_Freq":
                    # wc1 = obj.Add_L_From + " <> 0 AND " + obj.Add_L_To + " <> 0 AND " + obj.Add_R_From + " <> 0 AND " + obj.Add_R_To + " <> 0 AND SUBMIT = 'Y'"
                    wc1List = [obj.Add_L_From, " <> 0 AND ", obj.Add_L_To, " <> 0 AND ", obj.Add_R_From, " <> 0 AND ", obj.Add_R_To, " <> 0 AND ", obj.SUBMIT, " = 'Y'"]
                    # wc1List = [obj.Add_L_From, " <> 0 AND ", obj.Add_L_To, " <> 0 AND ", obj.Add_R_From, " <> 0 AND ", obj.Add_R_To, " <> 0 AND SUBMIT = 'Y'"] # Changed to OK Fields
                wc1 = "".join(wc1List)

                #run query on fc to make sure 0's are ignored
                MakeTableView_management(dbf, fl1, wc1)

                #set up field strings for statistics tool
                fields = fields.replace(";;", ";")
                fieldCountList = fields.replace(";", " COUNT;") + " COUNT"

                #split field names
                fieldsList = fields.split(";")
                feature_layer_fields = [f.strip() for f in fieldsList]

                #run frequency analysis
                try:
                    Statistics_analysis(fl1, freq, fieldCountList, fields)

                    #make feature layer
                    MakeTableView_management(freq, fl, wc)

                    #get count of the results
                    if getFastCount(fl) > 0:

                        #get field count
                        field_count = len(feature_layer_fields)
                        # AddMessage(fCount)
                        # AddMessage(fl_fields)

                        #get the unique ID field name
                        id1 = obj.UNIQUEID
                        # AddMessage(id1)

                        # fieldCalls = [str(id1)]
                        #
                        # for fieldID in fl_fields:
                        #     AddMessage(fieldID)
                        #     AddMessage(type(fieldID))
                        #     fieldCalls = fieldCalls + [fieldID]
                        # AddMessage(fieldCalls)

                        #run a search on the frequency table to report duplicate records
                        with SearchCursor(freq, feature_layer_fields, wc) as rows:
                            for row in rows:
                                i = 0
                                # AddMessage(row)
                                #generate where clause to find duplicate ID's
                                wcList = []
                                while i < field_count:
                                    stuffList = []  # List of conditions used to make the where clause
                                    if row[i] is not None:

                                        # see if the data type is an int
                                        if type(row[i]) == int:
                                            # if it is a int, we don't want quotes included
                                            stuffList = [" = ", unicode(row[i]), " "]
                                        # if it is a float, we don't want quotes included
                                        elif type(row[i]) == float:
                                            stuffList = [" = ", unicode(row[i]), " "]
                                        else:
                                            # if not, we need to include quotes
                                            stuffList = [" = '", row[i], "' "]
                                    else:
                                        # or put in null
                                        stuffList = [" is null "]

                                    # make one statement from the various field components
                                    stuff = "".join(stuffList)

                                    # add to the official where clause list
                                    wcList = wcList + [unicode(feature_layer_fields[i]), stuff, "and "]
                                    i += 1

                                #trim last "and " off where clause
                                wcList.pop()

                                # create the official string where clause statement
                                wc = "".join(wcList)

                                # AddMessage(wc)

                                #find records with duplicates to get their unique ID's
                                with SearchCursor(fl1, id1, wc) as sRows:
                                # with SearchCursor(fl1, (fieldCalls), wc) as sRows:
                                    for sRow in sRows:
                                        fID = sRow[0]

                                        #add information to FieldValuesCheckResults for all duplicates
                                        if fullFreq == "true":
                                            report = "Error: %s has duplicate field information" % (unicode(fID))
                                        else:
                                            report = "Notice: %s has duplicate address range information" % (unicode(fID))
                                        # userMessage(report)
                                        val = (today, report, filename, "", unicode(fID), "Check " + filename + " Frequency")
                                        values.append(val)

                    else:
                        if fullFreq == "true":
                            userMessage(filename + ": Checked frequency. All records are unique.")
                        elif fullFreq == "false":
                            userMessage(filename + ": Checked dual carriageways. All records are unique.")

                except Exception as e:
                    userMessage(unicode(e))
                    report = "Error: Could not complete duplicate record check. " + unicode(e)
                    val = (today, report, filename, "", "", "Check " + filename + " Frequency")
                    values.append(val)

                #report duplicate records
                if values:
                    RecordResults(recordType, values, gdb)
                    userWarning("Checked frequency. There were %s duplicate records. Individual results are in table FieldValuesCheckResults" % (str(len(values))))

                #clean up
                try:
                    cleanUp([fl, fl1, freq])
                    if Exists(dbf):
                        Delete_management(dbf)
                except:
                    userMessage("Issue deleting a feature layer or frequency table.")
            else:
                userWarning("Address field of Address Points is not an integer or a double field.")
                val1 = (today, "Error: Address field of Address Points is not an integer/double field", filename, "", "", "Check " + filename + " Frequency")
                values1 = [val1]
                RecordResults(recordType, values1, gdb)
        else:
            RecordResults(recordType, values1, gdb)
    else:
        userWarning(fc + " does not exist")


def checkLayerList(pathsInfoObject):
    gdb = pathsInfoObject.gdbPath
    esb = pathsInfoObject.gdbObject.esbList

    values = []
    today = strftime("%Y/%m/%d")

    #make sure the NG911 feature dataset exists
    userMessage("Checking feature dataset name...")
    env.workspace = gdb

    datasets = ListDatasets()

    if "NG911" not in datasets:
        dataset_report = "Error: No feature dataset named 'NG911' exists"
        val = (today, dataset_report, "Template", "Check Dataset")
        values.append(val)
        userMessage(dataset_report)

    userMessage("Checking geodatabase layers...")
    #get current required layer list
    layerList = pathsInfoObject.gdbObject.requiredLayers
    feature_dataset = pathsInfoObject.gdbObject.NG911_FeatureDataset

    # userMessage(feature_dataset)

    for l in layerList:
        if not Exists(l):
            report = "Error: Required layer %s is not in geodatabase dataset." % basename(l)
            userWarning(report)
            val = (today, report, "Layer", "Check Layer List")
            values.append(val)

    # make sure ESB layers have the right names
    # env.workspace = join(gdb, "NG911")
    # fcs = ListFeatureClasses()
    # esb_count = 0
    # for esb in ["ESB_EMS_BOUNDARY", "ESB_LAW_BOUNDARY", "ESB_FIRE_BOUNDARY"]:
    #     if esb in fcs:
    #         esb_count += 1
    #
    # if esb_count == 0 and "ESB" not in fcs:
    #     report = "Error: No ESB layers are present in geodatabase."
    #     userMessage(report)
    #     val = (today, report, "Layer", "Check Layer List")
    #     values.append(val)
    #
    # if 0 < esb_count < 3:
    #     report = "Error: ESB layers %s may not be named correctly in geodatabase." % (esb)
    #     userMessage(report)
    #     val = (today, report, "Layer", "Check Layer List")
    #     values.append(val)

    #record issues if any exist
    if values != []:
        RecordResults("template", values, gdb)
        userWarning("Not all required geodatabase datasets and/or layers are not present. See TemplateCheckResults.")
    else:
        userMessage("Checked that required layers are present.")


# def getKeyword(layer, esb):
#     keyword = "EmergencyBoundary" if layer in esb else layer
#     return keyword


def getRequiredFields(folder):
    path1 = path.join(folder, "NG911_RequiredFields.txt")

    #create a field definition dictionary
    rfDict = {}

    #make sure file path exists
    if path.exists(path1):
        fieldDefDoc = open(path1, "r")

        #parse the text to populate the field definition dictionary
        for line in fieldDefDoc.readlines():
            stuffList = line.split("|")
            #set up values
            fc = stuffList[0]
            field = stuffList[1].rstrip()
            fieldList = []

            #see if field list already exists
            if fc in rfDict.keys():
                fieldList = rfDict[fc]

            #append new value onto list
            fieldList.append(field)

            #set value as list
            rfDict[fc] = fieldList
    else:
        userWarning("The file %s is required to run field checks." % path1)

    return rfDict


def getFieldDomain(domain, folder):
    # type: (str, str) -> Dict[str, str]

    # get full path to domain
    docPath = path.join(folder, domain + "_Domains.txt")

    domainDict = {}

    #make sure path exists
    if path.exists(docPath):
        with open(docPath, "r") as doc:
            doc.readline()  # Purge header row
            #parse the text to population the field definition dictionary
            for line in doc.readlines():
                if line != "\n":
                    stuffList = line.split("|")
                    domainDict[stuffList[0].strip()] = stuffList[1].strip()

    else:
        userWarning("The file %s is required to run a domain check." % docPath)

    return domainDict

def getTableFieldInfo(table, folder = None):
    # type: (str, str) -> Dict[str, str]
    from NG911_GDB_Objects import NG911_Session

    # get full path to domain
    gdbPath = dirname(table)
    if folder is None:
        folder = NG911_Session(gdbPath).fieldsFolderPath

    # userMessage(folder)

    tablename = basename(table)
    docPath = path.join(folder, tablename + ".txt")

    domainDict = {}

    #make sure path exists
    if path.exists(docPath):
        doc = open(docPath, "r")

        #parse the text to population the field definition dictionary
        firstline = doc.readline()
        for line in doc.readlines():
            if line != "\n":
                stuffList = line.split("|")
                domainDict[stuffList[0].strip()] = {
                    "type":stuffList[1].strip(),
                    "length":int(stuffList[2].strip()) if stuffList[2].strip() is not '' else '',
                    "domain":stuffList[3].strip()
                }

    else:
        userWarning("The file %s is required to run a domain check." % (docPath))

    return domainDict


def launchRangeFinder(f_add, t_add, parity):
    sideRange = []

    if [f_add, t_add] != [0,0]:

        if parity != 'Z':
            # set the counter for the range, it'll usually be 2
            range_counter = 2
            if parity == "B": # if the range is B (both sides), the counter = 1
                range_counter = 1

            # get the range
            sideRange = []
            sideRange = list(range(f_add, t_add + range_counter, range_counter))
            high = t_add

            # if the range was high to low, flip it
            if sideRange == []:
                sideRange = list(range(t_add, f_add + range_counter, range_counter))
                high = f_add

            # make sure the range didn't extend beyond the high
            if len(sideRange) > 1:
                while sideRange[-1] > high:
                    sideRange.pop()

    return sideRange


def checkMsagLabelCombo(msag, current_fullname, overlaps, rd_fc, fields, msagList, name_field, txt, v21):
    # type: (str, str, List[str], str, Union[Tuple, List], List[str], str, str, int) -> List[str]
    """

    Parameters
    ----------
    msag : str

    current_fullname : str
        Current value of the FullName field
    overlaps : list of str
    rd_fc : str
    fields : tuple of str or list of str
        When called from FindOverlaps, this parameter is:
        `(left_from,left_to,right_from,right_to,parity_l,parity_r,segid,msagco_l,msagco_r)`
    msagList : list of str
    name_field : str
        Name of the field that will be created for comparing the label
    txt : str
    v21 : str

    Returns
    -------
    list of str:
        List of unique IDs

    """
    address_list = []
    checked_segids = []
    dict_ranges = {}
    for msagfield in msagList:
        side = msagfield[-1]

        if "'" in current_fullname:
            current_fullname = current_fullname.replace("'", "''")

        wcList = [msagfield, " = '", msag, "' AND ", name_field, " = '", current_fullname, "' AND SUBMIT = 'Y'"]

        if v21 == 1:
            wcList = wcList + ["AND GeoMSAG_", side, " = 'Y'"]  # Changed to OK fields

        wc = "".join(wcList)

        with SearchCursor(rd_fc, fields, wc) as rows:
            for row in rows:
                l_f_add, l_t_add, r_f_add, r_t_add, parity_l, parity_r, segid, msagco_l, msagco_r = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7].strip(), row[8].strip()
                if segid + "|2" not in checked_segids:

                    # creates dictionary for parameters of each road side
                    # deal with the left side first
                    dict_para = {
                        "left": {
                            "from": l_f_add,
                            "to": l_t_add,
                            "parity": parity_l,
                            "msagco": msagco_l,
                            "X": "L"
                        },
                        "right": {
                            "from": r_f_add,
                            "to": r_t_add,
                            "parity": parity_r,
                            "msagco": msagco_r,
                            "X": "R"
                        }
                    }
                    for side_of_road in dict_para:
                        dict_side = dict_para[side_of_road]
                        if [dict_side["from"], dict_side["to"]] != [0,0] and None not in [dict_side["from"], dict_side["to"]]:
                            if dict_side["msagco"] == msag:
                    # for side_of_road in [[l_f_add, l_t_add, parity_l, msagco_l, "L"],[r_f_add, r_t_add, parity_r, msagco_r, "R"]]:
                        
                        # for address_from, address_to, parity, msagco, X in izip([[l_f_add, l_t_add, parity_l, msagco_l, "L"],[r_f_add, r_t_add, parity_r, msagco_r, "R"]]:
                        # make sure the range isn't 0,0 or null
                        # if [side_of_road[0], side_of_road[1]] != [0,0] and None not in [side_of_road[0], side_of_road[1]]:
                        #     if side_of_road[3] == msag:
                                thisRange = launchRangeFinder(dict_side["from"], dict_side["to"], dict_side["parity"])
                                if thisRange != []:
                                    dict_ranges[segid + "|" + dict_side["X"]] = thisRange
                                    for lR in thisRange:
                                        if lR not in address_list:
                                            address_list.append(lR)
                                        else:
                                            # find out where the overlap is
                                            # lR is the value that exists somewhere else
                                            for key in dict_ranges:
                                                values = dict_ranges[key]
                                                if lR in values:
                                                    k_segid = key.split("|")[0]
                                                    # make sure the script isn't comparing a road segment to itself
                                                    writeToText(txt, "Address " + unicode(lR) + " overlaps between NGSEGID " + unicode(k_segid) + " and NGSEGID " + unicode(segid) + "\n")
                                                    if k_segid not in overlaps:
                                                        overlaps.append(k_segid)
                                                    # this means there's an overlap & we found the partner
                                                    if segid not in overlaps:
                                                        overlaps.append(segid)

                    if msagco_l == msagco_r:
                        checked_segids.append(segid + "|2")
                    else:
                        if segid + "|1" in checked_segids:
                            checked_segids.remove(segid + "|1")
                            checked_segids.append(segid + "|2")
                        else:
                            checked_segids.append(segid + "|1")

    del checked_segids, address_list, dict_ranges, row, rows, dict_para
    return overlaps


def FindOverlaps(working_gdb):
    """
    Checks road segments for overlapping address ranges.

    Parameters
    ----------
    working_gdb : str
        Full path to the working geodatabase
    """
    # start_time = time.time()
    userMessage("Checking overlapping address ranges...")
    #get gdb object
    gdb_object = NG911_GDB_Objects.getGDBObject(working_gdb)

    env.workspace = working_gdb
    env.overwriteOutput = True
    rd_fc = gdb_object.RoadCenterline         # Our street centerline feature class path
    final_fc = join(gdb_object.gdbPath, "AddressRange_Overlap")
    rd_object = NG911_GDB_Objects.getFCObject(rd_fc) # Road centerline feature class object
    name_field = "NAME_OVERLAP"
    parity_l = rd_object.PARITY_L
    parity_r = rd_object.PARITY_R
    left_from = rd_object.Add_L_From         # The left from address field
    left_to = rd_object.Add_L_To            # The left to address field
    right_from = rd_object.Add_R_From        # The right from address field
    right_to = rd_object.Add_R_To            # The right to address field
    msagco_l = rd_object.MSAGCO_L
    msagco_r = rd_object.MSAGCO_R
    segid = rd_object.UNIQUEID
    # version = rd_object.GDB_VERSION
    geomsag_l = rd_object.GEOMSAGL
    geomsag_r = rd_object.GEOMSAGR
    fields = (left_from, left_to, right_from, right_to, parity_l, parity_r, segid, msagco_l, msagco_r)
    msagList = [msagco_l, msagco_r]
    txt = working_gdb.replace(".gdb", "_OverlappingAddressSpecifics.txt")
    if exists(txt):
        remove(txt)

    # set up issue reporting variables
    values = []
    resultType = "fieldValues"
    today = strftime("%Y/%m/%d")

    # turn off editor tracking
    # DisableEditorTracking_management(rd_fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")

    # clean up if final overlap output already exists
    if Exists(final_fc):
        Delete_management(final_fc)

    # add the NAME_OVERLAP field
    if not fieldExists(rd_fc, name_field):
##        DeleteField_management(rd_fc, name_field)
        AddField_management(rd_fc, name_field, "TEXT", "", "", 150)

    # calculate values for NAME_OVERLAP field
    # Attribute FULLNAME_FIELDS of class NG911RoadCenterlineObject:
    # = [self.FullName, self.PreDir, self.PreTypeSep, self.Street, self.StreetType, self.SufDir, self.SufMod]
    field_list = rd_object.FULLNAME_FIELDS
    field_list[0] = name_field  # Replace FullName field with name_field
    fields1 = tuple(field_list)  # Equivalent to FULLNAME_FIELDS, except element 0 is name_field instead of the FullName field

    # start edit session
    with Editor(working_gdb):

        # run update cursor to calculate name_field
        with UpdateCursor(rd_fc, fields1) as rows:
            for row in rows:
                field_count = len(fields1)
                start_int = 1  # Element 0 is the field we're updating; skip it
                rd_fullname = u""

                # loop through the fields to see what's null & skip it
                while start_int < field_count:
                    if row[start_int] not in [None, "", " "]:
                        rd_fullname = rd_fullname + " " + unicode(row[start_int])
                    start_int = start_int + 1

                row[0] = rd_fullname
                rows.updateRow(row)

    # clean up name_field by removing unnecessary spaces if present
    trim_expression = '" ".join(!' + name_field + '!.split())'
    CalculateField_management(rd_fc, name_field, trim_expression, "PYTHON_9.3")

##    now_time = time.time()
##    print("Marker: done processing feature class. Elapsed time was %g seconds" % (now_time - start_time))

    # make sure the text file notification only shows up if there's an overlap problem
    overlap_error_flag = 0

##    try:
    if 1 == 1:  # If the laws of mathematics still check out, do the following:
        already_checked = []
        rd_fields = [msagco_l, msagco_r, name_field, segid]
        v21 = 0
        # if version == "21":
        v21 = 1
        rd_fields = rd_fields + [geomsag_l, geomsag_r]

        overlaps = []

        with SearchCursor(rd_fc, rd_fields, "SUBMIT = 'Y'") as cursor:
            for row in cursor:

                # in the 2.1 geodatabase, make sure only authoritative sides are checked
                checkL, checkR = 0, 0
                # if version == "21":
                if row[4] == "Y":
                    checkL = 1
                if row[5] == "Y":
                    checkR = 1
                # elif version == "20":
                #     checkL, checkR = 1, 1

                # make sure each MSAGCO_X is populated with a value
                # MSAGCO_X (Kan. field) -> MSAGComm_X (Okla.) | Value appears to be a county name based on sample data
                i = 0
                while i < 2:
                    if row[i] is None or row[i] in ('', ' '):
                        if i == 0:
                            checkL = 0 # this means the left side MSAG isn't a thing
                            report = "Notice: MSAGComm_L needs to be a real value"
                            val = (today, report, basename(rd_fc), "MSAGComm_L", row[3], "Overlapping Address Range")
                            values.append(val)
                        elif i == 1:
                            checkR = 0 # this means the right side MSAG isn't a thing
                            report = "Notice: MSAGComm_R needs to be a real value"
                            val = (today, report, basename(rd_fc), "MSAGComm_R", row[3], "Overlapping Address Range")
                            values.append(val)

                    i += 1


                if checkL == 1 and row[0] + "|" + row[2] not in already_checked:
                    # check the left side MSAGCO & LABEL combo
                    overlaps = checkMsagLabelCombo(row[0], row[2], overlaps, rd_fc, fields, msagList, name_field, txt, v21)
                    already_checked.append(row[0] + "|" + row[2])

                # if the r & l msagco are different, run the right side
                if checkR == 1 and row[0] != row[1] and row[1] + "|" + row[2] not in already_checked:
                    overlaps = checkMsagLabelCombo(row[1], row[2], overlaps, rd_fc, fields, msagList, name_field, txt, v21)
                    already_checked.append(row[1] + "|" + row[2])

##        now_time = time.time()
##        print("Marker: done checking MSAGs. Elapsed time was %g seconds" % (now_time - start_time))

        if overlaps != []:
            overlap_error_flag = 1
            userMessage("%s overlapping address range segments found. Please see %s for overlap results." % (str(len(overlaps)), final_fc))
            # add code here for exporting the overlaps to a feature class
            wcList = [segid, " in ('" +"','".join(overlaps), "')"]
            wc = "".join(wcList)
##            wc = segid + " in ('" +"','".join(overlaps) + "')"
            overlaps_lyr = "overlaps_lyr"
            MakeFeatureLayer_management(rd_fc, overlaps_lyr, wc)

            # get the count of persisting overlaps
            count = getFastCount(overlaps_lyr)

            # if there are more than 1, copy the layer
            if count > 0:
                CopyFeatures_management(overlaps_lyr, final_fc)

            Delete_management(overlaps_lyr)

            # add reporting for overlapping segments
            for ov in overlaps:
                report = "Notice: %s has an overlapping address range." % (unicode(ov))
                val = (today, report, basename(rd_fc), "", ov, "Overlapping Address Range")
                values.append(val)

##            now_time = time.time()
##            print("Marker: done creating error report. Elapsed time was %g seconds" % (now_time - start_time))

        else:
            userMessage("No overlaping address ranges found.")

    else:
        class CatastropicError(Exception):
            pass
        raise CatastropicError("Apparently 1 does not equal 1 today. Try again later, or try turning math off and back on again.")
##
##            now_time = time.time()
##            print("Marker: skipped error reporting. Elapsed time was %g seconds" % (now_time - start_time))

##    except Exception as e:
##        userWarning(str(e))

    # delete field if need be
    # if fieldExists(rd_fc, name_field):
    #     try:
    #         DeleteField_management(rd_fc, name_field)
    #     except:
    #         pass
    delete_field_if_exists(rd_fc, name_field)  # Replaces above commented-out code

    if values:
        RecordResults(resultType, values, working_gdb)
        userWarning("Completed checking overlapping addresses: %i issues found. See table FieldValuesCheckResults for results." % len(values))
        if overlap_error_flag == 1:
            userWarning("All specific overlaps with corresponding NGSEGIDs are listed in " + txt)
    else:
        userMessage("Completed checking overlapping addresses: 0 issues found")

##    now_time = time.time()
##    print("Marker: done reporting. Elapsed time was %g seconds" % (now_time - start_time))


    # turn editor tracking back on
    # EnableEditorTracking_management(rd_fc, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields

##    end_time = time.time()
##    print("Elapsed time was %g seconds" % (end_time - start_time))


def checkRCLMATCH(pathsInfoObject):
    # type: (NG911_GDB_Objects.NG911_Session_obj) -> None
    """Validates the RCLMatch field of the ADDRESS_POINTS feature class against the ROAD_CENTERLINE feature class.

    Parameters
    ----------
    pathsInfoObject : NG911_Session_obj
        The session object
    """
    gdb = pathsInfoObject.gdbPath
    ap = pathsInfoObject.gdbObject.AddressPoints
    rc = pathsInfoObject.gdbObject.RoadCenterline

    a_obj = NG911_GDB_Objects.getFCObject(ap)
    r_obj = NG911_GDB_Objects.getFCObject(rc)

    userMessage("Checking RCLMatch field...")
    #set up parameters to report duplicate records
    values = []
    resultType = "fieldValues"
    today = strftime("%Y/%m/%d")

    # set variables for comparison
    name_field = "NAME_COMPARE"
    code_field = "CODE_COMPARE"
    city_field = a_obj.MSAGCO
    # road_field_list = ["NAME_COMPARE", "PreDir", "PreTypeSep", "Street", "StreetType", "SufDir", "SufMod"]
    road_field_list = ["NAME_COMPARE"] + r_obj.FULLNAME_FIELDS[1:]
    # addy_field_list = ["NAME_COMPARE", "PreDir", "PreTypeSep", "Street", "StreetType", "SufDir", "SufMod"]
    addy_field_list = ["NAME_COMPARE"] + a_obj.FULLNAME_FIELDS[1:]

    # set holders for issues
    ngsegid_doesnt_exist = []
    doesnt_match_range = []
    streets_or_msags_dont_match = []
    null_values = []
    no_rclside = []

    # prep roads & address points for comparison

    # copy the roads to a table for comparison
    rc_table_view = "rc_table_view"
    rt = join("in_memory", "rcTable")
    if Exists(rt):
        Delete_management(rt)
    wc = r_obj.SUBMIT + " = 'Y'"

    # Take a subset of the road centerline feature class where SUBMIT = 'Y' to produce a table view
    # Copy table view to an in-memory table... not sure exactly why
    MakeTableView_management(rc, rc_table_view, wc)
    CopyRows_management(rc_table_view, rt)

    # Calculate NAME_COMPARE (label), CODE_COMPARE_L, and CODE_COMPARE_R for each road centerline feature
    prep_roads_for_comparison(
        rd_fc=rt,
        name_field=name_field,  # NAME_COMPARE
        code_fields=[code_field + "_L", code_field +"_R"],  # CODE_COMPARE_L, CODE_COMPARE_R
        city_fields=[city_field + "_L", city_field + "_R"],  # MSAGComm_L, MSAGComm_R
        field_list=road_field_list
    )

    # copy address points to a table for comparison
    ap_table_view = "ap_table_view"
    at = join("in_memory", "apTable")
    if Exists(at):
        Delete_management(at)
    wcList = [a_obj.SUBMIT, " = 'Y' AND ", a_obj.RCLMatch, " <> 'NO_MATCH'"]
    wc = "".join(wcList)
    MakeFeatureLayer_management(ap, ap_table_view, wc)
    CopyRows_management(ap_table_view, at)

    # Calculate NAME_COMPARE (label) and CODE_COMPARE for each address point feature
    prep_roads_for_comparison(
        rd_fc=at,  # in_memory\apTable
        name_field=name_field,  # NAME_COMPARE
        code_fields=[code_field],  # CODE_COMPARE
        city_fields=[city_field],  # MSAGComm
        field_list=addy_field_list
    )

    # make address points into a table view
    a = "a"
    MakeTableView_management(at, a)

    # check to see if any RCLSide values are null
    # wc_rclside = "RCLSide IS NULL and SUBMIT = 'Y' and LOCTYPE = 'PRIMARY'"
    wc_rclside = "%s IS NULL and %s = 'Y'" % (a_obj.RCLSide, a_obj.SUBMIT)
    rcl = "rcl"
    SelectLayerByAttribute_management(a, "NEW_SELECTION", wc_rclside)
    rcl_count = getFastCount(a)  # Number of address point records (for submission) where RCLSide is null

    # If there are address point records (for submission) where RCLSide is null...
    # ...then make a list of their NGUID_ADD values
    if rcl_count > 0:
        with SearchCursor(a, a_obj.UNIQUEID) as rows:
            for row in rows:
                no_rclside.append(row[0])
            del row, rows

    # clean up and clear selection
    Delete_management(rcl)
    del rcl_count
    SelectLayerByAttribute_management(a, "CLEAR_SELECTION")

    # join road & address table based on RCLMatch & NGSEGID
    r = "r"
    MakeTableView_management(rt, r)
    AddJoin_management(a, a_obj.RCLMatch, r, r_obj.UNIQUEID)

    a_ngaddid = "apTable.NGUID_ADD"

    # this will catch if the NGSEGID doesn't exist in the road centerline file
    # returns an error if RCLMatch (AP) is not null and NGUID_RDCL is null
    # i.e. the join was not successful in that the AP feature does not have a matching RDCL feature
    # If Populate AP was used, this should not happen.
    SelectLayerByAttribute_management(a, "NEW_SELECTION", "rcTable.NGUID_RDCL is null") # Changed to OK Fields
    count = getFastCount(a)  # Number of address point features without road centerline matches?

    # get a list of all the NGADDIDs with the issue that the RCLMatch doesn't exist in the road centerline
    if count > 0:
        with SearchCursor(a, a_ngaddid) as rows:
            for row in rows:
                ngsegid_doesnt_exist.append(row[0])
            del row, rows

    # clear selection
    SelectLayerByAttribute_management(a, "CLEAR_SELECTION")

    # jump into the records to see where things aren't matching
    # select records where code_compare doesn't match
    sides = ["L", "R"]

    # split up points by side
    for side in sides:

        # first, toss out any where code compares don't match
##        compare_codes_wc = a_obj.RCLSide + " = '" + side + "' AND rcTable.NGSEGID is not null AND apTable.CODE_COMPARE <> rcTable.CODE_COMPARE_" + side
        compare_codes_wc_list = [a_obj.RCLSide, " = '", side, "' AND rcTable.NGUID_RDCL is not null AND apTable.CODE_COMPARE <> rcTable.CODE_COMPARE_", side] # Changed to OK Fields
        compare_codes_wc = "".join(compare_codes_wc_list)
        SelectLayerByAttribute_management(a, "NEW_SELECTION", compare_codes_wc)
        count = getFastCount(a)

        # see if any address points had the problem
        if count > 0:
            with SearchCursor(a, a_ngaddid) as rows:
                for row in rows:
                    streets_or_msags_dont_match.append(row[0])
                del row, rows

        # clear selection
        SelectLayerByAttribute_management(a, "CLEAR_SELECTION")

        # look at ranges
##        compare_ranges_wc = a_obj.RCLSide + " = '" + side + "' AND rcTable.NGSEGID is not null AND apTable.CODE_COMPARE = rcTable.CODE_COMPARE_" + side
        compare_ranges_wc_list = [a_obj.RCLSide, " = '", side, "' AND rcTable.NGUID_RDCL is not null AND apTable.CODE_COMPARE = rcTable.CODE_COMPARE_", side] # Changed to OK Fields
        compare_ranges_wc = "".join(compare_ranges_wc_list)

        # get count of potential problems
        SelectLayerByAttribute_management(a, "NEW_SELECTION", compare_ranges_wc)
        count = getFastCount(a)

        if count > 0:

            # flds = (a_ngaddid, "apTable.Address", "rcTable.%s_F_ADD" % (side), "rcTable.%s_T_ADD" % (side), "rcTable.PARITY_%s" % (side))
            flds = (a_ngaddid, "apTable.Address", "rcTable.Add_%s_From" % side, "rcTable.Add_%s_To" % side, "rcTable.Parity_%s" % side)

            with SearchCursor(a, flds, compare_ranges_wc) as rows:
                for row in rows:
                    if None not in [type(row[2]), type(row[3])]:

                        # set the counter for the range, it'll usually be 2
                        range_counter = 2
                        if row[4] == "B": # if the range is B (both sides), the counter = 1
                            range_counter = 1

                        # get the range by the specified count
                        if row[3] > row[2]:
                            sideRange = list(range(row[2], row[3] + 2, range_counter))

                        # if the range was high to low, flip it
                        else:
                            sideRange = list(range(row[3], row[2] + 2, range_counter))

                        # see if Address is in the range
                        if int(row[1]) not in sideRange:
                            doesnt_match_range.append(row[0])
    ##                        userMessage("Address: " + str(row[1]))
    ##                        userMessage("From: " + str(row[2]))
    ##                        userMessage("To: " + str(row[3]))
    ##                        userMessage("Range: " + str(sideRange))

                    else:
                        null_values.append(row[0])
                del row, rows

    issueDict = {"Error: RCLMatch is reporting a NENA Unique ID that does not exist in the road centerline": ngsegid_doesnt_exist,
                 "Error: RCLMatch does not correspond to a NENA Unique ID that matches attributes": streets_or_msags_dont_match,
                 "Error: Address does not fit in range of corresponding RCLMatch": doesnt_match_range,
                 "Error: Road segment address ranges include one or more null values": null_values,
                 "Error: RCLSide is null": no_rclside}

    # this catches if the NGSEGID doesn't exist in the road centerline file
    for issue in issueDict:
        issueList = issueDict[issue]
        if issueList:
            for ngaddid in issueList:
                if "null values" not in issue:
                    val = (today, issue, "ADDRESS_POINT", "RCLMatch", ngaddid, "Check RCLMatch") # Changed to OK Fields/Layer
                else:
                    val = (today, issue, "ROAD_CENTERLINE", "RCLMatch", ngaddid, "Check RCLMatch") # Changed to OK Fields/Layer
                values.append(val)

    # clean up
    cleanUp([at, rt, a, r, ap_table_view, rc_table_view])

    if values != []:
        RecordResults(resultType, values, gdb)
        userWarning("Check complete. %s issues found. See table FieldValuesCheckResults for results." % (str(len(values))))
    else:
        userMessage("Check complete. All RCLMatch records correspond to appropriate road centerline segments.")


def checkMSAGCOspaces(fc1, gdb):
    """
    Checks `MSAGComm_X` field(s) for leading spaces, trailing spaces, null values, and blank values. Reports any such
    errors in the table `FieldValuesCheckResults`.

    Parameters
    ----------
    fc1 : str
        Full path to feature class with the `MSAGComm` or `MSAGComm_X` field(s) to check
    gdb : str
        Full path to the geodatabase
    """
    # define necessary variables
    fcobj = NG911_GDB_Objects.getFCObject(fc1)
    uniqueID = fcobj.UNIQUEID

    values = []
    resultType = "fieldValues"
    today = strftime("%Y/%m/%d")
    fc = basename(fc1)

    # see which MSAGCO fields we're working with
    if "ADDRESS" in fc:
        fields = ["MSAGComm"] # Changed to OK Fields
    else:
        fields = ["MSAGComm_L","MSAGComm_R"] # Changed to OK Fields

    wc_root = "SUBMIT = 'Y' AND "

    # loop through the fields to see if there are any leading or trailing spaces in the values
    for field in fields:

        # set up the where clauses to find leading or trailing spaces
        wcList = [field + " like ' %'", field + " like '% '"]
        for wc in wcList:
            fl = "fl"
            MakeFeatureLayer_management(fc, fl, wc_root + wc)

            # do reporting if issues are found
            if getFastCount(fl) > 0:
                with SearchCursor(fl, (uniqueID)) as rows:
                    for row in rows:
                        report = "Error: %s has a leading or trailing space." % field
                        # val = (today, report, fc, field, row[0], "Check Values Against Domains")
                        val = (today, report, fc, field, row[0], "Check MSAGComm Spaces")
                        values.append(val)

            # clean up between iterations
            Delete_management(fl)

        # check for blank or space-only string
        wc = field + " in ('', ' ')"
        fl = "fl"
        MakeFeatureLayer_management(fc, fl, wc_root + wc)

        # do reporting if issues are found
        if getFastCount(fl) > 0:
            with SearchCursor(fl, (uniqueID)) as rows:
                for row in rows:
                    report = "Notice: %s is a blank string or has only a space." % field
                    # val = (today, report, fc, field, row[0], "Check Values Against Domains")
                    val = (today, report, fc, field, row[0], "Check MSAGComm Spaces")
                    values.append(val)

        # clean up
        Delete_management(fl)

    if values != []:
        RecordResults(resultType, values, gdb)
        userWarning("Check complete. %s issues found. See table FieldValuesCheckResults for results." % (str(len(values))))
    else:
        userMessage("Check complete. No MSAGCO records have leading or trailing spaces.")


def checkGDBDomains(pathInfoObject):
    # type: (NG911_Session_obj) -> int

    from NG911_arcpy_shortcuts import DomainInfo
    import os
    from os.path import join
    import collections

    today = strftime("%Y/%m/%d")
    resultType = "fieldValues"
    values = []

    gdb = pathInfoObject.gdbPath # type: str
    domain_folder = pathInfoObject.domainsFolderPath

    userMessage("Checking Geodatabase Domains.")

    gdb_domains = arcpy.da.ListDomains(gdb)

    correct_domains = [] # type: List[DomainInfo]

    for file in os.listdir(domain_folder):
        correct_domains.append(DomainInfo.get_from_domainfile(join(domain_folder, file)))

    correct_names = []
    correct_descriptions = []
    correct_dicts = []

    for correct_domain in correct_domains:
        correct_names.append(correct_domain.domain_name)
        correct_descriptions.append(correct_domain.domain_description)
        correct_dicts.append(correct_domain.domain_dict)

    for gdb_domain in gdb_domains:
        if gdb_domain.name not in correct_names:
            report = "Error: Domain Name %s is not an approved domain." % (unicode(gdb_domain.name))
            val = (today, report, "GDB", "Domain", "", "Check GDB Domains")
            values.append(val)
        elif gdb_domain.name in correct_names:
            index = correct_names.index(unicode(gdb_domain.name))
            if gdb_domain.description != correct_descriptions[index]:
                if len(unicode(gdb_domain.description)) > 75:
                    report_desc = unicode(gdb_domain.description)[0:74]
                else:
                    report_desc = unicode(gdb_domain.description)
                if len(unicode(correct_descriptions[index])) > 75:
                    report_corr_desc = unicode(correct_descriptions[index])[0:74]
                else:
                    report_corr_desc = unicode(correct_descriptions[index])
                report = "Notice: Domain Description '%s' for %s Domain should be '%s'." % (report_desc, unicode(gdb_domain.name), report_corr_desc)
                if len(unicode(report)) > 250:
                    report = report[0:249]
                val = (today, report, "GDB", "Domain", "", "Check GDB Domains")
                values.append(val)
            # userMessage("Correct Dicts: %s" % str(correct_dicts[index]))
            # userMessage("Coded Dicts: %s" % str(gdb_domain.codedValues))
            gdb_domain_sort = collections.OrderedDict(sorted(gdb_domain.codedValues.items()))
            # userMessage(correct_dicts[index])
            correct_domain_sort = collections.OrderedDict(sorted(correct_dicts[index].items()))
            for key, value in gdb_domain_sort.items():
                # if gdb_domain_sort != correct_domain_sort
                if unicode(key) not in correct_domain_sort.keys():
                    report = "Error: Domain Coded Value '%s' for %s Domain is incorrect." % (unicode(key),
                        unicode(gdb_domain.name))
                    if len(report) > 250:
                        report = report[0:249]
                    val = (today, report, "GDB", "Domain", "", "Check GDB Domains")
                    values.append(val)
                else:
                    index_key = correct_domain_sort.keys().index(unicode(key))
                    if value != correct_domain_sort.values()[index_key]:
                        if len(unicode(value)) > 25:
                            report_value_desc = unicode(value)[0:24]
                        else:
                            report_value_desc = unicode(value)
                        if len(unicode(correct_domain_sort.values()[index_key])) > 25:
                            report_corr_desc = unicode(correct_domain_sort.values()[index_key])[0:24]
                        else:
                            report_corr_desc = unicode(correct_domain_sort.values()[index_key])
                        report = "Error: Domain Coded Value Description '%s' for %s coded value in %s Domain is incorrect and should be '%s'." % (report_value_desc, unicode(key), unicode(gdb_domain.name), report_corr_desc)
                        if len(unicode(report)) > 250:
                            report = report[0:249]
                        val = (today, report, "GDB", "Domain", "", "Check GDB Domains")
                        values.append(val)

    if values != []:
        RecordResults(resultType, values, gdb)
        userWarning("Completed checking GDB domains: %s issues found. See table FieldValuesCheckResults for results." % (unicode(len(values))))
    else:
        userMessage("Completed checking GDB domains: 0 issues found")

    return len(values)

def checkSpatialReference(pathsInfoObject):
    # type: (NG911_Session_obj) -> None
    dataset = pathsInfoObject.gdbObject.NG911_FeatureDataset
    spatial_reference = Describe(dataset).spatialReference.factoryCode
    if spatial_reference == pathsInfoObject.gdbObject.ProjectionFile:
        debugMessage("Spatial reference of feature dataset is correct.")
    else:
        values = []
        resultType = "template"  # Indicate that results should go to TemplateCheckResults table
        today = strftime("%Y/%m/%d")
        report = "Error: Spatial reference of feature dataset is incorrect."
        # date, desc, cat, check
        values.append((today, report, "Spatial Reference", "Check Spatial Reference"))
        RecordResults(resultType, values, pathsInfoObject.gdbPath)
        userWarning(report)


def checkValuesAgainstDomain(pathsInfoObject):
    # type: (NG911_Session_obj) -> None
    gdb = pathsInfoObject.gdbPath  # type: str
    folder = pathsInfoObject.domainsFolderPath  # type: str
    fcList = pathsInfoObject.gdbObject.fcList  # type: List[str]
    requiredLayer = pathsInfoObject.gdbObject.requiredLayers # type: List[str]

    userMessage("Checking field values against approved domains...")
    #set up parameters to report duplicate records
    values = []
    resultType = "fieldValues"  # Indicate that results should go to FieldValuesCheckResults table
    today = strftime("%Y/%m/%d")

    #set environment
    env.workspace = gdb

    for fullPath in fcList:
        fc = basename(fullPath)
        if Exists(fullPath):
            obj = NG911_GDB_Objects.getFCObject(fullPath)

            #only check records marked for submission
            worked = 0
            fullPathlyr = "fullPathlyr"
            wc2 = "%s = 'Y'" % unicode(obj.SUBMIT)
            try:
                MakeTableView_management(fullPath, fullPathlyr, wc2)
                count = getFastCount(fullPathlyr)
                if count > 0:
                    worked = 1
                else:
                    userWarning("No features are marked for submission in %s. Please mark records for submission by placing Y in the %s field." % (fc, unicode(obj.SUBMIT)))
            except:
                userWarning("Cannot check required field values for %s because the %s field does not exist." % (fc, unicode(obj.SUBMIT)))

            if worked == 1:

                #get list of fields with domains
                fieldsWDoms = obj.FIELDS_WITH_DOMAINS

                id1 = obj.UNIQUEID
                # userMessage("---------------------------")
                userMessage("Checking " + fc + " layer.")
                if id1 != "":

                    for fieldN in fieldsWDoms.keys():
                        # get domain
                        domain = fieldsWDoms[fieldN]
                        # userMessage("Checking: " + fieldN)

                        #get the full domain dictionary
                        if fieldN != "Address": # Changed of OK Fields
                            domainDict = getFieldDomain(domain, folder)  # type: Dict[str, str] # e.g. { "CARTER COUNTY": "CARTER COUNTY", etc. }
                            if domainDict != {}:
                                #put domain values in a list
                                domainList = []

                                for val in domainDict.keys():
                                    domainList.append(val)

                                # #add values for some CAD users of blank and space (edit suggested by Sherry M. & Keith S. Dec 2014)
                                # if domain != "YESNO": # except if it's YN- it's two values. Fill it in.
                                #     domainList.append('')
                                #     domainList.append(" ")

                                #if the domain is counties, add county names to the list without "COUNTY" so both will work (edit suggest by Keith S. Dec 2014)
                                # if fieldN == "COUNTY":
                                #     q = len(domainList)  # Number of keys in domainDict
                                #     i = 0
                                #     while i < q:
                                #         # dl1 = domainList[i].split(" ")[0]
                                #         if domainList[i][:-7].upper() == " COUNTY":  # Sorry Louisiana
                                #             # If domainList[i] (in uppercase) ends in a space followed by "COUNTY", strip off last 7 characters to get just county name
                                #             dl1 = domainList[i][:-7]
                                #         else:
                                #             # Otherwise, nothing to strip; just use the value itself
                                #             dl1 = domainList[i]
                                #         domainList.append(dl1)
                                #         # ["CARTER", "CARTER COUNTY", "CLEVELAND", "CLEVELAND COUNTY", ...]
                                #         i += 1
                                if fieldExists(fullPath, fieldN):
                                    with SearchCursor(fullPathlyr, (id1, fieldN)) as rows:
                                        # try:
                                        for row in rows:
                                            # if the row is null, skip it
                                            # If the value is null, running check required field values will determine if that is okay or not
                                            if row[1] is None or row[1] in ['',' ']:
                                                pass
                                            # see if the value is in the domain list
                                            elif row[1] not in domainList:
                                                fID = row[0]
                                                report = "Error: Value %s not in approved domain for field %s" % (unicode(row[1]), fieldN)
                                                val = (today, report, fc, fieldN, fID, "Check Values Against Domains")
                                                values.append(val)
                                            del row
                                else:
                                    userWarning("Field %s in feature class %s does not exist, and its values cannot be checked against domain %s." % (fieldN, fc, domain))
                                    # except RuntimeError as e:
                                        # raise e
                                        # excinfo = sys.exc_info()
                                        # tb = extract_tb(excinfo[2])
                                        # arcpy.AddError(sys.exc_info())
                                        # arcpy.AddError(tb)
                                        # if "A column was specified that does not exist" in str(e):
                                        #     userMessage("    ")
                                        #     userMessage(fieldN + " or " + id1 + " may not exist or may be inccorect. Please check and try again.")
                                        #     userMessage("---------------------------")
                                        #     sys.exit(1)
                                        # else:
                                        #     userMessage(str(e))
                                        #     sys.exit(1)
                                    # except Exception as e:
                                        # raise e
                                        # excinfo = sys.exc_info()
                                        # tb = extract_tb(excinfo[2])
                                        # arcpy.AddError(sys.exc_info())
                                        # arcpy.AddError(tb)
                                        # userMessage(str(sys.exc_info()[1]))
                                        # sys.exit(1)

                        else: # fieldN == "Address"
                            # check Address field of address points to make sure all values are valid
                            with SearchCursor(fullPathlyr, (id1, fieldN)) as rows:
                                try:
                                    for row in rows:
                                        hno = row[1]
                                        if hno > 999999 or hno < 0:
                                            report = "Error: Value %s not in approved domain for field %s" % (unicode(row[1]), fieldN)
                                            val = (today, report, fc, fieldN, row[0], "Check Values Against Domains")
                                            values.append(val)
                                except RuntimeError as e:
                                    raise e
                                    # excinfo = sys.exc_info()
                                    # tb = extract_tb(excinfo[2])
                                    # arcpy.AddError(sys.exc_info())
                                    # arcpy.AddError(tb)
                                    # if "A column was specified that does not exist" in str(e):
                                    #     userMessage("    ")
                                    #     userMessage(fieldN + " or " + id1 + " may not exist or may be inccorect. Please check and try again.")
                                    #     userMessage("---------------------------")
                                    #     sys.exit(1)
                                    # else:
                                    #     userMessage(str(e))
                                    #     sys.exit(1)
                                except Exception as e:
                                    raise e
                                    # excinfo = sys.exc_info()
                                    # tb = extract_tb(excinfo[2])
                                    # arcpy.AddError(sys.exc_info())
                                    # arcpy.AddError(tb)
                                    # userMessage(str(sys.exc_info()[1]))
                                    # sys.exit(1)

                            del rows, row

                # userMessage("Checked " + fc)
                # userMessage("---------------------------")

            Delete_management(fullPathlyr)

            # make sure the parcel ID's go through testing for character length
            # if "PARCELS" in basename(fullPath).upper():
            #     checkOKPID(fullPath, "NGOKPID") # Change to OK Fields

        else:
            if fullPath in requiredLayer:
                userWarning("Required layer " + fc + " does not exist")
            else:
                userMessage("Optional layer " + fc + " does not exist")
            # userWarning(fullPath + " does not exist")

    if values != []:
        RecordResults(resultType, values, gdb)
        userWarning("Completed checking fields against domains: %s issues found. See table FieldValuesCheckResults for results." % (str(len(values))))
    else:
        userMessage("Completed checking fields against domains: 0 issues found")


def checkRequiredFieldValues(pathsInfoObject):
    gdb = pathsInfoObject.gdbPath
    fcList = pathsInfoObject.gdbObject.fcList
    requiredLayer = pathsInfoObject.gdbObject.requiredLayers

    userMessage("Checking that required fields have all values...")

    #get today's date
    today = strftime("%Y/%m/%d")

    values = []

    #walk through the tables/feature classes
    for filename in fcList:
        layer = basename(filename)
        if Exists(filename):
            obj = NG911_GDB_Objects.getFCObject(filename)
            id1 = obj.UNIQUEID

            if id1 != "":
                requiredFieldList = obj.REQUIRED_FIELDS

                #get list of fields in the feature class
                fields = ListFieldNames(filename)

                #convert lists to sets
                set1 = set(requiredFieldList)
                set2 = set(fields)

                #get the set of fields that are the same
                matchingFields = list(set1 & set2)

                #only work with records that are for submission
                lyr2 = "lyr2"
                worked = 0
                wc2 = "%s = 'Y'" % unicode(obj.SUBMIT)
                try:
                    MakeTableView_management(filename, lyr2, wc2)
                    worked = 1
                except:
                    userWarning("Cannot check required field values for " + layer)

                if worked == 1:

                    #get count of the results
                    if getFastCount(lyr2) > 0:

                        #create where clause to select any records where required values aren't populated
##                        wc = ""
                        wcList = []

                        for field in matchingFields:
                            wcList = wcList + [field, "is null", "or"]
##                            wc = wc + " " + field + " is null or "

                        wcList.pop() # take off the last " or "
##                        wc = wc[0:-4]
                        wc = " ".join(wcList)

                        #make table view using where clause
                        lyr = "lyr"
                        MakeTableView_management(lyr2, lyr, wc)

                        #if count is greater than 0, it means a required value somewhere isn't filled in
                        if getFastCount(lyr) > 0:
                            #make sure the objectID gets included in the search for reporting
                            if id1 not in matchingFields:
                                matchingFields.append(id1)

                            try:
                                #run a search cursor to get any/all records where a required field value is null
                                with SearchCursor(lyr, (matchingFields), wc) as rows:
                                    for row in rows:
                                        k = 0
                                        #get object ID of the field
                                        oid = unicode(row[matchingFields.index(id1)])

                                        #loop through row
                                        while k < len(matchingFields):
                                            #see if the value is nothing
                                            if row[k] is None:
                                                #report the value if it is indeed null
                                                report = "Error: %s is null for Feature ID %s" % (matchingFields[k], oid)
                                                # userMessage(report)
                                                val = (today, report, basename(filename), matchingFields[k], oid, "Check Required Field Values")
                                                values.append(val)

                                            #iterate!
                                            k = k + 1
                            except:
                                userWarning("Could not check all fields in %s. Looking for: %s" % (layer, ", ".join(matchingFields)))
                        else:
                            userMessage( "All required values present for " + layer)

                        Delete_management(lyr)
                        del lyr

                    else:
                        userWarning(layer + " has no records marked for submission. Data will not be verified.")
                    Delete_management(lyr2)
        else:
            if filename in requiredLayer:
                userWarning("Required layer " + layer + " does not exist")
            else:
                userMessage("Optional layer "+ layer + " does not exist")
            # userWarning(filename + " does not exist.")

    if values != []:
        RecordResults("fieldValues", values, gdb)
        userWarning("Completed check for required field values: %s issues found. See table FieldValuesCheckResults for results." % (str(len(values))))
    else:
        userMessage("Completed check for required field values: 0 issues found")



def checkRequiredFields(pathsInfoObject):
    gdb = pathsInfoObject.gdbPath
    fcList = pathsInfoObject.gdbObject.fcList
    requiredLayer = pathsInfoObject.gdbObject.requiredLayers

    userMessage("Checking that required fields exist...")

    #get today's date
    today = strftime("%Y/%m/%d")
    values = []

    #walk through the tables/feature classes
    for fullPath in fcList:
        filename = basename(fullPath)
        if Exists(fullPath):

            try:
                obj = NG911_GDB_Objects.getFCObject(fullPath)
                # userMessage(obj)
                comparisonList = obj.REQUIRED_FIELDS
            except:
                userWarning("No implementation for %s." % fullPath)
                continue

            #list fields
            fields = ListFieldNames(fullPath)

            # userMessage("Fields: %s" % set(fields))
            # userMessage("Comparison: %s" % set(comparisonList))

            missingFields = list(set(comparisonList) - set(fields))

            if missingFields != []:

                #loop through required fields to make sure they exist in the geodatabase
                for comparisonField in missingFields:
                    report = "Error: %s does not have required field %s" % (filename, comparisonField)
                    userWarning(report)
                    #add issue to list of values
                    val = (today, report, "Field", "Check Required Fields")
                    values.append(val)
        else:
            if fullPath in requiredLayer:
                userWarning("Required layer " + filename + " does not exist")
            else:
                userMessage("Optional layer "+ filename + " does not exist")

    if Exists(pathsInfoObject.gdbObject.AddressPoints):
        userMessage("Checking that the Address field is a number...")
        #test to see if the Address field is a number or text
        fc = pathsInfoObject.gdbObject.AddressPoints
        ap_fields = ListFields(fc)
        for ap_field in ap_fields:
            # if ap_field.name == "Address" and ap_field.type != "Integer":
            if ap_field.name == "Address" and ap_field.type != "Integer" and ap_field.type != "Double": # Changed to OK Fields
                report = "Error: HNO/Address field of Address Points is not an integer or a double, it is a %s" % ap_field.type
                userWarning(report)
                val = (today, report, "Field", "Check Required Fields")
                values.append(val)
    else:
        userWarning("Layer ADDRESS_POINT does not exist, and therefore its fields cannot be checked.")

    #record issues if any exist
    if values != []:
        RecordResults("template", values, gdb)
        userWarning("Completed check for required fields: %s issues found. See table FieldValuesCheckResults for results." % (str(len(values))))
    else:
        userMessage("Completed check for required fields: 0 issues found")


def checkSubmissionNumbers(pathsInfoObject):
    #set variables
    gdb = pathsInfoObject.gdbPath
    fcList = pathsInfoObject.gdbObject.fcList
    requiredLayer = pathsInfoObject.gdbObject.requiredLayers

    today = strftime("%Y/%m/%d")
    values = []

    skipList = ["HYDRANTS", "GATES", "PARCELS", "CELLSECTORS", "BRIDGES", "CELLSITES",
         "MUNICIPAL_BOUNDARY", "COUNTY_BOUNDARY"] # Changed to OK Fields/Layer

    for fc in fcList:
        base = basename(fc)
        if Exists(fc):
            #count records that are for submission
            lyr2 = "lyr2"
            wc2 = "SUBMIT = 'Y'"
            # arcpy.AddMessage(fc)
            # if "Address_Point" in fc: # Changed to OK Fields/Layer
            #     wc2 = wc2 + " AND LOCTYPE = 'PRIMARY'"
            if fieldExists(fc,"SUBMIT"):
                MakeTableView_management(fc, lyr2, wc2)
            else:
                if fc in requiredLayer:
                    userWarning("SUBMIT field does not exist in required layer " + base)
                else:
                    userMessage("SUBMIT field does not exist in optional layer " + base)
                # userMessage("SUBMIT field does not exist for %s" %base)
                continue

            #get count of the results
            count = getFastCount(lyr2)
            bn = basename(fc)

            umList = [bn, ": ", str(count), " records marked for submission"]
            um = "".join(umList)
            # userMessage(um)

            if count == 0:
                report = "Error: %s has 0 records for submission" % (bn)
                if bn.upper() in skipList or bn[0:3].upper() == 'UT_':
                    report = report.replace("Error", "Notice")
                #add issue to list of values
                val = (today, report, "Submission", "Check Submission Counts")
                values.append(val)

            Delete_management(lyr2)
        else:
            if fc in requiredLayer:
                userWarning("Required layer " + base + " does not exist")
            else:
                userMessage("Optional layer "+ base + " does not exist")
            # userWarning(fc + " does not exist")

    #record issues if any exist
    if values != []:
        RecordResults("template", values, gdb)
        userWarning("One or more layers had no features to submit. See table TemplateCheckResults.")
    else:
        userMessage("All layers had features to submit.")

def checkFeatureLocations(pathsInfoObject):
    # NOTE: In Oklahoma, "authoritative boundary" generally refers to DISCREPANCYAGENCY_BOUNDARY (as of 6/10/2022)
    gdb = pathsInfoObject.gdbPath
    fcList = pathsInfoObject.gdbObject.fcList

    #get geodatabase object
    gdbObject = pathsInfoObject.gdbObject

    RoadAlias = gdbObject.RoadAlias
    if RoadAlias in fcList:
        fcList.remove(RoadAlias)

    userMessage("Checking feature locations...")

    #get today's date
    today = strftime("%Y/%m/%d")
    values = []

    #make sure features are all inside authoritative boundary

    #get authoritative boundary
    authBound = gdbObject.AuthoritativeBoundary
    countyBound = gdbObject.CountyBoundary
    parcels = gdbObject.PARCELS
    ab = "ab"
    addedField = 0

    #see if authoritative boundary has more than 1 feature
    #if more than one feature is in the authoritative boundary, use the county boundary instead
    if Exists(authBound):
        # DisableEditorTracking_management(authBound)
        if getFastCount(authBound) > 1:
            if Exists(countyBound):
                authBound = countyBound
            else:
                # see if the STATE field exists to dissolve features
                if not fieldExists(authBound, "STATE"):

                    # if not, add the field
                    AddField_management(authBound, "STATE", "TEXT", "", "", 2)
                    CalculateField_management(authBound, "STATE", '"OK"', "PYTHON_9.3", "")
                    addedField = 1 # toggle flag

                # set up to dissolve features on STATE into an in-memory layer
                auth = "auth"
                MakeFeatureLayer_management(authBound, auth)
                authBound = r"in_memory\Auth"

                Dissolve_management(auth, authBound, ["STATE"])

    elif Exists(countyBound):
            authBound = countyBound

    else:
        userWarning("Check Feature Locations could not run because the discrepancy agency and/or county boundary feature classes are absent or misnamed.")
        return

    #remove some layers from being checked
    for f in [authBound, countyBound, parcels]:
        if f in fcList:
            fcList.remove(f)

    MakeFeatureLayer_management(authBound, ab)

    for fullPath in fcList:
        fc_obj = NG911_GDB_Objects.getFCObject(fullPath)  # type: NG911_GDB_Objects.NG911FeatureClassObject

        if Exists(fullPath):
            fl = "fl"
            wcList = ["%s = 'Y'" % fc_obj.SUBMIT]
            rule = "WITHIN"
            if "ROAD_CENTERLINE" in fullPath: # Changed to OK Fields/Layer
                # Getting feature class object below is redundant,
                # but tells code analyzer that fc_obj will have a TopoExcept attribute.
                # Expected performance impact is imperceptible.
                fc_obj = NG911_GDB_Objects.getFCObject(fullPath)  # type: NG911_GDB_Objects.NG911_RoadCenterline_Object
                wcList = wcList + [" AND ", fc_obj.TopoExcept, " not in ('INSIDE_EXCEPTION', 'BOTH_EXCEPTION')"]
            elif "ADDRESS_POINT" in fullPath:
                rule = "COMPLETELY_WITHIN"
                # TODO: When TopoExcept added to ADDRESS_POINT, add logic similar to above!
                # Getting feature class object below is redundant,
                # but tells code analyzer that fc_obj will have a TopoExcept attribute.
                # Expected performance impact is imperceptible.
                # fc_obj = NG911_GDB_Objects.getFCObject(fullPath)  # type: NG911_GDB_Objects.NG911_Address_Object
            wc = "".join(wcList)
            MakeFeatureLayer_management(fullPath, fl, wc)

            try:
                #select by location to get count of features outside the authoritative boundary
                SelectLayerByLocation_management(fl, rule, ab)
                SelectLayerByAttribute_management(fl, "SWITCH_SELECTION", "")

                #get count of selected records
                #report results
                if getFastCount(fl) > 0:
                    layer = basename(fullPath)
                    if fc_obj.UNIQUEID != '':
                        fields = (fc_obj.UNIQUEID, )  # type: Tuple
                        # if "Address_Point" in fullPath: # Changed to OK Fields/Layer
                        #     fields = (obj.UNIQUEID, obj.LOCTYPE)
                        with SearchCursor(fl, fields) as rows:
                            for row in rows:
                                fID = row[0]
                                report = "Error: Feature not inside discrepancy agency boundary"
                                # if "Address_Point" in fullPath: # Changed to OK Fields/Layer
                                #     if row[1] != 'PRIMARY':
                                #         report = report.replace("Error:", "Notice:")

                                val = (today, report, layer, " ", fID, "Check Feature Locations")
                                values.append(val)

                        userWarning(basename(fullPath) + ": issues with some feature locations")
                    else:
                        userWarning("Could not process features in " + fullPath + " because unique ID is empty.")
                else:
                    userMessage(basename(fullPath) + ": all records inside discrepancy agency boundary")
            except:
                userWarning("Could not check locations of " + fullPath)

            finally:

                #clean up
                Delete_management(fl)

    if values != []:
        RecordResults("fieldValues", values, gdb)
        userWarning("Completed check on feature locations: %s issues found. See table FieldValuesCheckResults." % (str(len(values))))
    else:
        userMessage("Completed check on feature locations: 0 issues found")

    # clean up if various methods were used
    if authBound == r"in_memory\Auth":
        Delete_management(authBound)
    if addedField == 1:
        try:
            DeleteField_management(gdbObject.AuthoritativeBoundary, "STATE")
        except:
            pass

    # re-enable editor tracking
    # EnableEditorTracking_management(gdbObject.AuthoritativeBoundary, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields

def findInvalidGeometry(pathsInfoObject):
    userMessage("Checking for invalid geometry...")

    #set variables
    gdb = pathsInfoObject.gdbPath
    gdbObject = pathsInfoObject.gdbObject
    fcList = gdbObject.fcList
    requiredLayer = pathsInfoObject.gdbObject.requiredLayers

    for f in fcList:
        if "Road_Alias" in f: # Changed to OK Fields/Layer
            fcList.remove(f)

    today = strftime("%Y/%m/%d")
    values = []
    report = "Error: Invalid geometry"

    invalidDict = {"point": 1, "polyline": 2, "polygon":3}

    #loop through feature classes
    for fullPath in fcList:
        layer = basename(fullPath)

        if Exists(fullPath):
            obj = NG911_GDB_Objects.getFCObject(fullPath)
            id_column = obj.UNIQUEID

            if fieldExists(fullPath, id_column):

                #set up fields for cursor
                fields = ("SHAPE@", id_column)

                with SearchCursor(fullPath, fields) as rows:
                    for row in rows:
                        geom = row[0]
                        fid = row[1]

                        try:
                            #get geometry type
                            geomType = geom.type

                            #find the minimum number of required points
                            minNum = invalidDict[geomType]

                            #get the count of points in the geometry
                            count = geom.pointCount

                            #if the count is smaller than the minimum number, there's a problem
                            if count < minNum:
                                val = (today, report, layer, " ", fid, "Find Invalid Geometry")
                                values.append(val)
                        except:
                            #if this errors, there's an error accessing the geometry, hence problems
                            val = (today, report, layer, " ", fid, "Find Invalid Geometry")
                            values.append(val)

            else:
                userWarning("NGUID field %s does not exist in %s" % (id_column, layer))

        else:
            if fullPath in requiredLayer:
                userWarning("Required layer " + layer + " does not exist")
            else:
                userMessage("Optional layer "+ layer + " does not exist")
            # userWarning(fullPath + " does not exist")

    if values != []:
        RecordResults("fieldValues", values, gdb)
        userWarning("Completed for invalid geometry: %s issues found. See FieldValuesCheckResults." % (str(len(values))))
    else:
        userMessage("Completed for invalid geometry: 0 issues found")

def checkCutbacks(pathsInfoObject):
    """
    Searches road centerline line features (containing more than 4 points) for sharp angles (cutbacks), defined in this
    case as on the interval (0, 55) degrees. Generates notices if any are found.

    Parameters
    ----------
    pathsInfoObject : NG911_Session_obj
        See class documentation
    """
    userMessage("Checking for geometry cutbacks...")

    gdb = pathsInfoObject.gdbPath
    gdbObject = pathsInfoObject.gdbObject
    road_fc = gdbObject.RoadCenterline
    roads = "roads"
    rc_obj = NG911_GDB_Objects.getFCObject(road_fc)

    if Exists(road_fc):

        #make feature layer so only roads marked for submission are checked
        MakeFeatureLayer_management(road_fc, roads, rc_obj.SUBMIT + " = 'Y'")

        #set up tracking variables
        cutbacks = []
        values = []
        today = strftime("%Y/%m/%d")
        layer = "ROAD_CENTERLINE"

        k = 0

        #set up search cursor on roads layer
        with SearchCursor(roads, ("SHAPE@", rc_obj.UNIQUEID)) as rows:
            for row in rows:
                geom = row[0]
                segid = row[1]

                try:

                    #loop through geometry parts
                    for part in geom:
                        part_coords = []

                        #don't check simple roads
                        # TODO: Determine whether or not this should be reduced to >= 3 based on execution time
                        if len(part) > 4:
                            #loop through points
                            for pnt in part:
                                #set up points in a straightforward list
                                pc = []
                                if pnt:
                                    pc = [pnt.X, pnt.Y]
                                    part_coords.append(pc)
                                else:
                                    pass

                            #loop through coordinate list
                            if part_coords != []:
                                i = 1
                                while i < (len(part_coords)-1):

                                    #calculate the angle between three points
                                    angle = calcAngle(part_coords[i-1],part_coords[i],part_coords[i+1])
        ##                            print angle

                                    #if the angle is quite sharp, it might indicate a cutback
                                    if 0 < angle < 55:
                                        if segid not in cutbacks:
                                            report = "Notice: This segment might contain a geometry cutback."
                                            val = (today, report, layer, " ", segid, "Check for Cutbacks")
                                            values.append(val)
                                            cutbacks.append(segid)
                                    i += 1
                except Exception as e:
                    userMessage(unicode(e))
                    userMessage("Issue checking a cutback with segment " + segid)
                    k += 1

        Delete_management(roads)
    else:
        userWarning(road_fc + " does not exist")

    if values != []:
        RecordResults("fieldValues", values, gdb)
        userWarning("Completed check on cutbacks: %s issues found. See FieldValuesCheckResults." % (str(len(values))))
    else:
        userMessage("Completed check on cutbacks: 0 issues found")

    if k != 0:
        userMessage("Could not complete cutback check on %s segments." % (str(k)))


# def getNumbers():
#     numbers = "0123456789"
#     return numbers


def checkOKPID(fc, field):
    # make sure the OKPID value is 19 characters long
    values = []
    okpid_wc = "%s is not null and CHAR_LENGTH(%s) <> 19" % (field, field)
##    okpid_wc = "NGOKPID is not null and CHAR_LENGTH(NGOKPID) <> 19"
    userMessage(fc + " " + field + " " + okpid_wc)
    okpid_fl = "okpid_fl"
    MakeFeatureLayer_management(fc, okpid_fl, okpid_wc)

    # get the count of how many are too long or short
    if getFastCount(okpid_fl) > 0:
        today = strftime("%Y/%m/%d")
        layer = basename(fc)
        if layer == "AddressPoints":
            fields = (field, "NGADDID")
            ID_index = 1
        else:
            fields = (field)
            ID_index = 0

        with SearchCursor(okpid_fl, fields, okpid_wc) as rows:
            for row in rows:
                if layer == "ADDRESS_POINT": # Changed to OK Fields/Layer
                    # try to make sure we're not getting any blanks reported in Address Points
                    if row[0] not in ('', ' '):
                        fid = row[ID_index]
                        report = "Error: %s value is not the required 19 characters." % (field)
                        val = (today, report, layer, field, fid, "Check " + field)
                        values.append(val)

                else:
                    fid = row[ID_index]
                    report = "Error: %s value is not the required 19 characters." % (field)
                    val = (today, report, layer, field, fid, "Check " + field)
                    values.append(val)

    # report
    msgList = ["Completed check on ", basename(fc), " ", field, ": "]
    if values != []:
        if dirname(fc)[-3:] != 'gdb':
            gdb = dirname(dirname(fc))
        else:
            gdb = dirname(fc)
        RecordResults("fieldValues", values, gdb)
        msgList = msgList + [str(len(values)), " issues found. See FieldValuesCheckResults. Parcel IDs must be 19 digits with county code and no dots or dashes."]
        msg = "".join(msgList)
        userWarning(msg)
    else:
        msgList.append("0 issues found")
        msg = "".join(msgList)
        userMessage(msg)

    Delete_management(okpid_fl)


def checkJoin(gdb, inputTable, joinTable, where_clause, errorMessage, field):
    #set up tracking variables
    values = []
    today = strftime("%Y/%m/%d")
    layer = field.split(".")[0]
    recordType = "fieldValues"
    rc_obj = NG911_GDB_Objects.getFCObject(join(gdb, "NG911", "ROAD_CENTERLINE")) # Changed to OK Fields/Layer

    AddJoin_management(inputTable, rc_obj.UNIQUEID, joinTable, rc_obj.UNIQUEID)
    tbl = "tbl"

    #get the fast count to see if issues exist
    MakeTableView_management(inputTable, tbl, where_clause)

    #see if any issues exist
    #catalog issues
    if getFastCount(tbl) > 0:
        fields = (field, "ROAD_CENTERLINE." + rc_obj.Street) # Changed to OK Fields/Layer
        #NOTE: have to run the search cursor on the join table, running it on the table view throws an error
        with SearchCursor(inputTable, fields, where_clause) as rows:
            for row in rows:
                if row[1] is not None:
                    if " TO " in row[1] or "RAMP" in row[1] or "OLD" in row[1]:
                        #print("this is probably an exception")
                        pass
                    else:
                        val = (today, errorMessage, layer, "", row[0], "Check Road Alias")
                        values.append(val)

    #clean up
    RemoveJoin_management(inputTable)
    Delete_management(tbl)

    #report records
    if values != []:
        RecordResults(recordType, values, gdb)

    valCount = len(values)

    return valCount


# def checkESBDisplayLength(pathsInfoObject):
#     userMessage("Checking ESB DISPLAY field length...")
#     esbList = pathsInfoObject.gdbObject.esbList
#
#     #set variables for working with the data
#     gdb = pathsInfoObject.gdbObject.gdbPath
#     recordType = "fieldValues"
#     field = "DISPLAY"
#     today = strftime("%m/%d/%y")
#     values = []
#
#     for esb in esbList:
#         fc = basename(esb)
#         if fieldExists(esb, "DISPLAY"):
#             e = "e"
#             wc = "CHAR_LENGTH(DISPLAY) > 32"
#             MakeFeatureLayer_management(esb, e, wc)
#
#             if getFastCount(e) > 0:
#                 with SearchCursor(e, ("NGESBID")) as rows:
#                     for row in rows:
#                         msg = "Notice: DISPLAY length longer than 32 characters, value will be truncated"
#                         val = (today, msg, fc, field, row[0], "Check ESB DISPLAY length")
#                         values.append(val)
#             Delete_management(e)
#
#     if values != []:
#         RecordResults(recordType, values, gdb)
#         userWarning("Checked ESB DISPLAY length. There were %s issues." % str(len(values)))
#     else:
#         userMessage("Checked ESB DISPLAY length. No issues found.")


def checkTopology(gdbObject, check_polygons, check_roads):



    userMessage("Validating topology...")

    # set variables for working with the data
    gdb = gdbObject.gdbPath
    featureDataset = gdbObject.NG911_FeatureDataset
    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")
    values = []
    count = 0

    # export topology errors as feature class
    topology = gdbObject.Topology

    # make sure topology is all set up correctly & validate
    if not Exists(topology):
        userMessage("Function checkTopology: Topology does not already exist; will be created.")
        add_topology(gdb, "true")
    else:
        userMessage("Function checkTopology: Topology already exists; will be deleted and recreated.")
        Delete_management(topology)
        add_topology(gdb, "true")
    # userWarning("==== RECREATE TOPO TURNED OFF ====")

    out_basename = "NG911_Topology"
    polyErrors = "%s_poly" % out_basename
    lineErrors = "%s_line" % out_basename
    pointErrors = "%s_point" % out_basename

    if Exists(topology):
        for topE in (lineErrors, pointErrors, polyErrors):
            full = join(gdb, topE)  # Changed to OK Standards
            if Exists(full):
                Delete_management(full)

        # export topology
        userMessage("Exporting topology errors...")
        ExportTopologyErrors_management(topology, gdb, out_basename)  # Changed to OK Standards

        # query the polygon results for issues
        polyFC = join(gdb, polyErrors)
        lineFC = join(gdb, lineErrors)
        pointFC = join(gdb, pointErrors)

        error_fields = ["OriginObjectClassName", "OriginObjectID", "RuleDescription", "DestinationObjectClassName", "DestinationObjectID", "SHAPE@LENGTH"]

        error_list = [polyFC, lineFC, pointFC]

        dual_rule_list = set()
        for errorFC in error_list:
            for row in SearchCursor(errorFC, error_fields):
                if row[0] not in [None, "", " "] and row[3] not in [None, "", " "]:
                    # userMessage("Added '%s' rule to list for %s error FC" % (row[2], basename(errorFC)))
                    dual_rule_list.add(row[2])

        # set up exception definition dictionary
        exc_dict = {"INSIDE_EXCEPTION": ["Must Be Inside"],
                    "DANGLE_EXCEPTION": ["Must Not Have Dangles"],
                    "BOTH_EXCEPTION": ["Must Be Inside", "Must Not Have Dangles"]}

        # rules that require a summation for error exporting
        sum_rule = ["Must Cover Each Other", "Must Not Have Gaps", "Must Not Have Dangles", "Must Not Overlap", "Must Not Self-Intersect"]

        returned_error_list = []
        already_checked = []

        for error_fc_path in error_list:
            error_fc_name = basename(error_fc_path)


            # remove any in_topology exceptions
            wc_no_except = "isException = 0"
            error_fl = "error_fl"
            deleteExisting(error_fl)
            MakeFeatureLayer_management(error_fc_path, error_fl, wc_no_except)

            # get overall count of errors
            k = getFastCount(error_fl)
            if k > 0:
                with SearchCursor(error_fl, error_fields) as rows:
                    # topo_rec = [val for val in SearchCursor(lyr, fields)]
                    # topo_len = len(topo_rec)
                    # SetProgressor("step", "Beginning export of topology errors for polygons, polylines, and points...", 0, topo_len, 1)
                    for row in rows:

                        dual_rule_switch = False

                        origin_fc = row[0]
                        origin_id = row[1]
                        ruleDesc = row[2]
                        destination_fc = row[3]
                        destination_id = row[4]
                        error_length = row[5]

                        origin_id_field_name = "OriginObjectID"
                        destination_id_field_name = "DestinationObjectID"

                        if origin_fc not in [None, "", " "] and destination_fc not in [None, "", " "]:
                            if (ruleDesc, destination_fc, origin_fc) in already_checked or (ruleDesc, origin_fc, destination_fc) in already_checked:
                                debugMessage("SKIPPED %s; already collected information about rule, origin, and destination combination." % unicode(" and ".join([ruleDesc, origin_fc, destination_fc])))
                                continue
                            else:
                                already_checked.append((ruleDesc, origin_fc, destination_fc))
                        elif origin_fc in [None, "", " "] and destination_fc not in [None, "", " "]:
                            origin_fc = ""
                            origin_id = ""
                            if (ruleDesc, destination_fc, origin_fc) in already_checked:
                                debugMessage("SKIPPED %s; already collected information about rule, origin, and destination combination." % unicode(" and ".join([ruleDesc, destination_fc, "No Origin FC"])))
                                continue
                            else:
                                already_checked.append((ruleDesc, destination_fc, origin_fc))
                        elif origin_fc not in [None, "", " "] and destination_fc in [None, "", " "]:
                            destination_fc = ""
                            destination_id = ""
                            if (ruleDesc, origin_fc, destination_fc) in already_checked:
                                debugMessage("SKIPPED %s; already collected information about rule, origin, and destination combination." % unicode(" and ".join([ruleDesc, origin_fc, "No Destination FC"])))
                                continue
                            else:
                                already_checked.append((ruleDesc, origin_fc, destination_fc))


                        if origin_fc not in (None, "", " ") and destination_fc not in (None, "", " "):

                            # if (ruleDesc, origin_fc, origin_id, destination_fc, destination_id) in already_checked:
                            #     continue
                            #
                            # already_checked.append((ruleDesc, origin_fc, origin_id, destination_fc, destination_id))

                            debugMessage("%s Topo, Feature Classes: %s, %s | %s" % (error_fc_name, origin_fc, destination_fc, ruleDesc))

                            # grab appropriate parameters
                            lyr_rule = "lyr_rule"
                            fc_lyr_origin = "fc_lyr_origin"
                            fc_lyr_origin_path = join("in_memory", fc_lyr_origin)
                            fc_full_origin = join(featureDataset, origin_fc)
                            origin_obj = NG911_GDB_Objects.getFCObject(fc_full_origin)
                            fc_lyr_destination = "fc_lyr_destination"
                            fc_lyr_destination_path = join("in_memory", fc_lyr_destination)
                            fc_full_destination = join(featureDataset, destination_fc)
                            destination_obj = NG911_GDB_Objects.getFCObject(fc_full_destination)

                            wc = "RuleDescription = '%s'" % (ruleDesc)
                            MakeFeatureLayer_management(error_fl, lyr_rule, wc)

                            # origin FL
                            deleteExisting(fc_lyr_origin_path)
                            FeatureClassToFeatureClass_conversion(fc_full_origin, "in_memory", "%s" % fc_lyr_origin)
                            AddField_management(fc_lyr_origin_path, "RecordID", "DOUBLE")
                            deleteExisting("origin_fc_table")
                            MakeTableView_management(fc_lyr_origin_path, "origin_fc_table")
                            AddJoin_management("origin_fc_table", origin_obj.UNIQUEID, fc_full_origin, origin_obj.UNIQUEID)
                            CalculateField_management("origin_fc_table", "%s.RecordID" % fc_lyr_origin, "!%s.OBJECTID!" % origin_fc, "PYTHON")
                            RemoveJoin_management("origin_fc_table")

                            origin_table_view = "origin_table"
                            deleteExisting(origin_table_view)
                            MakeTableView_management(fc_lyr_origin_path, origin_table_view)

                            # destination FL
                            deleteExisting(fc_lyr_destination_path)
                            FeatureClassToFeatureClass_conversion(fc_full_destination, "in_memory", fc_lyr_destination)
                            AddField_management(fc_lyr_destination_path, "RecordID", "DOUBLE")
                            deleteExisting("destination_fc_table")
                            MakeTableView_management(fc_lyr_destination_path, "destination_fc_table")
                            AddJoin_management("destination_fc_table", destination_obj.UNIQUEID, fc_full_destination, destination_obj.UNIQUEID)
                            CalculateField_management("destination_fc_table", "%s.RecordID" % fc_lyr_destination, "!%s.OBJECTID!" % destination_fc, "PYTHON")
                            RemoveJoin_management("destination_fc_table")
                            destination_table_view = "destination_table"
                            deleteExisting(destination_table_view)
                            MakeTableView_management(fc_lyr_destination_path, destination_table_view)

                            # joins FLs to error FL
                            AddJoin_management(lyr_rule, origin_id_field_name, origin_table_view, "RecordID")
                            AddJoin_management(lyr_rule, destination_id_field_name, destination_table_view, "RecordID")

                            qry = "%s.%s IS NOT NULL and %s.isException = 0 and %s.%s = 'Y'" % (fc_lyr_origin, origin_obj.UNIQUEID, error_fc_name, fc_lyr_origin, origin_obj.SUBMIT)
                            qry += " and %s.%s IS NOT NULL and %s.%s = 'Y'" % (fc_lyr_destination, destination_obj.UNIQUEID, fc_lyr_destination, destination_obj.SUBMIT)
                            fields = ["%s.%s" % (fc_lyr_origin, origin_obj.UNIQUEID), "%s.%s" % (fc_lyr_destination, destination_obj.UNIQUEID), error_fc_name + ".RuleDescription", error_fc_name + ".isException"]
                            if "ROAD" in origin_fc:
                                fields.append("%s.%s" % (fc_lyr_origin, origin_obj.TopoExcept))
                                origin_topo_skip = False
                            else:
                                origin_topo_skip = True

                            if "ROAD" in destination_fc:
                                fields.append("%s.%s" % (fc_lyr_destination, destination_obj.TopoExcept))
                                destination_topo_skip = False
                            else:
                                destination_topo_skip = True

                            # TODO: Add "ADDRESS" to topo_skip analysis

                            # get all unique_ID associated with a given rule
                            for row in SearchCursor(lyr_rule, fields, qry):
                                row_origin_id = row[0]
                                row_destination_id = row[1]
                                row_rule = row[2]
                                row_is_exception = row[3]

                                if not origin_topo_skip and not destination_topo_skip:
                                    row_origin_topoexcept = row[4]
                                    row_destination_topoexcept = row[5]
                                elif origin_topo_skip and not destination_topo_skip:
                                    row_origin_topoexcept = "SKIP"
                                    row_destination_topoexcept = row[4]
                                elif not origin_topo_skip and destination_topo_skip:
                                    row_origin_topoexcept = row[4]
                                    row_destination_topoexcept = "SKIP"
                                else:
                                    row_origin_topoexcept = "SKIP"
                                    row_destination_topoexcept = "SKIP"

                                except_in_effect = False
                                # if len(fields) >= 5:
                                for topo_except, rule_list in exc_dict.items():
                                    if row_rule in rule_list:
                                        if row_origin_topoexcept == topo_except or row_destination_topoexcept == topo_except:
                                            except_in_effect = True

                                if except_in_effect:
                                    continue
                                else:
                                    if (row_rule, destination_fc, row_destination_id, origin_fc, row_origin_id) in returned_error_list:
                                        returned_error_list.append((row_rule, destination_fc, row_destination_id, origin_fc, row_origin_id))
                                    else:
                                        returned_error_list.append((row_rule, origin_fc, row_origin_id, destination_fc, row_destination_id))

                            # clean up & reset
                            RemoveJoin_management(lyr_rule)
                            try:
                                RemoveJoin_management(lyr_rule)
                                debugMessage("===== REMOVE JOIN TWICE! =====")
                            except:
                                debugMessage("===== REMOVE JOIN ONLY ONCE! =====")
                            Delete_management(fc_lyr_origin_path)
                            Delete_management(fc_lyr_destination_path)
                            Delete_management(lyr_rule)

                        else:
                            if origin_fc in [None, "", " "]:
                                fc = destination_fc
                                id = destination_id
                                id_field_name = destination_id_field_name
                            elif destination_fc in [None, "", " "]:
                                fc = origin_fc
                                id = origin_id
                                id_field_name = origin_id_field_name
                            else:
                                val = (today, "Error: Both origin and destination feature class names are null.", "", "", "", "Check Topology")
                                values.append(val)
                                userWarning(val[1])

                            # if (ruleDesc, fc, "") in already_checked:
                            #     continue
                            #
                            # already_checked.append((ruleDesc, fc, ""))

                            debugMessage("%s Topo, Feature Classes: %s | %s" % (error_fc_name, fc, ruleDesc))

                            wc = "RuleDescription = '%s'" % (ruleDesc)
                            lyr_rule = "lyr_rule"
                            MakeFeatureLayer_management(error_fl, lyr_rule, wc)

                            # fc FL
                            fc_lyr = "fc_lyr"
                            fc_full = join(featureDataset, fc)
                            MakeFeatureLayer_management(fc_full, fc_lyr)

                            # joins FL to error FL
                            AddJoin_management(lyr_rule, id_field_name, fc_lyr, "OBJECTID")

                            # grab appropriate objects
                            fc_obj = NG911_GDB_Objects.getFCObject(fc_full)

                            qry = "%s.%s IS NOT NULL and %s.isException = 0 and %s.%s = 'Y'" % (fc, fc_obj.UNIQUEID, error_fc_name, fc, fc_obj.SUBMIT)

                            fields = ["%s.%s" % (fc, fc_obj.UNIQUEID),
                                      error_fc_name + ".RuleDescription",
                                      error_fc_name + ".isException"]

                            if "ROAD" in fc:
                                fields.append("%s.%s" % (fc, fc_obj.TopoExcept))
                                topo_skip = False
                            else:
                                topo_skip = True

                            for row in SearchCursor(lyr_rule, fields, qry):
                                row_id = row[0]
                                row_rule = row[1]
                                row_is_exception = row[2]

                                if not topo_skip:
                                    row_topoexcept = row[3]
                                else:
                                    row_topoexcept = "SKIP"

                                except_in_effect = False
                                for topo_except, rule_list in exc_dict.items():
                                    if row_rule in rule_list:
                                        if row_topoexcept == topo_except:
                                            except_in_effect = True

                                if except_in_effect:
                                    continue
                                else:
                                    returned_error_list.append((row_rule, fc, row_id, "", ""))

                            # clean up & reset
                            RemoveJoin_management(lyr_rule)
                            Delete_management(fc_lyr)
                            Delete_management(lyr_rule)



        #  [(rule, origin_fc, row_origin_id, destination_fc, row_destination_id)]
        if len(returned_error_list) > 0:
            unique_count = Counter(returned_error_list)
            for keys, count in unique_count.items():
                rule = keys[0]
                result_fc_1 = keys[1]
                result_id_1 = keys[2]
                result_fc_2 = keys[3]
                result_id_2 = keys[4]

                if result_fc_2 == "":
                    fc_string = result_fc_1
                    id_string = result_id_1
                else:
                    fc_1 = result_fc_1[:20] if len(result_fc_1) > 20 else result_fc_1
                    fc_2 = result_fc_2[:20] if len(result_fc_2) > 20 else result_fc_2
                    fc_string = "%s | %s" % (fc_1, fc_2)
                    id_1 = result_id_1[:99] if len(result_id_1) > 99 else result_id_1
                    id_2 = result_id_2[:99] if len(result_id_2) > 99 else result_id_2
                    id_string = "%s | %s" % (id_1, id_2)

                msg = "Error: Topology issue- %s | Number of errors- %s" % (rule, unicode(count))

                val = (today, msg, fc_string, "", id_string, "Check Topology")
                values.append(val)

        # report records
        count = 0
        if values != []:
            count = len(values)
            RecordResults(recordType, values, gdb)

        # give the user some feedback
        warning = False
        messageList = ["Topology check complete.", str(count), "issues found."]
        if count > 0:
            messageList.append("Results in FieldValuesCheckResults.")
            warning = True
        elif count == 0:
            # clean up topology export if there were no errors
            for topE in (lineErrors, pointErrors, polyErrors):
                full = join(gdb, topE)
                if Exists(full):
                    Delete_management(full)

        message = " ".join(messageList)
        if warning:
            userWarning(message)
        else:
            userMessage(message)

                            # SetProgressorPosition()
                            # SetProgressorLabel("Checking %s to export errors..." % fc)


def checkTopology_KS(gdbObject, check_polygons, check_roads):
    # type: (__NG911_GDB_Object, bool, bool) -> None
    """
    Generates and validates topology rules on appropriate feature classes, then reports errors.

    Parameters
    ----------
    gdbObject : __NG911_GDB_Object
        The GDB object
    check_polygons : bool
        Flag indicating whether or not polygon feature classes should be checked
    check_roads : bool
        Flag indicating whether or not the road centerline feature class should be checked
    """
    userMessage("Validating topology...")

    #set variables for working with the data
    gdb = gdbObject.gdbPath
    featureDataset = gdbObject.NG911_FeatureDataset
    recordType = "fieldValues"
    today = strftime("%Y/%m/%d")
    values = []
    count = 0

    #export topology errors as feature class
    topology = gdbObject.Topology

    # make sure topology is all set up correctly & validate
    if not Exists(topology):
        userMessage("Function checkTopology: Topology does not already exist; will be created.")
        add_topology(gdb, "true")
    else:
        userMessage("Function checkTopology: Topology already exists; will be deleted and recreated.")
        Delete_management(topology)
        add_topology(gdb, "true")

    out_basename = "NG911_Topology"
    polyErrors = "%s_poly" % out_basename
    lineErrors = "%s_line" % out_basename
    pointErrors = "%s_point" % out_basename

    if Exists(topology):
        for topE in (lineErrors, pointErrors, polyErrors):
            full = join(gdb, topE) # Changed to OK Standards
            if Exists(full):
                Delete_management(full)

        # export topology
        userMessage("Exporting topology errors...")
        ExportTopologyErrors_management(topology, gdb, out_basename) # Changed to OK Standards

        # query the polygon results for issues
        polyFC = join(gdb, polyErrors)
        lineFC = join(gdb, lineErrors)
        pointFC = join(gdb, pointErrors)

        # create a dictionary of the counts
        fcIssueDict = {}

        top_fields = ["OriginObjectClassName", "OriginObjectID", "RuleDescription"]
        top_fields_line = ["OriginObjectClassName", "OriginObjectID", "RuleDescription", "SHAPE@LENGTH"]
        top_fields_poly = ["OriginObjectClassName", "OriginObjectID", "RuleDescription", "DestinationObjectClassName", "DestinationObjectID"]

        top_dict = {polyFC: top_fields_poly, lineFC: top_fields_line, pointFC: top_fields}

        # make a list of all of the exceptions in road attributes so these aren't reported
        roads = gdbObject.RoadCenterline
        rd_object = NG911_GDB_Objects.getFCObject(roads)
        wc = rd_object.TopoExcept + " <> 'NO_EXCEPTION'"
        rd_exceptions = {}
        with SearchCursor(roads, ("OBJECTID", rd_object.TopoExcept), wc) as rows:
            for row in rows:
                rd_exceptions[row[0]] = row[1]

        # make a list of all of the exceptions in address attributes so these aren't reported
        addresses = gdbObject.AddressPoints
        ap_object = NG911_GDB_Objects.getFCObject(addresses)
        # TODO: Re-enable below lines when/if Address_Point receives a TopoExcept field
        # wc = ap_object.TopoExcept + " <> 'NO_EXCEPTION'"
        # ap_exceptions = {}
        # with SearchCursor(addresses, ("OBJECTID", ap_object.TopoExcept), wc) as rows:
        #     for row in rows:
        #         ap_exceptions[row[0]] = row[1]

        # set up exception definition dictionary
        exc_dict = {"INSIDE_EXCEPTION": ["Must Be Inside"],
                    "DANGLE_EXCEPTION": ["Must Not Have Dangles"],
                    "BOTH_EXCEPTION": ["Must Be Inside", "Must Not Have Dangles"]}

        # rules that require a summation for error exporting
        sum_rule = ["Must Cover Each Other", "Must Not Have Gaps", "Must Not Have Dangles", "Must Not Overlap", "Must Not Self-Intersect"]

        dual_rule_list = set()
        for errorFC in top_dict:
            fields = top_fields_poly
            for row in SearchCursor(errorFC, fields):
                if row[0] not in [None, "", " "] and row[3] not in [None, "", " "]:
                    userMessage("Added '%s' rule to list for %s error FC" % (row[2], basename(errorFC)))
                    dual_rule_list.add(row[2])

        # loop through polygon and line errors
        for errorFC in top_dict:
            fields = top_dict[errorFC]

            # arcpy.AddMessage("ErrorFC: %s" % str(errorFC))

            # start a search cursor to report issues
            wc = "isException = 0"
            lyr = "lyr"
            # try:
            MakeFeatureLayer_management(errorFC, lyr, wc)
            # except:
            #     excinfo = sys.exc_info()
            #     tb = extract_tb(excinfo[2])
            #     arcpy.AddError(sys.exc_info())
            #     arcpy.AddError(tb)

            k = getFastCount(lyr)

            if k > 0:

                # set up ESB tracking
                esb_list = []
                esb_lengths = []
                reportESB = False
                esb_dict = {}

                # AddMessage("Lyr: %s" % lyr)
                # AddMessage("Fields: %s" % fields)

                with SearchCursor(lyr, fields) as rows:
                    topo_rec = [val for val in SearchCursor(lyr, fields)]
                    topo_len = len(topo_rec)
                    lyr_name = basename(errorFC)
                    SetProgressor("step", "Beginning export of topology errors for polygons, polylines, and points...", 0, topo_len, 1)
                    for row in rows:

                        dual_rule_switch = False

                        try:
                            # rules that use both Origin and Destination to describe the errors
                            if len(row) >= 4:
                                if row[0] not in [None, "", " "] and row[3] not in [None, "", " "]:
                                    origin_fc = row[0]
                                    origin_id = row[1]
                                    destination_fc = row[3]
                                    destination_id = row[4]
                                    fc = origin_fc
                                    objectID = origin_id
                                    oid = "OriginObjectID"
                                    dest_oid = "DestinationObjectID"
                                    dual_rule_switch = True
                                elif row[0] in [None, "", " "]:
                                    fc = row[3]
                                    objectID = row[4]
                                    oid = "DestinationObjectID"
                                # Else: Use first set of values (origin)
                                else:
                                    fc = row[0]
                                    objectID = row[1]
                                    oid = "OriginObjectID"
                            # if the first set of values (origin) is None, use second set of values (destination)
                            else:
                                fc = row[0]
                                objectID = row[1]
                                oid = "OriginObjectID"
                        except:
                            userWarning("Could not create error for Topology error feature class: %s" % lyr_name)
                            continue

                        SetProgressorPosition()
                        SetProgressorLabel("Checking %s to export errors..." %fc)

                        ruleDesc = row[2]

                        # fc = row[0]
                        # AddMessage("Row 0: %s" % row[0])
                        # objectID = row[1]
                        # AddMessage("Row 1: %s" % row[1])
                        # ruleDesc = row[2]
                        # AddMessage("Row 2: %s" % row[2])

                        # get the issues
                        if basename(errorFC) == "NG911_Topology_poly" and check_polygons == True:
                            # top_fields_poly = ["OriginObjectClassName", "OriginObjectID", "RuleDescription", "DestinationObjectClassName", "DestinationObjectID"]


                            if dual_rule_switch:
                                # FL for fc_origin (FL_origin)
                                # FL for fc_destination (FL_destination)
                                # Join FL_origin to FL_errors (oid & OBJECTID)
                                # Join FL_destination to FL_errors (dest_oid & OBJECTID)
                                # Create a list of uniqueID tuples from FL_origin.UNIQUEID and FL_destination.UNIQUEID
                                # Get count per UniqueID tuples (numpy.unique with return_count=True)
                                # Create error msgs based on Unique ID tuple, RuleDesc, and count
                                # origin

                                userMessage("Poly Topo, Feature Classes: %s, %s | %s" % (fc, destination_fc, ruleDesc))

                                wc = "RuleDescription = '%s'" % (ruleDesc)
                                lyr_rule = "lyr_rule"
                                MakeFeatureLayer_management(lyr, lyr_rule, wc)

                                # origin FL
                                fc_lyr_origin = "fc_lyr_origin"
                                fc_full_origin = join(gdb, "NG911", fc)
                                MakeFeatureLayer_management(fc_full_origin, fc_lyr_origin)

                                # destination FL
                                fc_lyr_destination = "fc_lyr_destination"
                                fc_full_dest = join(gdb, "NG911", destination_fc)
                                MakeFeatureLayer_management(fc_full_dest, fc_lyr_destination)

                                # joins FLs to error FL
                                AddJoin_management(lyr_rule, oid, fc_lyr_origin, "OBJECTID")
                                AddJoin_management(lyr_rule, dest_oid, fc_lyr_destination, "OBJECTID")

                                # grab appropriate objects
                                origin_obj = NG911_GDB_Objects.getFCObject(fc_full_origin)
                                destination_obj = NG911_GDB_Objects.getFCObject(fc_full_dest)

                                qry = "%s.%s IS NOT NULL and %s.isException = 0 and %s.%s = 'Y'" % (basename(errorFC), oid, basename(errorFC), basename(fc_full_origin), origin_obj.SUBMIT)
                                qry += " and %s.%s IS NOT NULL and %s.%s = 'Y'" % (basename(errorFC), dest_oid, basename(fc_full_dest), destination_obj.SUBMIT)
                                fields = ("%s.%s" % (fc, origin_obj.UNIQUEID), "%s.%s" % (destination_fc, destination_obj.UNIQUEID), basename(errorFC) + ".RuleDescription",basename(errorFC) + ".isException") # origin_fc.UNIQUEID, destination_fc.UNIQUEID, errorFC.RuleDescription, errorFC.isException

                                compare_list = []
                                counter = {}

                                for tup in SearchCursor(lyr_rule, fields, qry):
                                    if len(compare_list) > 0:
                                        if (tup[0], tup[1]) in compare_list:
                                            next_value = counter[(tup[0], tup[1])] + 1
                                            counter[(tup[0], tup[1])] = next_value
                                        elif (tup[1], tup[0]) in compare_list:
                                            next_value = counter[(tup[1], tup[0])] + 1
                                            counter[(tup[1], tup[0])] = next_value
                                        else:
                                            compare_list.append((tup[0], tup[1]))
                                            counter[(tup[0], tup[1])] = 1
                                    else:
                                        compare_list.append((tup[0], tup[1]))
                                        counter[(tup[0], tup[1])] = 1

                                for ids, count in counter.items():
                                    msg = "Error: Topology issue- %s | Number of errors- %s" % (ruleDesc, unicode(count))
                                    fc_1 = fc[:20] if len(fc) > 20 else fc
                                    fc_2 = destination_fc[:20] if len(destination_fc) > 20 else destination_fc
                                    fc_string = "%s|%s" % (fc_1, fc_2)

                                    id_1 = ids[0][:99] if len(ids[0]) > 99 else ids[0]
                                    id_2 = ids[1][:99] if len(ids[1]) > 99 else ids[1]
                                    id_string = "%s|%s" % (id_1, id_2)
                                    val = (today, msg, fc_string, "", id_string, "Check Topology")
                                    values.append(val)

                                # clean up & reset
                                RemoveJoin_management(lyr_rule)
                                Delete_management(fc_lyr_origin)
                                Delete_management(fc_lyr_destination)
                                Delete_management(lyr_rule)


                            else:

                                userMessage("Poly Topo, Feature Class: %s | %s" % (fc, ruleDesc))

                                fc_lyr = "fc_lyr"
                                fc_full = join(gdb, "NG911", fc)
                                # arcpy.AddMessage("fc_full: %s" % str(fc_full))
                                # arcpy.AddMessage("fc: %s" % str(fc))


                                # try:
                                MakeFeatureLayer_management(fc_full, fc_lyr)
                                # except:
                                #     excinfo = sys.exc_info()
                                #     tb = extract_tb(excinfo[2])
                                #     arcpy.AddError(sys.exc_info())
                                #     arcpy.AddError(tb)

                                #add join
                                AddJoin_management(fc_lyr, "OBJECTID", lyr, oid)

                                obj = NG911_GDB_Objects.getFCObject(fc_full)

                                #set query and field variables
                                # qry = "%s.OriginObjectID IS NOT NULL and %s.isException = 0" % (basename(errorFC), basename(errorFC))
                                qry = "%s.%s IS NOT NULL and %s.isException = 0 and %s.SUBMIT = 'Y'" % (basename(errorFC), oid, basename(errorFC), basename(fc_full))
                                fields2 = ("%s.%s" % (fc, obj.UNIQUEID), basename(errorFC) + ".RuleDescription", basename(errorFC) + ".isException")

                                #set up search cursor to loop through records
                                #query per poly rule that requires a summation count for the error report then get quick count and pass the result to the error
                                for rule in sum_rule:
                                    qry_for_cnt = qry + " and %s.RuleDescription = '%s'" % (basename(errorFC), rule)
                                    selected_from_qry = [val[0] for val in SearchCursor(fc_lyr, fields2, qry_for_cnt) if val[2] not in [1, "1"]]
                                    if len(selected_from_qry) > 0:
                                        unique_cnt = numpy.unique(selected_from_qry, return_counts=True)
                                        for value, count in zip(*unique_cnt):
                                            msg = "Error: Topology issue- %s | Number of errors- %s" % (rule, unicode(count))
                                            val = (today, msg, fc, "", value, "Check Topology")
                                            values.append(val)

                                # Remove all rules with Summation for next Search query
                                sum_rule_string = ["'%s'" % rule for rule in sum_rule]
                                dual_rule_string = ["'%s'" % rule for rule in dual_rule_list]
                                append_string = sum_rule_string + dual_rule_string
                                append_string = ",".join(append_string)
                                qry_not_cnt = qry + " and %s.RuleDescription not in (%s)" % (basename(errorFC), append_string)

                                with SearchCursor(fc_lyr, fields2, qry_not_cnt) as rows2:

                                    for row2 in rows2:
                                        # make sure we're not reporting back an exception
                                        if row2[2] not in (1, "1"):

                                            # report the issues back as notices
                                            msg = "Error: Topology issue- %s" % row2[1]
                                            val = (today, msg, fc, "", row2[0], "Check Topology")
                                            values.append(val)
                                    try:
                                        del row2, rows2
                                    except:
                                        pass

                                #clean up & reset
                                RemoveJoin_management(fc_lyr)
                                Delete_management(fc_lyr)

                        elif basename(errorFC) == "NG911_Topology_line":
                            userMessage("Line Topo, Feature Class: %s" % fc)

                            if dual_rule_switch:
                                # ESB and road relationship
                                if check_roads == True and "ROAD" in fc.upper() and "ROAD" in destination_fc.upper():
                                    userMessage("Line Topo, Feature Classes: %s, %s | %s" % (fc, destination_fc, ruleDesc))

                                    wc = "RuleDescription = '%s'" % (ruleDesc)
                                    lyr_rule = "lyr_rule"
                                    MakeFeatureLayer_management(lyr, lyr_rule, wc)

                                    # origin FL
                                    fc_lyr_origin = "fc_lyr_origin"
                                    fc_full_origin = join(gdb, "NG911", fc)
                                    MakeFeatureLayer_management(fc_full_origin, fc_lyr_origin)

                                    # destination FL
                                    fc_lyr_destination = "fc_lyr_destination"
                                    fc_full_dest = join(gdb, "NG911", destination_fc)
                                    MakeFeatureLayer_management(fc_full_dest, fc_lyr_destination)

                                    # joins FLs to error FL
                                    AddJoin_management(lyr_rule, oid, fc_lyr_origin, "OBJECTID")
                                    AddJoin_management(lyr_rule, dest_oid, fc_lyr_destination, "OBJECTID")

                                    # grab appropriate objects
                                    origin_obj = NG911_GDB_Objects.getFCObject(fc_full_origin)
                                    destination_obj = NG911_GDB_Objects.getFCObject(fc_full_dest)

                                    qry = "%s.%s IS NOT NULL and %s.isException = 0 and %s.%s = 'Y'" % (basename(errorFC), oid, basename(errorFC), basename(fc_full_origin), origin_obj.SUBMIT)
                                    qry += " and %s.%s IS NOT NULL and %s.%s = 'Y'" % (basename(errorFC), dest_oid, basename(fc_full_dest), destination_obj.SUBMIT)
                                    fields = ("%s.%s" % (fc, origin_obj.UNIQUEID), "%s.%s" % (destination_fc, destination_obj.UNIQUEID), basename(errorFC) + ".RuleDescription", basename(errorFC) + ".isException")  # origin_fc.UNIQUEID, destination_fc.UNIQUEID, errorFC.RuleDescription, errorFC.isException

                                    compare_list = []
                                    counter = {}

                                    for tup in SearchCursor(lyr_rule, fields, qry):
                                        if len(compare_list) > 0:
                                            if (tup[0], tup[1]) in compare_list:
                                                next_value = counter[(tup[0], tup[1])] + 1
                                                counter[(tup[0], tup[1])] = next_value
                                            elif (tup[1], tup[0]) in compare_list:
                                                next_value = counter[(tup[1], tup[0])] + 1
                                                counter[(tup[1], tup[0])] = next_value
                                            else:
                                                compare_list.append((tup[0], tup[1]))
                                                counter[(tup[0], tup[1])] = 1
                                        else:
                                            compare_list.append((tup[0], tup[1]))
                                            counter[(tup[0], tup[1])] = 1

                                    for ids, count in counter.items():
                                        msg = "Error: Topology issue- %s | Number of errors- %s" % (
                                        ruleDesc, unicode(count))
                                        fc_1 = fc[:20] if len(fc) > 20 else fc
                                        fc_2 = destination_fc[:20] if len(destination_fc) > 20 else destination_fc
                                        fc_string = "%s|%s" % (fc_1, fc_2)

                                        id_1 = ids[0][:99] if len(ids[0]) > 99 else ids[0]
                                        id_2 = ids[1][:99] if len(ids[1]) > 99 else ids[1]
                                        id_string = "%s|%s" % (id_1, id_2)
                                        val = (today, msg, fc_string, "", id_string, "Check Topology")
                                        values.append(val)

                                    # clean up & reset
                                    RemoveJoin_management(lyr_rule)
                                    Delete_management(fc_lyr_origin)
                                    Delete_management(fc_lyr_destination)
                                    Delete_management(lyr_rule)


                            else:

                                # ESB and road relationship
                                if check_polygons == True and "ESB" in fc.upper():
                                    # get some stats to analyze after the loop

                                    # ESB layer must be unique
                                    if fc not in esb_list:
                                        esb_list.append(fc)
                                    else:
                                        reportESB = True

                                    # rules must be "Must Not Have Gaps"
                                    if ruleDesc != "Must Not Have Gaps":
                                        reportESB = True

                                    # shape must all be the same
                                    esb_length = row[3]
                                    if esb_lengths == []:
                                        esb_lengths.append(esb_length)
                                    elif esb_length not in esb_lengths:
                                        reportESB = True

                                    # collect ESB issue details in case we have to report
                                    if fc not in esb_dict:
                                        esb_dict[fc] = [ruleDesc]
                                    else:
                                        rules = esb_dict[fc]
                                        rules.append(ruleDesc)
                                        esb_dict[fc] = rules

                                if check_roads == True and "ROAD" in fc.upper():

                                    # see if the road is marked as an exception or not
                                    wc = "OBJECTID = " + unicode(objectID)
                                    with SearchCursor(roads, (rd_object.UNIQUEID, rd_object.TopoExcept), wc) as j_rows:
                                        for j_row in j_rows:
                                            # get the NGSEGID & the exception
                                            ngsegid = j_row[0]
                                            rd_exc = j_row[1]

                                            # check to see if the exception has been marked
                                            if rd_exc in exc_dict:

                                                # get the list of plausible exceptions
                                                plausibleException = exc_dict[rd_exc]

                                                # if the reported issue isn't in acceptable exceptions,
                                                # then report it
                                                if ruleDesc not in plausibleException:
                                                    userMessage("In attributes: " + ", ".join(plausibleException))
                                                    userMessage("In topology: " + ruleDesc)
                                                    # then report the issue
                                                    msg = "Error: Topology issue- %s" % ruleDesc
                                                    val = (today, msg, fc, "", ngsegid, "Check Topology")
                                                    values.append(val)

                                                # the else implying that the marked exception and the
                                                # found issue match, so it should not be marked

                                            # this means it isn't marked, so report the topology issue
                                            elif rd_exc == "NO_EXCEPTION":
                                                # then report the issue
                                                msg = "Error: Topology issue- %s" % ruleDesc
                                                val = (today, msg, fc, "", ngsegid, "Check Topology")
                                                values.append(val)

                                        try:
                                            del j_row, j_rows
                                        except:
                                            pass

                        elif basename(errorFC) == "NG911_Topology_point":

                            if dual_rule_switch:
                                userMessage("Point Topo, Feature Classes: %s, %s | %s" % (fc, destination_fc, ruleDesc))

                                wc = "RuleDescription = '%s'" % (ruleDesc)
                                lyr_rule = "lyr_rule"
                                MakeFeatureLayer_management(lyr, lyr_rule, wc)

                                # origin FL
                                fc_lyr_origin = "fc_lyr_origin"
                                fc_full_origin = join(gdb, "NG911", fc)
                                MakeFeatureLayer_management(fc_full_origin, fc_lyr_origin)

                                # destination FL
                                fc_lyr_destination = "fc_lyr_destination"
                                fc_full_dest = join(gdb, "NG911", destination_fc)
                                MakeFeatureLayer_management(fc_full_dest, fc_lyr_destination)

                                # joins FLs to error FL
                                AddJoin_management(lyr_rule, oid, fc_lyr_origin, "OBJECTID")
                                AddJoin_management(lyr_rule, dest_oid, fc_lyr_destination, "OBJECTID")

                                # grab appropriate objects
                                origin_obj = NG911_GDB_Objects.getFCObject(fc_full_origin)
                                destination_obj = NG911_GDB_Objects.getFCObject(fc_full_dest)

                                qry = "%s.%s IS NOT NULL and %s.isException = 0 and %s.%s = 'Y'" % (
                                basename(errorFC), oid, basename(errorFC), basename(fc_full_origin), origin_obj.SUBMIT)
                                qry += " and %s.%s IS NOT NULL and %s.%s = 'Y'" % (
                                basename(errorFC), dest_oid, basename(fc_full_dest), destination_obj.SUBMIT)
                                fields = ("%s.%s" % (fc, origin_obj.UNIQUEID),
                                          "%s.%s" % (destination_fc, destination_obj.UNIQUEID),
                                          basename(errorFC) + ".RuleDescription", basename(
                                    errorFC) + ".isException")  # origin_fc.UNIQUEID, destination_fc.UNIQUEID, errorFC.RuleDescription, errorFC.isException

                                compare_list = []
                                counter = {}

                                for tup in SearchCursor(lyr_rule, fields, qry):
                                    if len(compare_list) > 0:
                                        if (tup[0], tup[1]) in compare_list:
                                            next_value = counter[(tup[0], tup[1])] + 1
                                            counter[(tup[0], tup[1])] = next_value
                                        elif (tup[1], tup[0]) in compare_list:
                                            next_value = counter[(tup[1], tup[0])] + 1
                                            counter[(tup[1], tup[0])] = next_value
                                        else:
                                            compare_list.append((tup[0], tup[1]))
                                            counter[(tup[0], tup[1])] = 1
                                    else:
                                        compare_list.append((tup[0], tup[1]))
                                        counter[(tup[0], tup[1])] = 1

                                for ids, count in counter.items():
                                    msg = "Error: Topology issue- %s | Number of errors- %s" % (
                                    ruleDesc, unicode(count))
                                    fc_1 = fc[:20] if len(fc) > 20 else fc
                                    fc_2 = destination_fc[:20] if len(destination_fc) > 20 else destination_fc
                                    fc_string = "%s|%s" % (fc_1, fc_2)

                                    id_1 = ids[0][:99] if len(ids[0]) > 99 else ids[0]
                                    id_2 = ids[1][:99] if len(ids[1]) > 99 else ids[1]
                                    id_string = "%s|%s" % (id_1, id_2)
                                    val = (today, msg, fc_string, "", id_string, "Check Topology")
                                    values.append(val)

                                # clean up & reset
                                RemoveJoin_management(lyr_rule)
                                Delete_management(fc_lyr_origin)
                                Delete_management(fc_lyr_destination)
                                Delete_management(lyr_rule)

                            else:

                                userMessage("Point Topo, Feature Class: %s" % fc)
                                if check_roads == True and "ROAD" in fc.upper():

                                    # see if the road is marked as an exception or not
                                    if ruleDesc in sum_rule:
                                        # perform summation error analysis
                                        fc_lyr = "fc_lyr"
                                        fc_full = join(gdb, "NG911", fc)
                                        # arcpy.AddMessage("fc_full: %s" % str(fc_full))
                                        # arcpy.AddMessage("fc: %s" % str(fc))

                                        # try:
                                        MakeFeatureLayer_management(fc_full, fc_lyr)
                                        # except:
                                        #     excinfo = sys.exc_info()
                                        #     tb = extract_tb(excinfo[2])
                                        #     arcpy.AddError(sys.exc_info())
                                        #     arcpy.AddError(tb)

                                        # add join
                                        AddJoin_management(fc_lyr, "OBJECTID", lyr, oid)

                                        obj = NG911_GDB_Objects.getFCObject(fc_full)

                                        # set query and field variables
                                        # qry = "%s.OriginObjectID IS NOT NULL and %s.isException = 0" % (basename(errorFC), basename(errorFC))
                                        qry = "%s.%s IS NOT NULL and %s.isException = 0 and %s.SUBMIT = 'Y'" % (basename(errorFC), oid, basename(errorFC), basename(fc_full))
                                        fields2 = ("%s.%s" % (fc, obj.UNIQUEID), basename(errorFC) + ".RuleDescription", basename(errorFC) + ".isException")

                                        # set up search cursor to loop through records
                                        # query per poly rule that requires a summation count for the error report then get quick count and pass the result to the error

                                        qry_for_cnt = qry + " and %s.RuleDescription = '%s'" % (basename(errorFC), ruleDesc)
                                        selected_from_qry = [val[0] for val in SearchCursor(fc_lyr, fields2, qry_for_cnt) if val[2] not in [1, "1"]]
                                        if len(selected_from_qry) > 0:
                                            unique_cnt = numpy.unique(selected_from_qry, return_counts=True)

                                            for value, count in zip(*unique_cnt):
                                                msg = "Error: Topology issue- %s | Number of errors- %s" % (ruleDesc, unicode(count))
                                                val = (today, msg, fc, "", value, "Check Topology")
                                                values.append(val)

                                        # clean up & reset
                                        RemoveJoin_management(fc_lyr)
                                        Delete_management(fc_lyr)

                                    else:
                                        wc = "OBJECTID = " + unicode(objectID)
                                        with SearchCursor(roads, (rd_object.UNIQUEID, rd_object.TopoExcept), wc) as j_rows:
                                            for j_row in j_rows:
                                                # get the NGSEGID & the exception
                                                ngsegid = j_row[0]
                                                rd_exc = j_row[1]

                                                # check to see if the exception has been marked
                                                if rd_exc in exc_dict:

                                                    # get the list of plausible exceptions
                                                    plausibleException = exc_dict[rd_exc]

                                                    # if the reported issue isn't in acceptable exceptions,
                                                    # then report it
                                                    if ruleDesc not in plausibleException:
                                                        userMessage("In attributes: " + ", ".join(plausibleException))
                                                        userMessage("In topology: " + ruleDesc)
                                                        # then report the issue
                                                        msg = "Error: Topology issue- %s" % ruleDesc
                                                        val = (today, msg, fc, "", ngsegid, "Check Topology")
                                                        values.append(val)

                                                    # the else implying that the marked exception and the
                                                    # found issue match, so it should not be marked

                                                # this means it isn't marked, so report the topology issue
                                                elif rd_exc == "NO_EXCEPTION":
                                                    # then report the issue
                                                    msg = "Error: Topology issue- %s" % ruleDesc
                                                    val = (today, msg, fc, "", ngsegid, "Check Topology")
                                                    values.append(val)

                                            try:
                                                del j_row, j_rows
                                            except:
                                                pass

                                elif "ADDRESS" in fc.upper():

                                    # see if the road is marked as an exception or not
                                    wc = "OBJECTID = " + unicode(objectID)
                                    # with SearchCursor(addresses, (ap_object.UNIQUEID, ap_object.TopoExcept), wc) as j_rows:
                                    # TODO: Replace below line with above line when TopoExcept added
                                    with SearchCursor(addresses, ap_object.UNIQUEID, wc) as j_rows:
                                        for j_row in j_rows:
                                            # TODO: Re-enable appropriate disabled code below when TopoExcept added; also improve variable names
                                            # get the NGSEGID & the exception
                                            ngsegid = j_row[0]
                                            # rd_exc = j_row[1]
                                            #
                                            # # check to see if the exception has been marked
                                            # if rd_exc in exc_dict:
                                            #
                                            #     # get the list of plausible exceptions
                                            #     plausibleException = exc_dict[rd_exc]
                                            #
                                            #     # if the reported issue isn't in acceptable exceptions,
                                            #     # then report it
                                            #     if ruleDesc not in plausibleException:
                                            #         userMessage("In attributes: " + ", ".join(plausibleException))
                                            #         userMessage("In topology: " + ruleDesc)
                                            #         # then report the issue
                                            #         msg = "Error: Topology issue- %s" % ruleDesc
                                            #         val = (today, msg, fc, "", ngsegid, "Check Topology")
                                            #         values.append(val)
                                            #
                                            #     # the else implying that the marked exception and the
                                            #     # found issue match, so it should not be marked
                                            #
                                            # # this means it isn't marked, so report the topology issue
                                            # elif rd_exc == "NO_EXCEPTION":
                                                # then report the issue
                                            msg = "Error: Topology issue- %s" % ruleDesc  # TODO: re-indent when TopoExcept added
                                            val = (today, msg, fc, "", ngsegid, "Check Topology")  # TODO: re-indent when TopoExcept added
                                            values.append(val)  # TODO: re-indent when TopoExcept added

                                        try:
                                            del j_row, j_rows
                                        except:
                                            pass

                    ResetProgressor()

                # report back polygon issues
                if reportESB == True:
                    for esb in esb_dict:
                        rules = esb_dict[esb]
                        for rule in rules:
                            # report the issues back as notices
                            # userMessage("Error: Topology issue- %s" % rule)
                            msg = "Error: Topology issue- %s" % rule
                            val = (today, msg, esb, "", "", "Check Topology")
                            values.append(val)
            Delete_management(lyr)



    else:
        msg = "Error: Topology does not exist"
        val = (today, msg, "", "", "", "Check Topology")
        values.append(val)

    #report records
    count = 0
    if values != []:
        count = len(values)
        RecordResults(recordType, values, gdb)


    #give the user some feedback
    messageList = ["Topology check complete.", str(count), "issues found."]
    if count > 0:
        messageList.append("Results in FieldValuesCheckResults.")
    elif count == 0:
        #clean up topology export if there were no errors
        for topE in (lineErrors, pointErrors, polyErrors):
            full = join(gdb, topE)
            if Exists(full):
                Delete_management(full)

    message = " ".join(messageList)
    userMessage(message)


def checkToolboxVersionFinal():
    versionResult = checkToolboxVersion()
    if versionResult == "Your NG911 toolbox version is up-to-date.":
        userMessage(versionResult)
    else:
        userWarning(versionResult)

def sanityCheck(currentPathSettings):
    # type: (NG911_Session_obj) -> int
    """
    Function executed by the `Validation - Check All` tool (and therefore additionally by the `Submission - Check All
    and Zip` tool).

    This function performs ALL validation checks to determine whether or not the data in a given geodatabase is ready
    for submission. Errors causing the geodatabase to fail validation are noted in the console as the program runs,
    and each error is also exported to one of the following tables, depending on the type of error:

    * `TemplateCheckResults`
    * `FieldValuesCheckResults`
    * `DASC_Communication` (No longer created)

    Those tables can be found in the geodatabase that was provided as input to this function (or the Validation - Check
    All tool).

    This function performs the following:

    * Template Checks

      * ``clearOldResults``
      * ``checkLayerList``
      * ``checkGDBDomains``
      * ``checkRequiredFields``
      * ``checkRequiredFieldValues``
      * ``checkSubmissionNumbers``
      * ``findInvalidGeometry``

    * Common Layer Checks

      * ``checkValuesAgainstDomain``
      * ``checkFeatureLocations``
      * ``checkTopology`` [Note: Run on road *and* polygon features, unlike in ``main_check``, where it is only run on road features]
      * ``checkUniqueID...``
        * ``...Format``
        * ``...Frequency``

    * Address Point Checks

      * ``checkMSAGCOspaces``
      * ``checkRCLMATCH``
      * ``checkFrequency``
      * ``checkESNandMuniAttribute``

    * Road Checks

      * ``checkMSAGCOspaces``
      * ``checkFrequency``
      * ``checkCutbacks``
      * ``checkDirectionality``
      * ``checkFrequency`` (of dual carriageways)
      * ``FindOverlaps``
      * ``checkParities``

    See ``main_check`` function documentation for details on the above check functions.

    Parameters
    ----------
    currentPathSettings : NG911_Session_obj
        The geodatabase session information. This object contains, among other things, the path to the geodatabase to be
        validated, the path to the `Domains` folder.

    Returns
    -------
    int
        0 or 1. Returns 1 (sane) if there are no errors that would prevent submission; 0 (insane, I guess) otherwise

    """
    # fcList will contain all layers in GDB so everything will be checked

    # clear out template check results & field check results
    gdb = currentPathSettings.gdbPath
    gdbObject = currentPathSettings.gdbObject
    templateTable = gdbObject.TemplateCheckResults
    if Exists(templateTable):
        deleteExisting(templateTable)
        userMessage(basename(templateTable) + " deleted")

    fieldValuesTable = gdbObject.FieldValuesCheckResults
    if Exists(fieldValuesTable):
        deleteExisting(fieldValuesTable)
        userMessage(basename(fieldValuesTable) + " deleted")

    # ClearOldResults(gdb, "true", "true")

    cnt_length = 21

    SetProgressor("step", "Checking All Required Layers...", 0, cnt_length, 1)
    # set_pos = SetProgressorPosition()

    # check template
    checkLayerList(currentPathSettings)
    SetProgressorPosition()
    checkGDBDomains(currentPathSettings)
    checkSpatialReference(currentPathSettings)
    SetProgressorPosition()
    checkRequiredFields(currentPathSettings)
    SetProgressorPosition()
    checkRequiredFieldValues(currentPathSettings)
    SetProgressorPosition()
    checkSubmissionNumbers(currentPathSettings)
    SetProgressorPosition()
    findInvalidGeometry(currentPathSettings)
    SetProgressorPosition()

    # common layer checks
    checkValuesAgainstDomain(currentPathSettings)
    SetProgressorPosition()
    # checkESBDisplayLength(currentPathSettings)
    checkFeatureLocations(currentPathSettings)
    SetProgressorPosition()
    try:
        checkTopology(gdbObject, True, True) # check everything

    except arcpy.ExecuteError as e:
        # userWarning(str(e))
        RecordResults("template", [(strftime("%Y/%m/%d"), "Error: Could not validate topology", "Topology", "Check Topology")], gdb)
        # excinfo = sys.exc_info()
        # tb = extract_tb(excinfo[2])
        # arcpy.AddError(sys.exc_info())
        # arcpy.AddError(tb)
    SetProgressorPosition()
    checkUniqueIDFrequency(currentPathSettings)  # also calls checkUniqueIDFormat
    SetProgressorPosition()

    # check address points
    if Exists(gdbObject.AddressPoints):
        addressPoints = gdbObject.AddressPoints
        checkMSAGCOspaces(addressPoints, gdb)
        SetProgressorPosition()
        if fieldExists(addressPoints, "RCLMatch"):
            checkRCLMATCH(currentPathSettings)
        else:
            userWarning("Missing required field RCLMatch.")
        SetProgressorPosition()
        AP_freq = gdbObject.AddressPointFrequency
        a_obj = NG911_GDB_Objects.getFCObject(addressPoints)
        AP_fields = a_obj.FREQUENCY_FIELDS_STRING
        checkFrequency(addressPoints, AP_freq, AP_fields, gdb, "true")
        SetProgressorPosition()
        if Exists(gdbObject.ESZ):
            checkESNandMuniAttribute(currentPathSettings)
        else:
            userWarning("ESZ layer does not exist. Cannot complete check.")
        SetProgressorPosition()
    else:
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()
        userWarning("Layer ADDRESS_POINT does not exist and therefore cannot be checked. This will prevent submission.")


    # check roads
    if Exists(gdbObject.RoadCenterline):
        roads = gdbObject.RoadCenterline
        road_freq = gdbObject.RoadCenterlineFrequency
        rc_obj = NG911_GDB_Objects.getFCObject(roads)
        road_fields = rc_obj.FREQUENCY_FIELDS_STRING

        # make sure editor tracking is turned on for the roads
        try:
            # EnableEditorTracking_management(roads, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields
            pass
        except:
            userWarning("Hit that PASS")
            pass

        checkMSAGCOspaces(roads, gdb)
        SetProgressorPosition()
        checkFrequency(roads, road_freq, road_fields, gdb, "true")
        SetProgressorPosition()
        checkCutbacks(currentPathSettings)
        SetProgressorPosition()
        checkDirectionality(roads, gdb)
        SetProgressorPosition()
        # checkRoadAliases(currentPathSettings)
        # complete check for duplicate address ranges on dual carriageways
        fields = rc_obj.FREQUENCY_FIELDS
        fields.remove("Oneway")  # TODO: Remove hard-code?
        fields_string = ";".join(fields)
        checkFrequency(roads, road_freq, fields_string, gdb, "false")
        SetProgressorPosition()
        # check for overlapping address ranges
        FindOverlaps(gdb)
        SetProgressorPosition()
        # check parities
        checkParities(currentPathSettings)
        SetProgressorPosition()
    else:
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()
        userWarning("Layer ROAD_CENTERLINE does not exist and therefore cannot be checked. This will prevent submission.")

    # verify that the check resulted in 0 issues
    sanity = 0 # flag to return at end
    numErrors = 0 # the total number of errors

    fieldCheckResults = gdbObject.FieldValuesCheckResults
    templateResults = gdbObject.TemplateCheckResults

    for table in [fieldCheckResults, templateResults]:
        if Exists(table):
            tbl = "tbl"
            wc = "Description not like '%Notice%'"
            MakeTableView_management(table, tbl, wc)
            count = getFastCount(tbl)
            numErrors = numErrors + count
            Delete_management(tbl)

    #change result = 1
    if numErrors == 0:
        sanity = 1
        today = strftime("%Y/%m/%d")
        # values = [(today, "Passed all checks")]
        # RecordResults("DASCmessage", values, gdb)
        userMessage("Geodatabase passed all data checks.")
    else:
        userWarning("There were %s issues with the data that will prevent a successful submission. Please view errors in the TemplateCheckResults and/or FieldValuesCheckResults tables." % (str(numErrors)))
        # userWarning("For documentation on Interpreting Tool Results, please copy and paste this link into your web browser: https://goo.gl/aUlrLH")

    # checkToolboxVersionFinal()

    return sanity

def main_check(checkType, currentPathSettings):
    # type: (str, NG911_Session_obj) -> None
    # TODO: Finish main_check documentation for Check RCLMatch
    """
    Function containing the implementation of much of the Validation toolset's functionality. The type of check(s)
    to perform are indicated by the ``checkType`` parameter. Each check type has more specific checks that can be selected
    or deselected by the user. There are four valid options for ``checkType``:

    * "template"

      * `Check Layer List`: Checks for required layers. Missing required layers are reported in the `TemplateCheckResults` table.
      * `Check Required Fields`: Checks feature classes to ensure that they contain the required fields.
      * `Check Required Field Values`: Returns errors if required fields contain null values.
      * `Check Submission Numbers`: Checks to see how many features are marked for submission.
      * `Find Invalid Geometry`: Returns errors if points, lines, or polygons have fewer than 1, 2, or 3 points, respectively.
      * `Check GDB Domains`: Returns errors if Domains for the geodatabase don't match the domains in the Domains Folder

    * "ADDRESS_POINT"

      * `Check Values Against Domain`: Ensures that fields with domains contain values that match the domain.
      * (Run with above) `Check MSAGCO Spaces`: Checks for and removes leading or trailing spaces in MSAGComm fields.
      * (Run with above if field `RCLMatch` exists) `Check RCLMatch`: Validates the `RCLMatch` field of the ADDRESS_POINTS feature class against the ROAD_CENTERLINE feature class.
      * `Check Feature Locations`: Compares features in a feature class to the discrepancy agency boundary to ensure that they lie within a boundary.
      * `Check Frequency`: Checks for identical address records and returns errors if any are found.
      * `Check Unique ID Frequency`: Ensures that no address records share unique IDs.
      * `Check ESN and Muni Attribute`: Selects address points using ESN or muni polygons to check `ESN` and `City` attributes match those of the polygons.

    * "Roads"

      * `Check Values Against Domain`: Ensures that fields with domains contain values that match the domain.
      * (Run with above) `Check MSAGCO Spaces`: Checks for and removes leading or trailing spaces in MSAGComm fields.
      * (Run with above) `Check Parities`: Returns a notice if address ranges do not match parity fields
      * `Check Feature Locations`: Compares features in a feature class to the discrepancy agency boundary to ensure that they lie within a boundary.
      * `Check Frequency`: (Called twice; why?) `Check Frequency`: Checks for identical road centerline records and returns errors if any are found.
      * `Check Unique ID Frequency`: Ensures that no road centerline records share unique IDs.
      * `Check Cutbacks`: Returns a notice if a road centerline feature contains angle on the open interval (0, 55) degrees, which could potentially indicate a cutback.
      * (Run with above): `Check Topology` (of just roads): Generates and attempts to validate topology rules for road centerline features.
      * `Check Directionality`: Ensures that address ranges run from low to high numbers.
      * `Check Address Range Overlaps`: Checks for numerical overlaps in address ranges between road centerline features.

    * "standard"

      * `Check Values Against Domain`: Ensures that fields with domains contain values that match the domain.
      * `Check Feature Locations`: Compares features in a feature class to the discrepancy agency boundary to ensure that they lie within a boundary.
      * `Check Unique ID Frequency`: Ensures that no records in boundary feature classes share unique IDs.

    Finally, errors are written to the `TemplateCheckResults` and/or `FieldValuesCheckResults` tables.

    Parameters
    ----------
    checkType : str
        One of "template", "ADDRESS_POINT", "Roads", "standard"
    currentPathSettings : NG911_Session_obj
        The session object
    """

    checkList = currentPathSettings.checkList
    gdb = currentPathSettings.gdbPath
    env.workspace = gdb
    env.overwriteOutput = True

    gdbObject = currentPathSettings.gdbObject  # type: __NG911_GDB_Object

    #give user a warning if they didn't select any validation checks
    stuffToCheck = 0
    for cI in checkList:
        if cI == "true":
            stuffToCheck += 1
    if stuffToCheck == 0:
        userWarning("Warning: you choose no validation checks.")

    #check geodatabase template
    if checkType == "template":
        temp_len = 6
        SetProgressor("step", "Checking Template...", 0, temp_len, 1)

        if checkList[0] == "true":
            checkSpatialReference(currentPathSettings)
            checkLayerList(currentPathSettings)
        SetProgressorPosition()

        if checkList[1] == "true":
            checkRequiredFields(currentPathSettings)
        SetProgressorPosition()

        if checkList[2] == "true":
            checkRequiredFieldValues(currentPathSettings)
        SetProgressorPosition()

        if checkList[3] == "true":
            checkSubmissionNumbers(currentPathSettings)
        SetProgressorPosition()

        if checkList[4] == "true":
            findInvalidGeometry(currentPathSettings)
        SetProgressorPosition()

        if checkList[5] == "true":
            checkGDBDomains(currentPathSettings)
        SetProgressorPosition()

        ResetProgressor()

    #check address points
    elif checkType == "ADDRESS_POINT": # Changed to OK Fields/Layer
        add_len = 7
        SetProgressor("step","Checking Address Point...", 0, add_len, 1)
        addressPoints = gdbObject.AddressPoints
        if checkList[0] == "true":
            checkValuesAgainstDomain(currentPathSettings)
            SetProgressorPosition()
            checkMSAGCOspaces(addressPoints, gdb)
            SetProgressorPosition()
            # checkOKPID(addressPoints, "OKPID") # Changed to OK Fields
        else:
            SetProgressorPosition()
            SetProgressorPosition()
            SetProgressorPosition()

        if checkList[1] == "true":
            checkFeatureLocations(currentPathSettings)
            SetProgressorPosition()
            if fieldExists(addressPoints, "RCLMatch"):
                # pass
                checkRCLMATCH(currentPathSettings)
                # checkAddressPointGEOMSAG(currentPathSettings)
            else:
                userWarning("Missing required field RCLMatch.")
            SetProgressorPosition()
        else:
            SetProgressorPosition()
            SetProgressorPosition()


        if checkList[2] == "true":
            # TODO: Figure out if lat/long should be included in the frequency check; if lat/long
            #       are included, this may return false negatives for duplicated addresses
            #       example/ Beaver County with lat/long versus without lat/long
            AP_freq = gdbObject.AddressPointFrequency
            a_obj = NG911_GDB_Objects.getFCObject(addressPoints)
            AP_fields = a_obj.FREQUENCY_FIELDS_STRING
            checkFrequency(addressPoints, AP_freq, AP_fields, gdb, "true")
        SetProgressorPosition()

        if checkList[3] == "true":
            checkUniqueIDFrequency(currentPathSettings)
        SetProgressorPosition()

        if checkList[4] == "true":
            if Exists(gdbObject.ESZ):
                checkESNandMuniAttribute(currentPathSettings)
            else:
                userWarning("ESZ layer does not exist, cannot complete ESN Attribute check.")
        SetProgressorPosition()

        ResetProgressor()


    #check roads
    elif checkType == "Roads":
        road_len = 11
        SetProgressor("step", "Checking Road Centerline...", 0, road_len, 1)
        roads = gdbObject.RoadCenterline
        rc_obj = NG911_GDB_Objects.getFCObject(roads)
        if checkList[0] == "true":
            checkValuesAgainstDomain(currentPathSettings)
            checkMSAGCOspaces(roads, gdb)

            # check parity
            checkParities(currentPathSettings)
        SetProgressorPosition()
        SetProgressorPosition()
        SetProgressorPosition()

        if checkList[1] == "true":
            checkFeatureLocations(currentPathSettings)
        SetProgressorPosition()

        if checkList[2] == "true":
            road_freq = gdbObject.RoadCenterlineFrequency
            road_fields = rc_obj.FREQUENCY_FIELDS_STRING
            checkFrequency(roads, road_freq, road_fields, gdb, "true")

            # complete check for duplicate address ranges on dual carriageways
            road_freq = gdbObject.RoadCenterlineFrequency
            fields = rc_obj.FREQUENCY_FIELDS
            fields.remove("Oneway")
            fields_string = ";".join(fields)
            checkFrequency(roads, road_freq, fields_string, gdb, "false")
        SetProgressorPosition()
        SetProgressorPosition()

        if checkList[3] == "true":
            checkUniqueIDFrequency(currentPathSettings)
        SetProgressorPosition()

        if checkList[4] == "true":
            checkCutbacks(currentPathSettings)
            debugMessage("Topology check has been removed from road checks.")
            # checkTopology(gdbObject, False, True) # just check roads
        SetProgressorPosition()
        SetProgressorPosition()

        if checkList[5] == "true":
            checkDirectionality(roads, gdb)
        SetProgressorPosition()

        # if checkList[6] == "true":
        #     checkRoadAliases(currentPathSettings)

        # if checkList[7] == "true":
        if checkList[6] == "true":
            # check for address range overlaps
            FindOverlaps(gdb)
        SetProgressorPosition()

        ResetProgressor()

    # run standard checks
    elif checkType == "standard":
        stand_len = 4
        SetProgressor("step", "Checking Other...", 0, stand_len, 1)
        if checkList[0] == "true":
            checkValuesAgainstDomain(currentPathSettings)
            # checkESBDisplayLength(currentPathSettings)
        SetProgressorPosition()

        if checkList[1] == "true":
            checkFeatureLocations(currentPathSettings)
            debugMessage("Topology check has been removed from standard checks.")
            # try:
            # checkTopology(gdbObject, True, False) # just check polygons
            # except Exception as e:
            #     userWarning(str(e))
            #     RecordResults("template", [strftime("%m/%d/%y"), "Error: Could not validate topology", "Topology"], gdb)
            #     excinfo = sys.exc_info()
            #     tb = extract_tb(excinfo[2])
            #     arcpy.AddError(sys.exc_info())
            #     arcpy.AddError(tb)
        SetProgressorPosition()
        SetProgressorPosition()

        if checkList[2] == "true":
            checkUniqueIDFrequency(currentPathSettings)
        SetProgressorPosition()

        ResetProgressor()

    fieldCheckResults = gdbObject.FieldValuesCheckResults
    templateResults = gdbObject.TemplateCheckResults
    numErrors = 0

    for table in [fieldCheckResults, templateResults]:
        if Exists(table):
            tbl = "tbl"
            wc = "Description not like '%Notice%'"
            MakeTableView_management(table, tbl, wc)
            count = getFastCount(tbl)
            numErrors = numErrors + count
            Delete_management(tbl)

    # change result = 1
    if numErrors > 0:
        # BigMessage = """There were issues with the data. Please view errors in
        # the TemplateCheckResults and:or FieldValuesCheckResults tables. For
        # documentation on Interpreting Tool Results, please copy and paste this
        # link into your web browser: https://goo.gl/aUlrLH"""
        BigMessage = """There were issues with the data. Please view errors in
        the TemplateCheckResults and:or FieldValuesCheckResults tables."""
        userWarning(BigMessage)

    # checkToolboxVersionFinal()