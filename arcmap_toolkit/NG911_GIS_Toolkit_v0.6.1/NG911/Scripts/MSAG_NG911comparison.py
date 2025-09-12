#-------------------------------------------------------------------------------
# Name:        MSAG_NG911comparison
# Purpose:     Compares MSAG with the road centerline file
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     26/08/2016
# Modified:    August 03, 2021
# Copyright:   (c) kristen 2016
#-------------------------------------------------------------------------------
from arcpy import (ExcelToTable_conversion, AddJoin_management, RemoveJoin_management,
                MakeTableView_management, MakeFeatureLayer_management,
                AddField_management, CalculateField_management, GetParameterAsText,
                Exists, CopyFeatures_management, CreateFileGDB_management,
                SelectLayerByAttribute_management, Delete_management, 
                CreateTable_management, Statistics_analysis, Merge_management, SetProgressor, SetProgressorPosition,
                SetProgressorLabel, ResetProgressor)
from arcpy.da import SearchCursor, InsertCursor, UpdateCursor
from os import mkdir
from os.path import exists, dirname, basename, join
from time import strftime
from NG911_arcpy_shortcuts import getFastCount

from NG911_GDB_Objects import NG911_Session, getFCObject, NG911_RoadCenterline_Object
from NG911_User_Messages import *



class MSAG_Object(object):
    #good object to have around
    def __init__(self, u_workspace_folder, u_workingGDB, u_workingRoads, u_msag_table,
                u_rc_names, u_rc_merged_msag, u_msag_merged_msag, u_rc_mm_freq, u_msag_mm_freq,
                u_msag_names, u_Dir, u_Street, u_Community, u_ESN, u_Low, u_High):

        self.workspace_folder = u_workspace_folder
        self.workingGDB = u_workingGDB
        self.workingRoads = u_workingRoads
        self.msag_table = u_msag_table
        self.rc_names = u_rc_names
        self.rc_merged_msag = u_rc_merged_msag
        self.msag_merged_msag = u_msag_merged_msag
        self.rc_mm_freq = u_rc_mm_freq
        self.msag_mm_freq = u_msag_mm_freq
        self.msag_names = u_msag_names
        self.Dir = u_Dir
        self.Street = u_Street
        self.Community = u_Community
        self.ESN = u_ESN
        self.Low = u_Low
        self.High = u_High


def getMSAGObject(gdb, today):
    #too many things to remember, needed an object
    workspace_folder = join(dirname(gdb), "MSAG_analysis_" + basename(gdb.replace(".gdb","")))
    workingGDB = join(workspace_folder, "MSAG_analysis_" + basename(gdb))
    workingRoads = join(workingGDB, "ROAD_CENTERLINE") # Changed to OK Fields/Layer
    msag_table = join(workingGDB, "MSAG_" + today)
    rc_names = workingRoads + "_NAMES"
    msag_names = msag_table + "_NAMES"
    rc_merged_msag = workingRoads + "_MERGED_MSAG"
    msag_merged_msag = msag_table + "_MERGED_MSAG"
    rc_mm_freq = rc_merged_msag + "_freq"
    msag_mm_freq = msag_merged_msag + "_freq"
    MSAG_Default = MSAG_Object(workspace_folder, workingGDB, workingRoads, msag_table,
        rc_names, rc_merged_msag, msag_merged_msag, rc_mm_freq, msag_mm_freq, msag_names,
        "Dir", "Street", "Community", "ESN", "Low", "High")
    return MSAG_Default

def ListFieldNames(item):
    #create a list of field names
    from arcpy import ListFields
    fields = ListFields(item)
    fieldList = []
    for f in fields:
        fieldList.append(f.name.upper())
    return fieldList

def fieldExists(fc, fieldName):
    exists = False
    fields = ListFieldNames(fc)
    if fieldName in fields:
        exists = True
    return exists

# def userMessage(msg):
#     AddMessage(msg)
#     print(msg)

def makeFriendlyRangeMsg(reporting):
    #turns a list of ranges into a printable format
    msg = ""
    for pair in reporting:
        if len(pair) == 2:
            low = pair[0]
            high = pair[1]
            if low != high:
                msg += "Rng: " + str(low) + "-" + str(high) + ", "
            else:
                msg += "Val: " + str(pair[0]) + ", "

    msg = msg[0:-2]
    return msg

def getRanges(data):
    #from http://stackoverflow.com/questions/2361945/detecting-consecutive-integers-in-a-list
    from itertools import groupby
    from operator import itemgetter
    listOfLists = []
    #create lists of consecutive numbers
    for k, g in groupby(enumerate(data), lambda i_x: i_x[0]-i_x[1]):
        floob = list(map(itemgetter(1), g))
        #add the low & high of the range to the list o/ lists
        listOfLists.append([floob[0], floob[len(floob)-1]])

    return listOfLists

