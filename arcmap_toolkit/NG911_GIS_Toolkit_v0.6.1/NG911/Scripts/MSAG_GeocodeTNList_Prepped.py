#-------------------------------------------------------------------------------
# Name:        MSAG_GeocodeTNList_Prepped
# Purpose:     Geocode a TN list where the full address has already been caclulated
#
# Author:      kristen (KS), Baker(OK), Baird (OK)
#
# Created:     01/08/2016
# Modified:    January 6, 2022
#-------------------------------------------------------------------------------
from arcpy import (Delete_management, AddField_management,
            GetParameterAsText, Exists, CreateTable_management,
            CreateFileGDB_management, DisableEditorTracking_management,
            EnableEditorTracking_management)
from arcpy.da import InsertCursor, UpdateCursor
from NG911_DataCheck import getFieldDomain
from NG911_User_Messages import userMessage, debugMessage
from os.path import join, dirname, basename, exists, realpath
from os import mkdir
from NG911_GDB_Objects import getFCObject, getTNObject, NG911_Session
from MSAG_CheckTNList import geocodeTable

try:
    from typing import Union, List
except:
    pass

def prepXLS(tnxls_sheet, gdb, xls_fields, legacy_check):
    # type: (str, str, List[str], str) -> None
    import xlrd

    userMessage("Converting spreadsheet to geodatabase table...")
    #create gdb table
    tn_object = getTNObject(gdb)
    outTable = tn_object.TN_List
    tn_gdb = tn_object.tn_gdb
    LocatorFolder = tn_object.LocatorFolder

    # get the correct address point object
    session = NG911_Session(gdb)
    address_points = session.gdbObject.AddressPoints  # Change to OK layer
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
        fields = (a_obj.Address, a_obj.AddSuf, a_obj.LgcyPreDir, a_obj.LgcyStreet, a_obj.LgcyType, a_obj.LgcySufDir, a_obj.MSAGCO, tn_object.UNIQUEID)
    else:
        fields = (a_obj.Address, a_obj.AddSuf, a_obj.PreDir, a_obj.Street, a_obj.StreetType, a_obj.SufDir, a_obj.MSAGCO, tn_object.UNIQUEID)

    # [hno, hns, prd, rd, sts, post, msagco, tn]
    colIDlist = ["0", "0", "0", "0", "0", "0", "0", "0"]

    #add fields
    for field in fields:
        AddField_management(outTable, field, "TEXT", "", "", 254)

    #read xls spreadsheet
    tnxls = dirname(tnxls_sheet)
    xl_workbook = xlrd.open_workbook(tnxls)
    xl_sheet = xl_workbook.sheet_by_index(0)
    header_row = xl_sheet.row(0)

    # xls_fields is passed as: [hno, hns, prd, rd, sts, post, msagco, tn]
    for idx, cell_obj in enumerate(header_row):
        val = xl_sheet.cell(0,idx).value
        if val in xls_fields:
            place = xls_fields.index(val)
            colIDlist[place] = idx

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
            #     userMessage("Enjoying our tools? Have suggestions? Email rbaird@odot.org or ebaker@odot.org for more info!")

            #create list to hold info
            rowToInsertList = []
            #look at just the fields I want to import
            for colID in colIDlist:
                if colID != "0":
                    cellval = xl_sheet.cell(rowIdx,colID).value
                    rowToInsertList.append(cellval)
                else:
                    rowToInsertList.append("")

            #convert list of info to a tuple
            rowToInsert = tuple(rowToInsertList)

            #create insert cursor
            # i =
            #insert the row of info
            i.insertRow(rowToInsert)
            #clean up
            # del i, rowToInsert, rowToInsertList

            rowIdx = rowIdx + 1

    # split out Street into Street, StreetType, & SufDir
    folder = join(dirname(dirname(realpath(__file__))), "Domains")
    if legacy_check == "true":
        postRoadFields = [a_obj.LgcyType, a_obj.LgcySufDir, a_obj.LgcyStreet]
        streetSuffixDict = getFieldDomain("LGCYSTREETTYPE", folder).keys()  # Changed to OK Fields/layer
        postDirectionalDict = getFieldDomain("LGCYDIRECTION", folder).keys()  # Changed to OK Fields/layer
    else:
        postRoadFields = [a_obj.StreetType, a_obj.SufDir, a_obj.Street]
        streetSuffixDict = getFieldDomain("STREETTYPE", folder).keys()  # Changed to OK Fields/layer
        postDirectionalDict = getFieldDomain("DIRECTION", folder).keys()  # Changed to OK Fields/layer

    with UpdateCursor(outTable, postRoadFields) as rows:
        check_between = 0
        post_updated = False
        type_updated = False
        for row in rows:
            fullNameList = row[2].split()
            i = 1  # Skip the first word
            rd =[fullNameList[0]]
            while i < len(fullNameList):
                # 2100 N Ave Rd
                if fullNameList[i] not in streetSuffixDict and fullNameList[i] not in postDirectionalDict:
                    # If the current word matches neither a street type nor a direction, include it in the name
                    rd.append(fullNameList[i])
                    check_between += 1
                elif fullNameList[i] in streetSuffixDict:
                    # If the current word matches a street type, set StreetType/LgcyType to the word
                    # UNLESS StreetType/LgcyType already has a value
                    if fullNameList[0] not in ("AVENUE", "AVE", "ROAD", "RD", "HIGHWAY", "HWY", "SH", "US", "OK", "INT"):
                        if row[0] in ["", " ", None]:
                            debugMessage("Updating old street type from \"%s\" to \"%s\"." % (row[0], fullNameList[i]))
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
                        rd.append(fullNameList[i])
                        check_between += 1

                # Example: "2100 N Avenue S" and post-directional field (row[1]) is None in the beginning
                elif fullNameList[i] in postDirectionalDict:
                    # If the current word matches a direction, set SufDir/LgcySufDir to the word
                    # IF AND ONLY IF SufDir/LgcySufDir does not have a value AND the first word is not in the list below
                    # if i < len(fullNameList) - 1:
                    if fullNameList[0] not in ("AVENUE", "AVE", "ROAD", "RD", "HIGHWAY", "HWY", "SH", "US", "OK", "INT"):
                        if row[1] in ["", " ", None]:
                            debugMessage("Updating old post-direction from \"%s\" to \"%s\"." % (row[1], fullNameList[i]))
                            row[1] = fullNameList[i]
                            check_between += 1
                            post_updated = True
                            index = i
                        elif row[1] != fullNameList[i]:
                            if post_updated:
                                debugMessage("Changing post direction \"%s\" to \"%s\". Adding \"%s\" to road name." % (row[1], fullNameList[i], row[1]))
                                # Assume that this is the second directional in the name and therefore is the correct post-directional field and needs to be updated.
                                rd.insert(index, row[1])
                                row[1] = fullNameList[i]
                                check_between += 1
                            else:
                                # Assume that the post-directional field has not been calculated by this script and therefore should not be updated.
                                debugMessage("Post-directional field not updated. However, calculated directional \"%s\" does NOT match field value \"%s\"." % (fullNameList[i], row[1]))
                                row[1] = row[1]
                        else:
                            row[1] = row[1]
                    else:
                        rd.append(fullNameList[i])
                        check_between += 1
                    # elif i == len(fullNameList) - 1:
                    #     if row[1] in ["", " ", None]:
                    #         debugMessage("Updating old post-direction from \"%s\" to \"%s\"." % (row[1], fullNameList[i]))
                    #         row[1] = fullNameList[i]
                    #         check_between += 1
                    #     elif row[1] != fullNameList[i]:
                    #         row[1] = row[1]


                i += 1

            updated_street_name = " ".join(rd)
            if check_between > 0 and row[2] != updated_street_name:
                debugMessage("Updating street name \"%s\" to \"%s\"." % (row[2], updated_street_name))
                row[2] = updated_street_name
            else:
                row[2] = row[2]

            rows.updateRow(row)

    userMessage("Conversion to geodatabase table successful. " + str(endRow-1) + " rows converted.")

