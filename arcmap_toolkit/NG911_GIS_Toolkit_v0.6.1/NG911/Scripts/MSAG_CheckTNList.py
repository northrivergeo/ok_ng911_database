#-------------------------------------------------------------------------------
# Name:        MSAG_CheckTNList
# Purpose:     Check a county's TN list against MSAG communities in the NG911 Address Point and Road Centerline files
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     03/09/2015
# Modified:    January 6, 2022
#-------------------------------------------------------------------------------
from arcpy import (Delete_management, AddField_management,
            CalculateField_management, GetParameterAsText, Exists, 
            CreateTable_management, CreateFileGDB_management,
            MakeTableView_management, DisableEditorTracking_management,
            EnableEditorTracking_management)
from arcpy.da import InsertCursor, UpdateCursor
from NG911_DataCheck import getFieldDomain
from NG911_User_Messages import userMessage, debugMessage
from os.path import join, dirname, basename, exists, realpath
from os import mkdir
from NG911_GDB_Objects import getFCObject, getTNObject, NG911_Session
from NG911_arcpy_shortcuts import getFastCount, fieldExists
from MSAG_DBComparison import launch_compare

try:
    from typing import Union
except:
    pass


def prepXLS(tnxls, gdb, legacy_check):
    # type: (str, str, str) -> None
    import xlrd

    userMessage("Converting spreadsheet to geodatabase table...")
    #create gdb table
    tn_object = getTNObject(gdb)
    outTable = tn_object.TN_List
    tn_gdb = tn_object.tn_gdb
    LocatorFolder = tn_object.LocatorFolder

    #get the correct address point object
    session = NG911_Session(gdb)
    address_points = session.gdbObject.AddressPoints # Change to OK layer
    a_obj = getFCObject(address_points)

    if not exists(LocatorFolder):
        mkdir(LocatorFolder)

    if not Exists(tn_gdb):
        CreateFileGDB_management(dirname(tn_gdb), basename(tn_gdb))

    if Exists(outTable):
        Delete_management(outTable)

    tname = basename(outTable)
    CreateTable_management(tn_gdb, tname)

    #add fields
    if legacy_check == "true":
        fields = (a_obj.Address, a_obj.AddSuf, a_obj.LgcyPreDir, a_obj.LgcyStreet, a_obj.MSAGCO, a_obj.STATE, "NPA", "NXX", "PHONELINE", "SERVICECLASS")
    else:
        fields = (a_obj.Address, a_obj.AddSuf, a_obj.PreDir, a_obj.Street, a_obj.MSAGCO, a_obj.STATE, "NPA", "NXX", "PHONELINE", "SERVICECLASS")

    # House Number, Suffix, Dir, Street, Community, State, NPA, NXX, Phone Line, Service Class
    colIDlist = (17,18,20,21,22,24,2,3,4,7)

    #add fields
    for field in fields:
        AddField_management(outTable, field, "TEXT", "", "", 254)

    #read xls spreadsheet
    xl_workbook = xlrd.open_workbook(tnxls)
    xl_sheet = xl_workbook.sheet_by_index(0)

    #start at row 1 (maybe? depends on indexing, skip the headers is the goal)
    rowIdx = 1
    endRow = xl_sheet.nrows

    userMessage("This takes a while. It's a great time to take a 10 minute walk or refresh your favorite beverage.")

    #loop through info rows
    with InsertCursor(outTable, fields) as i:
        while rowIdx < endRow:
            if str(rowIdx)[-3:] == "000":
                userMessage("Converted %i / %i rows..." % (rowIdx, endRow))
                # userMessage("Converted " + str(rowIdx) + " spreadsheet records so far...")

            # if rowIdx == endRow/2:
            #     userMessage("Have you backed up your GIS data with DASC recently? Email dasc@kgs.ku.edu for more info!")

            #create list to hold info
            rowToInsertList = []
            #look at just the fields I want to import
            # colIDlist Fields: House Number, Suffix, Dir, Street, Community, State, NPA, NXX, Phone Line, Service Class
            for colID in colIDlist:
                cellval = xl_sheet.cell(rowIdx,colID).value
                rowToInsertList.append(cellval)

            #see if the service class is 8 or V. if it is, skip adding that row
            if rowToInsertList[-1] not in ["8", "V"]:

                #convert list of info to a tuple
                rowToInsert = tuple(rowToInsertList)

                # #create insert cursor
                # i = InsertCursor(outTable,fields)
                #insert the row of info
                i.insertRow(rowToInsert)
                # #clean up
                # del i, rowToInsert, rowToInsertList
            rowIdx = rowIdx + 1

    # split out Street into Street, StreetType, & SufDir
    if legacy_check == "true":
        postRoadFields = [a_obj.LgcyType, a_obj.LgcySufDir]
    else:
        postRoadFields = [a_obj.StreetType, a_obj.SufDir]

    for prf in postRoadFields:
        AddField_management(outTable, prf, "TEXT", "", "", 254)

    if legacy_check == "true":
        postRoadFields.append(a_obj.LgcyStreet)
    else:
        postRoadFields.append(a_obj.Street)

    folder = join(dirname(dirname(realpath(__file__))), "Domains")

    if legacy_check == "true":
        streetSuffixDict = getFieldDomain("LGCYSTREETTYPE", folder).keys() # Changed to OK Fields/layer
        postDirectionalDict = getFieldDomain("LGCYDIRECTION", folder).keys() # Changed to OK Fields/layer
    else:
        streetSuffixDict = getFieldDomain("STREETTYPE", folder).keys() # Changed to OK Fields/layer
        postDirectionalDict = getFieldDomain("DIRECTION", folder).keys() # Changed to OK Fields/layer

    with UpdateCursor(outTable, postRoadFields) as rows:
        check_between = 0
        type_updated = False
        post_updated = False
        for row in rows:

            # split the road name by spaces
            fullNameList = row[2].split()

            # try to skip things that are OLD HIGHWAY/HWY
            strikes = 0
            if "OLD" in fullNameList:
                strikes += 2
            if "HWY" in fullNameList:
                strikes += 1
            if "HIGHWAY" in fullNameList:
                strikes += 1

            # if it has less than three strikes, keep processing the split
            if strikes < 3:

                # set up an iteration to loop through the road name parts
                i = 1
                rd =[fullNameList[0]]
                while i < len(fullNameList):
                    # check to see if the road part is really a street type or post directional
                    if fullNameList[i] not in streetSuffixDict and fullNameList[i] not in postDirectionalDict:
                        rd.append(fullNameList[i])
                        check_between += 1

                    # if it's a street suffix...
                    # 2100 N Ave A Rd S
                    elif fullNameList[i] in streetSuffixDict:

                        # see if it's the last part of the street name or in the middle
                        if i < (len(fullNameList) - 1):
                            # if it's in the middle and the last part is also a street type...
                            if fullNameList[0] in ("AVENUE", "AVE", "ROAD", "RD", "HIGHWAY", "HWY", "SH", "US", "OK", "INT"):
                                rd.append(fullNameList[i])
                                check_between += 1
                            elif fullNameList[i + 1] in streetSuffixDict:
                                # include the middle street suffix as part of the road name
                                rd.append(fullNameList[i])
                                check_between += 1
                            else:
                                # if not, set it as the street suffix since the last part is probable
                                # a post directional
                                if row[0] in ["", " ", None]:
                                    debugMessage("Updating street type \"%s\" to \"%s\"." % (row[0], fullNameList[i]))
                                    row[0] = fullNameList[i]
                                    check_between += 1
                                    type_updated = True
                                    index = i
                                elif row[0] != fullNameList[i]:
                                    if type_updated:
                                        debugMessage("Changing street type \"%s\" to \"%s\". Adding \"%s\" to road name." % (row[0], fullNameList[i], row[0]))
                                        rd.insert(index, row[0])
                                        row[0] = fullNameList[i]
                                        check_between += 1
                                    else:
                                        debugMessage("Street Type field not updated. However, calculated type \"%s\" does NOT match field value \"%s\"." % (fullNameList[i], row[0]))
                                        row[0] = row[0]
                                else:
                                    row[0] = row[0]
                        else:
                            # if it's really the last part, set as the street type
                            if row[0] in ["", " ", None]:
                                debugMessage("Updating street type \"%s\" to \"%s\"." % (row[0], fullNameList[i]))
                                row[0] = fullNameList[i]
                                check_between += 1
                            elif row[0] != fullNameList[i]:
                                if type_updated:
                                    debugMessage("Changing street type \"%s\" to \"%s\". Adding \"%s\" to road name." % (row[0], fullNameList[i], row[0]))
                                    rd.insert(index, row[0])
                                    row[0] = fullNameList[i]
                                    check_between += 1
                                else:
                                    debugMessage("Street Type field not updated. However, calculated type \"%s\" does NOT match field value \"%s\"." % (fullNameList[i], row[0]))
                                    row[0] = row[0]
                            else:
                                row[0] = row[0]

                    # if it's a post directional
                    elif fullNameList[i] in postDirectionalDict:
                        # check for various components that indicate it's not actually a post directional
                        if fullNameList[0] not in ("AVENUE", "AVE", "ROAD", "RD", "HIGHWAY", "HWY", "SH", "US", "OK", "INT"):
                            if row[1] in ["", " ", None]:
                                debugMessage("Updating post-direction \"%s\" to \"%s\"." % (row[1], fullNameList[i]))
                                row[1] = fullNameList[i]
                                check_between += 1
                                post_updated = True
                                index = i
                            elif row[1] != fullNameList[i]:
                                if post_updated:
                                    debugMessage("Changing post direction \"%s\" to \"%s\". Adding \"%s\" to road name." % (row[1], fullNameList[i], row[1]))
                                    rd.insert(index, row[1])
                                    row[1] = fullNameList[i]
                                    check_between += 1
                                else:
                                    debugMessage("Post-directional field not updated. However, calculated direction \"%s\" does NOT match field value \"%s\"." % (fullNameList[i], row[1]))
                                    row[1] = row[1]
                            else:
                                row[1] = row[1]
                        else:
                            rd.append(fullNameList[i])
                            check_between += 1
                    i += 1

            # things with OLD HIGHWAY/HWY will leave the Street field as is for comparison purposes

                    updated_street_name = " ".join(rd)
                    if check_between > 0 and row[2] != updated_street_name:
                        debugMessage("Updating street name \"%s\" to \"%s\"." % (row[2], updated_street_name))
                        row[2] = updated_street_name
                    else:
                        row[2] = row[2]
                    rows.updateRow(row)

    userMessage("Conversion to geodatabase table successful. " + str(endRow-1) + " rows converted. VOIP and test rows were not converted.")