def prepRoads(msag_object, gdb, field, use_legacy):
    """

    Copies a subset of the road centerline feature class to the MSAG working geodatabase where records with null values
    for both MSAGComm_L and MSAGComm_R have been filtered out.

    Creates and computes the fields Compare_L, Compare_R, L_R_SAME for this new working feature class.

    Values of Compare_L and Compare_R consist of a concatenation of several name-related fields.

    Parameters
    ----------
    msag_object : MSAG_Object
        MSAG Object containing workingRoads attribute
    gdb : str
        Fullpath to NG911 geodatabase
    field : str
        "COMPARE"
    use_legacy : bool
        Whether or not to use legacy fields

    Returns
    -------
    None
    """
    workingRoads = msag_object.workingRoads
    session = NG911_Session(gdb)
    gdb_object = session.gdbObject
    rcl_path = gdb_object.RoadCenterline
    rcl_object = getFCObject(rcl_path)  # type: NG911_RoadCenterline_Object

    # Removes the objects where MSAGComm_L and MSAGComm_R are null
    wc = "%s is not null OR %s is not null" % (rcl_object.MSAGCO_L, rcl_object.MSAGCO_R)
    wc2 = "%s is null AND %s is null" % (rcl_object.MSAGCO_L, rcl_object.MSAGCO_R)
    fl = "fl"
    cnt = "cnt"
    MakeFeatureLayer_management(rcl_path, fl, wc)
    MakeFeatureLayer_management(rcl_path, cnt, wc2)
    remove_count = getFastCount(cnt)
    userMessage("%i road centerline objects have null MSAGComm attributes and will be removed from MSAG Comparison analysis." % remove_count)
    if not Exists(workingRoads):
        CopyFeatures_management(fl, workingRoads)  # Changed to OK Fields/Layer
        userMessage("Copied roads")
    Delete_management(fl)

    # prep roads
    road_fields = {field + "_L": 250, field + "_R": 250, "L_R_SAME": 1}
    for k in road_fields:
        if not fieldExists(workingRoads, k):
            AddField_management(workingRoads, k, "TEXT", "", "", road_fields[k])

    # replace nulls in working MSAG road centerline
    if use_legacy:
        fields_with_nulls = [rcl_object.LgcyPreDir, rcl_object.LgcyType]
    else:
        fields_with_nulls = [rcl_object.PreDir, rcl_object.StreetType]  # Changed to OK Fields/Layer

    for fwn in fields_with_nulls:
        wcf = fwn + " is null"
        fl = "fl"
        MakeFeatureLayer_management(workingRoads, fl, wcf)
        CalculateField_management(fl, fwn, "''", "PYTHON")
        Delete_management(fl)

    if use_legacy:
        left_fields = [field + "_L"] + rcl_object.LGCYNAME_FIELDS[1:] + [rcl_object.MSAGCO_L, rcl_object.ESN_L]
        right_fields = [field + "_R"] + rcl_object.LGCYNAME_FIELDS[1:] + [rcl_object.MSAGCO_R, rcl_object.ESN_R]
    else:
        left_fields = [field + "_L"] + rcl_object.FULLNAME_FIELDS[1:] + [rcl_object.MSAGCO_L, rcl_object.ESN_L]
        right_fields = [field + "_R"] + rcl_object.FULLNAME_FIELDS[1:] + [rcl_object.MSAGCO_R, rcl_object.ESN_R]

    with UpdateCursor(workingRoads, left_fields) as left_cursor:
        for row in left_cursor:
            for i in range(1, len(left_fields)):
                if unicode(row[i]).upper() in ["NONE", "", " "]:
                    row[i] = " "
            concatenated_string = "".join([val for val in left_fields[1:-2]])  # Compute first part of compare field
            row[0] = (u"%s|%s|%s" % (concatenated_string, row[-2], row[-1])).replace(" ", "").upper()
            left_cursor.updateRow(row)

    with UpdateCursor(workingRoads, right_fields) as right_cursor:
        for row in right_cursor:
            for i in range(1, len(right_fields)):
                if unicode(row[i]).upper() in ["NONE", "", " "]:
                    row[i] = " "
            concatenated_string = "".join([val for val in right_fields[1:-2]])  # Compute first part of compare field
            row[0] = (u"%s|%s|%s" % (concatenated_string, row[-2], row[-1])).replace(" ", "").upper()
            right_cursor.updateRow(row)

    #calculate fields to hold directionally appropriate full street name, MSAGComm & Esn
    # FOLLOWING 2 LINES REPLACED WITH UPDATECURSOR ABOVE
    # CalculateField_management(workingRoads, field+"_L", "(!PreDir!+!Street!+!StreetType!+'|'+!MSAGComm_L!+'|'+!Esn_L!).replace(' ','').upper()", "PYTHON") # Changed to OK Fields/Layer
    # CalculateField_management(workingRoads, field+"_R", "(!PreDir!+!Street!+!StreetType!+'|'+!MSAGComm_R!+'|'+!Esn_R!).replace(' ','').upper()", "PYTHON") # Changed to OK Fields/Layer

