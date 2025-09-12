#-------------------------------------------------------------------------------
# Name:        Comparison_CompareDataLayers
# Purpose:     Find edits in layers based on their unique ID fields
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     13/05/2016
# Modified:    August 03, 2021
#-------------------------------------------------------------------------------
from arcpy import (GetParameterAsText, AddJoin_management, Delete_management,
            CalculateField_management, AddField_management,
            Describe, AddIndex_management, DeleteField_management, RemoveJoin_management,
            Exists, CreateTable_management, AddError, FeatureClassToFeatureClass_conversion)
from arcpy.da import SearchCursor, InsertCursor
from os.path import join, basename, dirname
from NG911_User_Messages import userMessage
from NG911_arcpy_shortcuts import (ListFieldNames, MakeLayer, fieldExists, indexExists,
                getFastCount, hasRecords, cleanUp, deleteExisting)
from NG911_GDB_Objects import getFCObject, getGDBObject
from time import strftime

def CompareThatData(fc1, fc2, resultsTable, data_obj):

##    try:
        compare = "compare"
        ng911id = "ng911id"

        # get object of data
        data_obj = getFCObject(fc1)

        # get unique ID, RevDate, RevEditor
        uniqueID = data_obj.UNIQUEID
        revDate = data_obj.RevDate
        revEditor = data_obj.RevEditor

        # open in memory feature classes for join with different feature class name
        second_fc = "in_memory/fc2"
        deleteExisting(second_fc)
        FeatureClassToFeatureClass_conversion(fc2, "in_memory", "fc2")
        first_fc = "in_memory/fc1"
        deleteExisting(first_fc)
        FeatureClassToFeatureClass_conversion(fc1, "in_memory", "fc1")

        # convert to feature layer
        lyr1 = MakeLayer(fc1, "lyr1", "")
        lyr2 = MakeLayer(fc2, "lyr2", "")

        # if needed, add a field index in the unique ID
        if not indexExists(fc1, ng911id):
            AddIndex_management(lyr1, uniqueID, ng911id, "UNIQUE")
        if not indexExists(fc2, ng911id):
            AddIndex_management(lyr2, uniqueID, ng911id, "UNIQUE")

        # join the two layers
        AddJoin_management(lyr1, uniqueID, second_fc, uniqueID)

        lyr_compare = MakeLayer(lyr1, "lyr5")

        # set up list for reporting various edits
        attributeEdits = {}
        spatialEdits = []
        in1not2Records = []
        in2not1Records = []

        fields_fc1 = ListFieldNames(fc1)
        fields_fc2 = ListFieldNames(fc2)
        common_fields = []

        # build a common list of fields between both feature classes
        for field in fields_fc1:
            if field in fields_fc2:
                if field not in ["OBJECTID", unicode(uniqueID), "SHAPE@", "Shape", revDate, revEditor]:
                    common_fields.append(field)

        # search for attribute issues
        for field_name in common_fields:
            uniID1 = unicode(basename(fc1)) + "." + unicode(uniqueID)
            uniID2 = unicode(basename(second_fc)) + "." + unicode(uniqueID)
            current_fc1 = unicode(basename(fc1)) + "." + unicode(field_name)
            current_fc2 = unicode(basename(second_fc)) + "." + unicode(field_name)
            # userMessage(str(uniID1) + ": " + str(current_fc1) + ", " + str(uniID2) + ": " + str(current_fc2))
            with SearchCursor(lyr_compare, [uniID1, uniID2, current_fc1, current_fc2]) as cursor:
                for row in cursor:
                    if row[0] == row[1]:
                        if row[2] != row[3]:
                            attributeEdits[row[0]] = field_name
                            userMessage(unicode(row[0])+": "+unicode(field_name))
                del row

        # clean up attribute issue stuff
        # delete joined layer
        Delete_management(lyr_compare)

        # search for spatial differences if possible
        dataType = Describe(fc1).dataType
        if dataType != "Table":
            with SearchCursor(fc1, (uniqueID, "SHAPE@TRUECENTROID")) as sRows:
                for sRow in sRows:
                    uniqueID_val = unicode(sRow[0])
                    geom1 = sRow[1]
                    where_clause = uniqueID + " = '" + uniqueID_val + "'"
                    with SearchCursor(fc2, ("SHAPE@TRUECENTROID"), where_clause) as moreRows:
                        for mRow in moreRows:
                            geom2 = mRow[0]
                            if geom1 != geom2:
                                spatialEdits.append(uniqueID_val)
                del sRow, sRows

        # search for in 1 not 2 records
        wc1 = basename(second_fc) + "." + uniqueID + " is null"
        mismatch1 = MakeLayer(lyr1, "m1", wc1)

        count = getFastCount(mismatch1)

        if count > 0:
            with SearchCursor(mismatch1, (basename(fc1) + "." + uniqueID)) as rows:
                for row in rows:
                    uniqueID_val = unicode(row[0])
                    in1not2Records.append(uniqueID_val)
                del row, rows

        # clean up
        Delete_management(mismatch1)

        # remove join
        RemoveJoin_management(lyr1)

        # search for in 2 not 1 records
        AddJoin_management(lyr2, uniqueID, first_fc, uniqueID)
        wc2 = basename(first_fc) + "." + uniqueID + " is null"
        mismatch2 = MakeLayer(lyr2, "m2", wc2)

        count = getFastCount(mismatch2)

        if count > 0:
            with SearchCursor(mismatch2, (basename(fc2) + "." + uniqueID)) as rows:
                for row in rows:
                    uniqueID_val = unicode(row[0])
                    in2not1Records.append(uniqueID_val)
                del row, rows

        Delete_management(mismatch2)

        # remove join
        RemoveJoin_management(lyr2)

        # clean up
        # delete added fields
        DeleteField_management(fc1, [compare + "1"])
        DeleteField_management(fc2, [compare + "2"])

        # issue reporting
        attribute_unis = [x for x in attributeEdits.keys()]
        issueDict = {"Attribute edit": attribute_unis, "Spatial edit": spatialEdits,
        "Record not in " + fc2: in1not2Records, "Record not in " + fc1: in2not1Records}

        if issueDict != {"Attribute edit": [], "Spatial edit": [],
        "Record not in " + fc2: [], "Record not in " + fc1: []}:

            # see if the results table already exists
            if not Exists(resultsTable):
                CreateTable_management(dirname(resultsTable), basename(resultsTable))

            # see if the fields exists
            if not fieldExists(resultsTable, "DateChecked"):
                AddField_management(resultsTable, "DateChecked", "DATE")
            if not fieldExists(resultsTable, "FC1"):
                AddField_management(resultsTable, "FC1", "TEXT", "", "", 255)
            if not fieldExists(resultsTable, "FC2"):
                AddField_management(resultsTable, "FC2", "TEXT", "", "", 255)
            if not fieldExists(resultsTable, "EditResult"):
                AddField_management(resultsTable, "EditResult", "TEXT", "", "", 300)
            if not fieldExists(resultsTable, "FeatureID"):
                AddField_management(resultsTable, "FeatureID", "TEXT", "", "", 254)

            #create result records
            insertFields = ("DateChecked", "FC1", "FC2", "EditResult", "FeatureID")
            today = strftime("%Y/%m/%d")

            cursor = InsertCursor(resultsTable, insertFields)

            for message in issueDict:
                IDlist = issueDict[message]
                if IDlist != []:
                    for id_num in IDlist:
                        userMessage("Feature class 1: %s" % fc1)
                        userMessage("Feature class 2: %s" % fc2)
                        userMessage("Edit Results: %s" % message)
                        userMessage("Unique ID: %s" % id_num)
                        if "Attribute edit" in message:
                            message = "Attribute edit, %s" % (attributeEdits[id_num])
                        cursor.insertRow((today, fc1, fc2, message, id_num))
        else:
            userMessage("No changes were found.")

        Delete_management(lyr1)
        Delete_management(lyr2)