def AddUniqueIDField(outTable, uniqueIDField, tn_for_uniqueid):
    # type: (str, str, Union[str, None]) -> None
    if not fieldExists(outTable, uniqueIDField):
        AddField_management(outTable, uniqueIDField, "TEXT", "", "", 254) #EDIT: changed from 38 to 50 to 254

    wc = uniqueIDField + " is null or " + uniqueIDField + " in ('', ' ')"
    tbl = "tbl"
    MakeTableView_management(outTable, tbl, wc)

    if tn_for_uniqueid is not None:
        CalculateField_management(tbl, uniqueIDField, "!%s! + unicode(!OBJECTID!)" % tn_for_uniqueid, "PYTHON")
    elif fieldExists(outTable, "NXX"):
        CalculateField_management(tbl, uniqueIDField, "!NPA! + !NXX! + !PHONELINE!", "PYTHON")
    else:
        CalculateField_management(tbl, uniqueIDField, "uniqueID() + unicode(!OBJECTID!)", "PYTHON", "def uniqueID():\\n  x = '%d' % time.time()\\n  str(x)\\n  return x")


def geocodeTable(gdb, legacy_check, tn_for_uniqueid=None):
    # type: (str, str, Union[str, None]) -> None
    #geocode addresses
    tn_object = getTNObject(gdb)
    tname = tn_object.TN_List
    uniqueFieldID = tn_object.UNIQUEID

    session = NG911_Session(gdb)
    gdb_obj = session.gdbObject
    add_obj = getFCObject(gdb_obj.AddressPoints)

    #add unique ID to TN List table
    AddUniqueIDField(tname, uniqueFieldID, tn_for_uniqueid)

    if legacy_check == "true":
        addy_field_list = ["NAME_COMPARE"] + add_obj.LGCYNAME_FIELDS[1:]
    else:
        addy_field_list = ["NAME_COMPARE"] + add_obj.FULLNAME_FIELDS[1:]

    launch_compare(gdb, tname, add_obj.Address, add_obj.MSAGCO, addy_field_list, True, legacy_check) # Changed to OK Fields/layer

    #see if any records did not match
    wc = "MATCH <> 'M'"
    lyr = "lyr"
    MakeTableView_management(tname, lyr, wc)

    rCount = getFastCount(lyr)
    if rCount > 0:
        userMessage("Geocoding complete. " + str(rCount) + " records did not geocode. Processing results...")
        userMessage("Results processed. Please see results in " + tname)
    else:
        userMessage("Geocoding complete. All records geocoded successfully.")

    Delete_management(lyr)

def main():

    tnxls = GetParameterAsText(0)
    gdb = GetParameterAsText(1)
    legacy_check = GetParameterAsText(2)

    addy_fc = join(gdb, "NG911", "ADDRESS_POINT") # Changed to OK Fields/layer
    rd_fc = join(gdb, "NG911", "ROAD_CENTERLINE") # Changed to OK Fields/layer

    # turn off editor tracking
    # DisableEditorTracking_management(addy_fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")
    # DisableEditorTracking_management(rd_fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")

    #prep TN list
    prepXLS(tnxls, gdb, legacy_check)

    #geocode addresses
    geocodeTable(gdb, legacy_check, None)

    # turn editor tracking back on
    # EnableEditorTracking_management(addy_fc, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields/layer
    # EnableEditorTracking_management(rd_fc, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields/layer


if __name__ == '__main__':
    main()