##    chars = r'"/\[]{}-.,?;:`~!@#$%^&*()' + "'"
##    for char in chars:
    CalculateField_management(workingRoads, field+"_L", "!" + field + "_L!.replace(" + "'" + '"' + "'" + ",'')", "PYTHON")
    CalculateField_management(workingRoads, field+"_R", "!" + field + "_R!.replace(" + "'" + '"' + "'" + ",'')", "PYTHON")
    CalculateField_management(workingRoads, field+"_L", "!" + field + "_L!.replace(" + '"' + "'" + '"' + ",'')", "PYTHON")
    CalculateField_management(workingRoads, field+"_R", "!" + field + "_R!.replace(" + '"' + "'" + '"' + ",'')", "PYTHON")

    #record L/R same status
    wc_list = {"COMPARE_L = COMPARE_R": "'Y'", "L_R_SAME is null":"'N'"}
    for wc in wc_list:
        wr = "wr"
        exp = wc_list[wc]
        MakeFeatureLayer_management(workingRoads, wr, wc)
        CalculateField_management(wr, "L_R_SAME", exp, "PYTHON")
        Delete_management(wr)

    userMessage("Prepped roads for analysis")

def checkField(table, val):
    # if "Low" and "High" don't exist in the table, find some good candidates
    if not fieldExists(table, val):
        val = ""
        fields = ListFieldNames(table)
        for f in fields:
            if val.upper() in f.upper():
                val = f
    return val

def prepMSAG(msag_object, msag, field):
    """
    Creates High and Low for msag_table in the MSAG Object.

    Parameters
    ----------
    msag_object : MSAG_Object
        MSAG Object containint msag_table attribute
    msag : str
        Fullpath to MSAG excel file
    field : str
        COMPARE field

    Returns
    -------
    list of str
        Low and high fields for MSAG
    """
    msag_table = msag_object.msag_table

    #import msag to table
    if Exists(msag_table):
        Delete_management(msag_table)
    ExcelToTable_conversion(msag, msag_table)
    userMessage("MSAG spreadsheet converted")

    # set low & high fields
    low = msag_object.Low  #checkField(msag_table, msag_object.Low)
    high = msag_object.High  #checkField(msag_table, msag_object.High)
    debugMessage("Low field: %s | High field: %s" % (low, high))

    # error trapping in case the fields didn't get set
    if low == "" or high == "":
        userMessage("MSAG spreadsheet does not have columns with the words 'Low' and:or 'High'. Please edit the spreadsheet so two columns names contains the words 'Low' and 'High'.")
        exit()

    #add comparison fields
    if not fieldExists(msag_table, field):
        AddField_management(msag_table, field, "TEXT", "", "", 250)

    #calculate msag field to hold dir, street, community & esn
    msag_fields = [field, msag_object.Dir, msag_object.Street, msag_object.Community, msag_object.ESN]
    with UpdateCursor(msag_table, msag_fields) as cursor:
        for row in cursor:
            for i in range(1, len(msag_fields)):
                if unicode(row[i]).upper() in ["NONE", "", " "]:
                    row[i] = " "
            # row[0] = ("%s%s|%s|%s" % (unicode(row[1]), row[2], row[3], unicode(row[4]))).replace(" ", "").upper()
            concatenated_string = "".join([val for val in msag_fields[1:-2]])  # Compute first part of compare field
            row[0] = (u"%s|%s|%s" % (concatenated_string, row[-2], row[-1])).replace(" ", "").upper()
            cursor.updateRow(row)
    # expression = "(str(!Dir!) + !Street! + '|'+ !Community! + '|'+ str(!ESN!)).replace(' ', '').upper()"
    # CalculateField_management(msag_table, field, expression, "PYTHON")

    #remove any strange characters
    CalculateField_management(msag_table, field, "!" + field + "!.replace(" + "'" + '"' + "'" + ",'')", "PYTHON")
    CalculateField_management(msag_table, field, "!" + field + "!.replace(" + '"' + "'" + '"' + ",'')", "PYTHON")

    userMessage("Prepped MSAG for analysis")
    return([low, high])