def main():

    gdb = GetParameterAsText(0)
    xls = GetParameterAsText(1)
    hno = GetParameterAsText(2)
    hns = GetParameterAsText(3)
    prd = GetParameterAsText(4)
    rd = GetParameterAsText(5)
    sts = GetParameterAsText(6)
    post = GetParameterAsText(7)
    msagco = GetParameterAsText(8)
    tn = GetParameterAsText(9)
    legacy_check = GetParameterAsText(10)

    addy_fc = join(gdb, "NG911", "ADDRESS_POINT") # Changed to OK Fields/layer
    rd_fc = join(gdb, "NG911", "ROAD_CENTERLINE") # Changed to OK Fields/layer

    # turn off editor tracking
    # DisableEditorTracking_management(addy_fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")
    # DisableEditorTracking_management(rd_fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")

    xls_fields = [hno, hns, prd, rd, sts, post, msagco, tn]

    prepXLS(xls, gdb, xls_fields, legacy_check)

    #geocode addresses
    if tn not in ["", " ", None]:
        geocodeTable(gdb, legacy_check, tn)
    else:
        geocodeTable(gdb, legacy_check, None)

    # turn editor tracking back on
    # EnableEditorTracking_management(addy_fc, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields/layer
    # EnableEditorTracking_management(rd_fc, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields/layer

if __name__ == '__main__':
    main()