##    except Exception as e:
##        userMessage(str(e))
##    finally:
        cleanUp([lyr1, lyr2, lyr_compare])

def LaunchDataCompare(fc1, fc2, resultsTable):
##    try:
        userMessage(fc1)
        userMessage(fc2)

        keyword = basename(fc1).upper()
        if "FIRE" in keyword or "EMS" in keyword or "LAW" in keyword:
            keyword = "ESB"
        if "ESZ" in keyword:
            keyword = "ESZ"
        if "PSAP" in keyword:
            keyword = "PSAP"

        GoAheadAndTest = 1

        #make sure the two layers are the same type
        if basename(fc1) != basename(fc2):
            GoAheadAndTest = 0

        #make sure both layers have the same unique ID
        if GoAheadAndTest == 1:
            fields1 = ListFieldNames(fc1)
            fields2 = ListFieldNames(fc2)

            obj = getFCObject(fc1)
            uniqueID = obj.UNIQUEID
            if uniqueID not in fields1 or uniqueID not in fields2:
                GoAheadAndTest = 2

        if GoAheadAndTest == 1:
            userMessage("Comparing data...")
            CompareThatData(fc1, fc2, resultsTable, obj)
        elif GoAheadAndTest == 2:
            userMessage("Layers do not have the same unique ID and cannot be compared.")
        elif GoAheadAndTest == 0:
            userMessage("Layers are not the same NG911 type and cannot be comapared.")
##    except Exception as e:
##        userMessage("Cannot compare " + basename(fc1) + " and " + basename(fc2) + ".")
##        userMessage(str(e))

def CompareAllData(gdb1, gdb2, resultsTable):

    gdbObject = getGDBObject(gdb1)

    layers = gdbObject.fcList

    #launch the comparison for each active data lyaer
    for fc1 in layers:
        fc2 = fc1.replace(gdb1, gdb2)
        if Exists(fc2):
            if hasRecords(fc1) and hasRecords(fc2):
                LaunchDataCompare(fc1, fc2, resultsTable)

    userMessage("Results of the data comparison are in " + resultsTable)

def main():
    item1 = GetParameterAsText(0)
    item2 = GetParameterAsText(1)
    results_table = GetParameterAsText(2)

    #handle scripting options so either two feature classes or two geodatabases can be processed
    if Describe(item1).dataType == "FeatureClass":
        LaunchDataCompare(item1, item2, results_table)
    elif Describe(item1).dataType == "Workspace":
        CompareAllData(item1, item2, results_table)

if __name__ == '__main__':
    main()