def insertReports(workingGDB, report, records, high, low):
    #prepare reporting
    report_table = join(workingGDB, "MSAG_reporting")
    if not Exists(report_table):
        CreateTable_management(dirname(report_table), basename(report_table))
    if not fieldExists(report_table, "REPORT"):
        AddField_management(report_table, "REPORT", "TEXT", "", "", 255)
    if not fieldExists(report_table, "COMPARISON"):
        AddField_management(report_table, "COMPARISON", "TEXT", "", "", 50)

    fld = ["REPORT", "COMPARISON"]
    cursor = InsertCursor(report_table, fld)
    for r in records:
        if len(fld) == 2:
            cursor.insertRow((report[0:254], r))

def consolidateMSAG(table, compare_field, hilow_fields):
    '''

    Consolidates "COMPARE_L" and "COMPARE_R" fields into single "COMPARE" field

    Parameters
    ----------
    table : MSAG_Object attribute
        Fullpath to MSAG_Object attribute
    compare_field : str
        COMPARE_L (road) or COMPARE (msag)
    hilow_fields : List of str
        rcl_object.Add_L_From, rcl_object.Add_L_To, rcl_object.Add_R_From, rcl_object.Add_R_To (Road)
        Low, High (MSAG)

    Returns
    -------

    '''
    #Run stats on combine field
    dissolve_names = table + "_NAMES"
    if Exists(dissolve_names):
        Delete_management(dissolve_names)

    #make sure all road segments get represented
    if basename(table) == "ROAD_CENTERLINE": # Changed to OK Standards
        #get all the left side names
        dissolve_left = table + "_NAMES_L"
        if Exists(dissolve_left):
            Delete_management(dissolve_left)
        Statistics_analysis(table, dissolve_left, [[compare_field, "COUNT"]], compare_field)
        AddField_management(dissolve_left, "COMPARE", "TEXT", "", "", 100)
        # CalculateField_management(dissolve_left, "COMPARE", "!COMPARE_L!", "PYTHON")
        with UpdateCursor(dissolve_left, ["COMPARE", "COMPARE_L"]) as cursor:
            for row in cursor:
                row[0] = row[1]
                cursor.updateRow(row)

        #get all the ride side names
        dissolve_right = table + "_NAMES_R"
        if Exists(dissolve_right):
            Delete_management(dissolve_right)
        Statistics_analysis(table, dissolve_right, [["COMPARE_R", "COUNT"]], "COMPARE_R")
        AddField_management(dissolve_right, "COMPARE", "TEXT", "", "", 100)
        # CalculateField_management(dissolve_right, "COMPARE", "!COMPARE_R!", "PYTHON")
        with UpdateCursor(dissolve_right, ["COMPARE", "COMPARE_R"]) as cursor:
            for row in cursor:
                row[0] = row[1]
                cursor.updateRow(row)

        #put both tables into one
        dissolve_all = table + "_NAMES_A"
        if Exists(dissolve_all):
            Delete_management(dissolve_all)
        Merge_management([dissolve_left, dissolve_right], dissolve_all)

        Statistics_analysis(dissolve_all, dissolve_names, [["COMPARE", "COUNT"]], "COMPARE")
        userMessage(basename(table) + " names created")

    else:
        #just run name statistics
        Statistics_analysis(table, dissolve_names, [[compare_field, "COUNT"]], compare_field)
        userMessage(basename(table) + " names created")

    #create table for rc to msag conversion
    NG911_msag = table + "_MERGED_MSAG"
    if not Exists(NG911_msag):
        CreateTable_management(dirname(NG911_msag), basename(NG911_msag))
    fields_dict = {"COMPARE": 100, "Low":10, "High":10}
    for f in fields_dict:
        if not fieldExists(NG911_msag, f):
            AddField_management(NG911_msag, f, "TEXT", "", "", fields_dict[f])

    userMessage("Analyzing name highs and lows...")
    #this needs to be adjusted to account for R & L, or both
    #loop through names
    row_cnt = [val for val in SearchCursor(dissolve_names, "COMPARE")]
    row_len = len(row_cnt)
    SetProgressor("step", "Analyzing name highs and lows...", 0, row_len, 1)

    with SearchCursor(dissolve_names, "COMPARE") as n_rows:
        # i_row = 1
        # checkpoint = 5
        for n_row in n_rows:
            SetProgressorPosition()
            # if float(float(i_row)/float(row_len)/100.0) >= checkpoint:
            #     debugMessage("Loop through name: %i percent done." %checkpoint)
            #     checkpoint += 5
            name = n_row[0]
            #run basic MSAG merge
            if name is not None:
                load_name = "MSAG"
                name_wc = compare_field + " = '" + name + "'"
                if "ROAD_CENTERLINE" in table: # Changed to OK Fields/Layer
                    name_wc = name_wc + " AND L_R_SAME = 'Y'"
                    load_name = "ROAD_CENTERLINE"
                writeSegmentInfo(table, hilow_fields, name_wc, NG911_msag, name)

                SetProgressorLabel("Analyzing lows and highs from %s..." % load_name)

                #run R & L isolated analysis
                if "ROAD_CENTERLINE" in table: # Changed to OK Fields/Layer
                    r_wc = "COMPARE_R = '" + name + "' AND L_R_SAME = 'N'"
                    #rcl_object.Add_L_From, rcl_object.Add_L_To, rcl_object.Add_R_From, rcl_object.Add_R_To, hilow_fields
                    # writeSegmentInfo(table, ("Add_R_From", "Add_R_To"), r_wc, NG911_msag, name)
                    writeSegmentInfo(table, (hilow_fields[2], hilow_fields[3]), r_wc, NG911_msag, name)

                    l_wc = "COMPARE_L = '" + name + "' AND L_R_SAME = 'N'"
                    # writeSegmentInfo(table, ("Add_L_From", "Add_L_To"), l_wc, NG911_msag, name)
                    writeSegmentInfo(table, (hilow_fields[0], hilow_fields[1]), l_wc, NG911_msag, name)

    ResetProgressor()

    del n_row, n_rows

    userMessage("Consolidated MSAG complete for " + basename(table))

def writeSegmentInfo(table, hilow_fields, name_wc, NG911_msag, name):
    '''

    Parameters
    ----------
    table : MSAG_Object attribute
        Fullpath to MSAG_Object attribute
    hilow_fields : List of str
        "Add_L_From", "Add_L_To"; "Add_R_From", "Add_R_To" (road)
        "High", "Low" (msag)
    name_wc : str
        Wherecause
    NG911_msag : str
        Fullpath to RC to MSAG conversion table
    name : str
        COMPARE field from dissolved working road attribute

    Returns
    -------
    None
    '''
    seg_list = []
    hilow_len = len(hilow_fields)
    check_rows = [val for val in SearchCursor(table, hilow_fields, name_wc)]
    row_len = len(check_rows)
    debugMessage("Table: %s" % unicode(table))
    debugMessage("Number of rows to check: %s" % unicode(row_len))
    debugMessage("WC: %s" %unicode(name_wc))
    with SearchCursor(table, hilow_fields, name_wc) as rows:
        i_row = 1
        for row in rows:
            # debugMessage("Create Sorted List: %i, %i" %(i_row, row_len))
            #create sorted list of address components
            field_i = 0
            num_list = []
            between_list = []  # ranges with zeroes removed
            while field_i < hilow_len:
                if row[field_i] is not None and row[field_i] != '':
                    num_list.append(int(row[field_i]))
                field_i += 1
            num_list.sort()

            if num_list != []:
                # # Potential temporary fix for ROAD_CENTERLINE BOTH parity cases
                for i in num_list:
                    if i != 0:
                        between_list.append(i)
                between_list.sort()
                between_len = len(between_list)
                if between_list != [] and between_len > 1:
                    seg_list.append(between_list[0])
                    seg_list.append(between_list[between_len - 1])

                # if num_list[0] == 0 and num_list[1] == 0:
                #     pass
                # else:
                #     #add the high and low to the seg_list
                #     seg_list.append(num_list[0])
                #     seg_list.append(num_list[hilow_len - 1])

            i_row = i_row + 1

    debugMessage("Pre-Sorted Seg List: %s" % unicode(seg_list))

    if seg_list != []:

        pop_list = []

        if "ROAD_CENTERLINE" in basename(table):
            seg_list.sort()
            i = len(seg_list)
            k = 1
            # k = 0

            while k + 1 < i:
                # index 0 will definitely be the low so we don't need to worry about it
                # compare the high of one range with the low of the next
                temp_high = seg_list[k]
                temp_nextLow = seg_list[k + 1]

                if temp_nextLow - temp_high == 1:
                    pop_list.append(temp_high)
                    pop_list.append(temp_nextLow)

                k += 2

        else:
            seg_pairs = []
            for i in range(0, len(seg_list), 2):  # [::2] means count by 2, i.e. get every *other* item in seg_list
                debugMessage("iterator: %s" % unicode(i))
                if i < len(seg_list):
                    seg_pairs.append((seg_list[i], seg_list[i+1]))
            seg_pairs.sort()  # sorts by first item in each tuple

            debugMessage("Seg pairs: %s" % unicode(seg_pairs))

            k = len(seg_pairs)
            j = 0
            msag_seg_list = []
            while j < k:
            # for j in range(0, len(seg_pairs)):
                if j < k - 1:
                    low_first = seg_pairs[j][0]
                    low_second = seg_pairs[j+1][0]
                    high_first = seg_pairs[j][1]
                    high_second = seg_pairs[j+1][1]
                    debugMessage("First low: %s, First high: %s, Second low: %s, Second high: %s" % (str(low_first),str(high_first),str(low_second),str(high_second)))
                    if abs(low_second - low_first) == 1 and abs(high_second - high_first) == 1:
                        # even and odd
                        low_min = min([low_second, low_first])
                        high_max = max([high_second, high_first])
                        msag_seg_list.append(low_min)
                        msag_seg_list.append(high_max)
                        j += 2

                    else:
                        # both or a single even/odd side
                        msag_seg_list.append(low_first)
                        msag_seg_list.append(high_first)
                        j += 1
                elif j == k - 1:
                    low_first = seg_pairs[j][0]
                    high_first = seg_pairs[j][1]
                    msag_seg_list.append(low_first)
                    msag_seg_list.append(high_first)
                    j += 1

            msag_seg_list.sort()
            seg_list = msag_seg_list

                # last pair is a both or single even/odd side and needs to be add to list.


        debugMessage("Pop List: %s" % unicode(pop_list))

        #remove values from list that can be absorbed into others
        if pop_list != []:
            for popIt in pop_list:
                seg_list.remove(popIt)

        debugMessage("New Seg List: %s" % unicode(seg_list))

        count = len(seg_list)
        pair_int = 0
        checkpoint = 25

        #write consolidated records
        while pair_int < count:
            # debugMessage("Consolidate: %i, %i, %f" %(pair_int, count, (float(pair_int)/float(count)*100.0)))
            val_count = float(float(pair_int)/float(count)*100.0)
            if val_count >= checkpoint:
                # debugMessage("Consolidate is %s percent done." %str(checkpoint))
                checkpoint += 25
            cursor = InsertCursor(NG911_msag, ("COMPARE", "LOW", "HIGH"))
            cursor.insertRow((name, seg_list[pair_int], seg_list[pair_int + 1]))
            # cursor.insertRow((name, seg_list[0], seg_list[len(seg_list)-1]))

            pair_int += 2
        # cursor = InsertCursor(NG911_msag, ("COMPARE", "LOW", "HIGH"))
        # cursor.insertRow((name, min(seg_list), max(seg_list)))

            del cursor

def compareMSAGnames(msag_object):
    #compare MSAG segments
    msag_names = msag_object.msag_names
    road_names = msag_object.rc_names
    workingRoads = msag_object.workingRoads

    #add report field
    for tbl in (msag_names, road_names):
        if not fieldExists(tbl, "REPORT"):
            AddField_management(tbl, "REPORT", "TEXT", "", "", 255)

    lyr_msag_names = "lyr_msag_names"
    lyr_road_names = "lyr_road_names"
    MakeTableView_management(msag_names, lyr_msag_names)
    MakeTableView_management(road_names, lyr_road_names)

    #add join
    AddJoin_management(lyr_msag_names, "COMPARE", lyr_road_names, "COMPARE")
    wc_msag_names = basename(road_names) + ".COMPARE is null"

    SelectLayerByAttribute_management(lyr_msag_names, "NEW_SELECTION", wc_msag_names)
    CalculateField_management(lyr_msag_names, "REPORT", "'Does not have a road centerline match'", "PYTHON")

    #find records without a match (MSAG)
    record = [val for val in SearchCursor(lyr_msag_names, (basename(msag_names) + ".COMPARE"), wc_msag_names)]
    record_len = len(record)
    SetProgressor("step", "Finding records with a match (MSAG)...", 0, record_len, 1)
    records = []
    with SearchCursor(lyr_msag_names, (basename(msag_names) + ".COMPARE"), wc_msag_names) as msag_rows:
        for msag_row in msag_rows:
            SetProgressorPosition()
            records.append(msag_row[0])

    ResetProgressor()

    #report issues
    if records != []:
        insertReports(dirname(workingRoads), "Does not have a road centerline match", records, '', '')

    #clean up: remove the join
    RemoveJoin_management(lyr_msag_names)

    #add join other direction
    AddJoin_management(lyr_road_names, "COMPARE", lyr_msag_names, "COMPARE")
    wc_road_names = basename(msag_names) + ".COMPARE is null"

    SelectLayerByAttribute_management(lyr_road_names, "NEW_SELECTION", wc_road_names)
    CalculateField_management(lyr_road_names, "REPORT", "'Does not have an MSAG match'", "PYTHON")

    #find records without a match (Road)
    records = []
    record = [val for val in SearchCursor(lyr_road_names, (basename(road_names) + ".COMPARE"), wc_road_names)]
    record_len = len(record)
    SetProgressor("step", "Finding records with a match (ROAD_CENTERLINE)...", 0, record_len, 1)
    with SearchCursor(lyr_road_names, (basename(road_names) + ".COMPARE"), wc_road_names) as road_rows:
        for road_row in road_rows:
            SetProgressorPosition()
            records.append(road_row[0])

    ResetProgressor()

    #report issues
    if records != []:
        insertReports(dirname(workingRoads), "Does not have an MSAG match", records, '', '')

    #clean up: remove the join
    RemoveJoin_management(lyr_road_names)
    Delete_management(lyr_msag_names)
    Delete_management(lyr_road_names)

def compareMSAGranges(msag_object):
    #loop through road centerline names
    userMessage("Comparing MSAG ranges...")
    rc_merged_msag = msag_object.rc_merged_msag
    msag_merged_msag = msag_object.msag_merged_msag
    rc_mm_freq = msag_object.rc_mm_freq
    msag_mm_freq = msag_object.msag_mm_freq

    #run frequency on merged MSAG names, the ones with one entry in each are an easy comparison
    if not Exists(rc_mm_freq):
        Statistics_analysis(rc_merged_msag, rc_mm_freq, [["COMPARE", "COUNT"]], "COMPARE")
    if not Exists(msag_mm_freq):
        Statistics_analysis(msag_merged_msag, msag_mm_freq, [["COMPARE", "COUNT"]], "COMPARE")

    #next step: join the two frequency tables and select the records where both counts = 1
    r1 = "r"
    m = "m"
    MakeTableView_management(rc_mm_freq, r1)
    MakeTableView_management(msag_mm_freq, m)
    AddJoin_management(r1, "COMPARE", m, "COMPARE", "KEEP_COMMON")

    #compare the segments
    record = [val for val in SearchCursor(r1, (basename(rc_mm_freq) + ".COMPARE"))]
    record_len = len(record)
    SetProgressor("step", "Comparing MSAG to ROAD_CENTERLINE...", 0, record_len, 1)
    with SearchCursor(r1, (basename(rc_mm_freq) + ".COMPARE")) as rows:
        for row in rows:

            SetProgressorPosition()

            wc = "COMPARE = '" + row[0] + "'"

            roadnumbers = []
            with SearchCursor(rc_merged_msag, ("Low", "High"), wc) as r_rows:
                for r_row in r_rows:
                    road_range = list(range(int(r_row[0]), int(r_row[1]) + 1))
                    for rr in road_range:
                        roadnumbers.append(rr)
            msagNumbers = []
            with SearchCursor(msag_merged_msag, ("Low", "High"), wc) as m_rows:
                for m_row in m_rows:
                    msag_range = list(range(int(m_row[0]), int(m_row[1]) + 1))
                    for mm in msag_range:
                        msagNumbers.append(mm)

            if roadnumbers == msagNumbers:
                insertReports(msag_object.workingGDB, "Exact MSAG match", [row[0]], '', '')

            else:
                #this is where we do further investigation, probably with ranges as a tool
                msag_outliers = list(set(roadnumbers) - set(msagNumbers))
                msag_outliers.sort()
                # debugMessage(unicode(msag_outliers))
                reporting = getRanges(msag_outliers)
                if reporting != []:
                    friendly_reporting = makeFriendlyRangeMsg(reporting)
                    insertReports(msag_object.workingGDB, "Not in MSAG- " + friendly_reporting, [row[0]], '', '')

                road_outliers = list(set(msagNumbers) - set(roadnumbers))
                road_outliers.sort()
                reporting2 = getRanges(road_outliers)
                if reporting2 != []:
                    friendly_reporting2 = makeFriendlyRangeMsg(reporting2)
                    insertReports(msag_object.workingGDB, "Not in NG911 road- " + friendly_reporting2, [row[0]], '', '')

    # clean-up: del row, rows, r_row, r_rows, m_row, m_rows
    ResetProgressor()
    del rows
    Delete_management(rc_mm_freq)
    Delete_management(msag_mm_freq)

def main():

    #set variables
    msag = GetParameterAsText(0)
    gdb = GetParameterAsText(1)
    road_flag = GetParameterAsText(2)
    msag_flag = GetParameterAsText(3)
    legacy_flag = GetParameterAsText(4)

    today = strftime('%Y%m%d')
    field = "COMPARE"

    msag_object = getMSAGObject(gdb, today)
    session = NG911_Session(gdb)
    gdb_object = session.gdbObject
    rcl_path = gdb_object.RoadCenterline
    rcl_object = getFCObject(rcl_path)  # type: NG911_RoadCenterline_Object

    #create workspaces- folder
    workspaceFolder = msag_object.workspace_folder
    if not exists(workspaceFolder):
        mkdir(workspaceFolder)

    #create workspaces - gdb in folder
    workingGDB = msag_object.workingGDB
    if not Exists(workingGDB):
        CreateFileGDB_management(workspaceFolder, basename(workingGDB))

    #copy over road centerline
    if road_flag == "true" or not Exists(msag_object.workingRoads):
        if legacy_flag == "true":
            prepRoads(msag_object, gdb, field, True)
        else:
            prepRoads(msag_object, gdb, field, False)
        consolidateMSAG(msag_object.workingRoads, "COMPARE_L", (rcl_object.Add_L_From, rcl_object.Add_L_To, rcl_object.Add_R_From, rcl_object.Add_R_To)) # Changed to OK Fields/Layer
    else:
        userMessage("Road data already converted.")

    #prep msag table
    if msag_flag == "true" or not Exists(msag_object.msag_table):
        fields = prepMSAG(msag_object, msag, field) # [Low, High]
        consolidateMSAG(msag_object.msag_table, "COMPARE", (fields[0],fields[1]))
    else:
        userMessage("MSAG data already converted.")

    #compare msag names
    userMessage("Comparing MSAG segment names...")
    compareMSAGnames(msag_object)

    #compare msag ranges
    compareMSAGranges(msag_object)

    #add reporting
    workingRoads = msag_object.workingRoads
    wr = "wr"
    MakeFeatureLayer_management(workingRoads, wr)

    msag = msag_object.msag_table
    mr = "mr"
    MakeTableView_management(msag, mr)

    #add reporting fields
    f_list = ["REPORT_R", "REPORT_L"]
    for f in f_list:
        if not fieldExists(workingRoads, f):
            AddField_management(workingRoads, f, "TEXT", "", "", 255)

    if not fieldExists(msag, "REPORT"):
        AddField_management(msag, "REPORT", "TEXT", "", "", 255)

    #set up where clauses
    wc_roads = "REPORT not like '%in MSAG%'"
    wc_msag = "REPORT not like '%in NG911%'"

    report_roads = "rr"
    report_msag = "rm"

    reporting = join(workingGDB, "MSAG_reporting")

    #report roads first
    MakeTableView_management(reporting, report_roads, wc_roads)

    #run a join on the road centerline based on the R
    AddJoin_management(wr, "COMPARE_R", report_roads, "COMPARISON")
    CalculateField_management(wr, "ROAD_CENTERLINE.REPORT_R", "!MSAG_reporting.REPORT!", "PYTHON") # Changed to OK Fields/Layer
    RemoveJoin_management(wr)

    #run a join on the road centerline based on the L
    AddJoin_management(wr, "COMPARE_L", report_roads, "COMPARISON")
    CalculateField_management(wr, "ROAD_CENTERLINE.REPORT_L", "!MSAG_reporting.REPORT!", "PYTHON") # Changed to OK Fields/Layer
    RemoveJoin_management(wr)

    # refresh the layer
    Delete_management(wr)
    wr = "wr"
    MakeFeatureLayer_management(workingRoads, wr)

    SelectLayerByAttribute_management(wr, "NEW_SELECTION", "REPORT_R IS NULL")
    CalculateField_management(wr, "REPORT_R", "'Issue with corresponding MSAG range'", "PYTHON")
    SelectLayerByAttribute_management(wr, "NEW_SELECTION", "REPORT_L IS NULL")
    CalculateField_management(wr, "REPORT_L", "'Issue with corresponding MSAG range'", "PYTHON")

    #run a join on the MSAG
    MakeTableView_management(reporting, report_msag, wc_msag)
    AddJoin_management(mr, "COMPARE", report_msag, "COMPARISON")
    CalculateField_management(mr, "MSAG_" + today + ".REPORT", "!MSAG_reporting.REPORT!", "PYTHON")
    RemoveJoin_management(mr)

    SelectLayerByAttribute_management(mr, "NEW_SELECTION", "REPORT IS NULL")
    CalculateField_management(mr, "REPORT", "'Issue with corresponding road centerline range'", "PYTHON")

    #notes- basically the MSAG needs to be fully represented in road centerline
    #my email example is fine
    #flag "inconsistent range"
    #bigger issue is with inconsistent communities and ESN's
    #report what doesn't match, community or ESN or if everything is a mess, inconsistent street names?


if __name__ == '__main__':
    main()
