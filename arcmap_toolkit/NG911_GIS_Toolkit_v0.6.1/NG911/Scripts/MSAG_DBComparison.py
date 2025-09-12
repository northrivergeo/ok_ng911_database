#-------------------------------------------------------------------------------
# Name:        MSAG_DBComparison
# Purpose:     Compare an address point to the road centerline file
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     10/05/2017
# Modified:	   12/10/2019, June 14, 2021, January 6, 2022
#-------------------------------------------------------------------------------
from NG911_GDB_Objects import getFCObject, NG911_Session
from os import remove
from os.path import join, dirname, exists
from arcpy.da import SearchCursor, UpdateCursor, Editor
from arcpy import (AddField_management,
                    MakeFeatureLayer_management, Delete_management,
                    CalculateField_management, Exists, Merge_management,
                    MakeTableView_management, CopyRows_management,
                    DeleteField_management, SetProgressor, SetProgressorPosition, ResetProgressor)
from NG911_arcpy_shortcuts import getFastCount, fieldExists, ListFieldNames
import time
from NG911_User_Messages import *

try:
    from typing import List, Tuple
except:
    pass

def prep_roads_for_comparison(rd_fc, name_field, code_fields, city_fields, field_list):
    # type: (str, str, List[str], List[str], List[str]) -> None
    """Calculates name_field and code_fields. A label is calculated and assigned to name_field. A very strange code
    is computed and assigned to each field in code_fields.

    When called from checkRCLMATCH, this function calculates NAME_COMPARE, CODE_COMPARE_L, and CODE_COMPARE_R.

    Parameters
    ----------
    rd_fc : str
        Path to a table/feature class of either road centerline features (which must be named "rcTable") OR address
        point features (which must be named "apTable")
    name_field : str
        Name of the field to which a calculated label will be assigned
    code_fields : list of str
        The names of the code fields for each side, ending in "_L" and "_R"
    city_fields : list of str
        The names of the city fields for each side, ending in "_L" and "_R". Used to calculate values for the respective
        side field in code_fields.
    field_list : list of str
        A list of fields used to calculate the fullname, which is assigned to name_field
    """

    # calculate values for NAME_OVERLAP field
    # field_list = ["NAME_COMPARE", "PreDir", "PreTypeSep", "Street", "StreetType", "SufDir", "SufMod"]
    fields1 = tuple(field_list)  # type: Tuple[str]

    # add the NAME_OVERLAP field
    if not fieldExists(rd_fc, name_field):
        AddField_management(rd_fc, name_field, "TEXT", "", "", 254)  # TODO: Import field details from text file

    if "rcTable" in rd_fc:
        field_list.append("NGUID_RDCL")
        i = field_list.index("NGUID_RDCL")
    elif "apTable" in rd_fc:
        if "NGUID_RDCL" in field_list:
            field_list.remove("NGUID_RDCL")
        field_list.append("NGUID_ADD")
        i = field_list.index("NGUID_ADD")
    else:
        i = 0

##    AddMessage("Query field list:" + ", ".join(field_list))

    if "in_memory" not in rd_fc:

        # start edit session
        working_gdb = dirname(rd_fc)
        if working_gdb[-3:] not in "gdb":  # TODO: Should this be changed to accomodate geodatabases (e.g. Oracle) that do not end in "gdb"?
            working_gdb = dirname(dirname(rd_fc))
        if r"Database Servers\GISS01_SQLEXPRESSGIS.gds" in working_gdb:
            working_gdb =  r"Database Servers\GISS01_SQLEXPRESSGIS.gds\KSNG911S(VERSION:dbo.DEFAULT)"  # TODO: String seems Kansas-specific; determine whether to replace string or delete conditional

        # made some changes to account for Butler Co's SDE gdb
    ##    AddMessage(working_gdb)
        edit = Editor(working_gdb)
        if "dbo.DEFAULT" not in working_gdb:
            edit.startEditing(with_undo=False, multiuser_mode=False)
        else:
            edit.startEditing(with_undo=False, multiuser_mode=True)
    else:
        edit = None

    # run update cursor
    # fields1 = {"NAME_COMPARE", "PreDir", "PreTypeSep", "Street", "StreetType", "SufDir", "SufMod"}
    with UpdateCursor(rd_fc, fields1) as rows:
        for row in rows:
            field_count = len(fields1)  # type: int
            start_int = 1  # type: int
            fullname = ""  # type: unicode

            # loop through the fields to see what's null & skip it
            # computes NAME_COMPARE
            while start_int < field_count:
                if row[start_int] is not None:
                    if row[start_int] not in ("", " "):
                        fullname = fullname + "|" + unicode(row[start_int]).strip().upper()  # fullname += "|" + [field contents] as uppercase stripped str
                start_int = start_int + 1

            if fullname.find("||") != -1:
                row[0] = fullname.replace("||","|")
                # userMessage("Double pipe replaced with single pipe.")
            else:
                # Assign label to NAME_COMPARE field
                row[0] = fullname

            try:
                # Commit change
                rows.updateRow(row)
            except:
                UserWarning("Error with " + rd_fc + field_list[i] + row[i])

    if edit:
        edit.stopEditing(save_changes=True)

    # clean up all labels
    trim_expression = '" ".join(!' + name_field + '!.split())'
    CalculateField_management(rd_fc, name_field, trim_expression, "PYTHON_9.3")

    # covert labels to road code with MSAG city code
    code_block= """def calc_code(rd, city):
                   b = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10,"K":11,
                        "L":12,"M":13,"N":14,"O":15,"P":16,"Q":17,"R":18,"S":19,"T":20,"U":21,
                        "V":22,"W":23,"X":24,"Y":25,"Z":26," ":27,"0":28,"1":29,"2":30,"3":31,"4":32,"5":33,"6":34,"7":35,
                        "8":36,"9":37,"|":38,"-":39,"'":40,";":43}
                   tot = 0
                   if city is None or city in ('', ' ', '  '):
                       city = "   "
                   for name in rd, city:
                       name = name.strip().upper()
                       while len(name) < 3:
                           name = name + " "
                       list_len = len(name)
                       k = 0
                       while k < list_len:
                           try:
                               chars1 = b[name[k].upper()]
                           except:
                               chars1 = 42
                           if 0 < k + 1 < list_len:
                               try:
                                   chars1 = chars1 * k * b[name[k+1].upper()]
                               except:
                                   chars1 = chars1 * k * 42
                           else:
                               try:
                                   chars1 = chars1 * b[name[list_len - 1]]
                               except:
                                   chars1 = chars1 * 42
                           tot += chars1
                           k += 1

                       # make sure all the values actually work
                       if name[0].upper() not in b:
                           a0 = 42
                       else:
                           a0 = b[name[0].upper()]

                       if name[1].upper() not in b:
                           a1 = 43
                       else:
                           a1 = b[name[1].upper()]

                       if name[2].upper() not in b:
                           a2 = 44
                       else:
                           a2 = b[name[2].upper()]

                       if name[-1].upper() not in b:
                           a3 = 45
                       else:
                           a3 = b[name[-1].upper()]

                       c = len(rd) + len(city)
                       tot = tot * c - a1 + a2 - a3

                   return tot"""

    for code_field in code_fields:
        i = code_fields.index(code_field)
        city_field = city_fields[i]
        # add the NAME_OVERLAP field
        # (From CheckRCLMATCH): Create CODE_COMPARE_X field
        if not fieldExists(rd_fc, code_field):
            AddField_management(rd_fc, code_field, "LONG")

        # (From CheckRCLMATCH): Calculate the CODE_COMPARE_X field value using NAME_COMPARE and MSAGComm_X with code_block
        # Example call from CheckRCLMATCH:
        # CalculateField_management([ROAD_CENTERLINE in_memory table], "CODE_COMPARE_X", calc_code( !NAME_COMPARE!.upper(), !MSAGComm_X! ), code_block)
        CalculateField_management(rd_fc, code_field, "calc_code( !" + name_field + "!.upper(), !" + city_field + "! )", "PYTHON_9.3", code_block)


def ap_compare(hno, hno_code, ap_fc):
    # type: (str, str, str) -> Union[str, unicode]
    segid_list = []

    wc = "CODE_COMPARE = %s AND Address = %s" % (unicode(hno_code), unicode(hno)) # Changed to OK Fields/Layer
##    wc = "CODE_COMPARE = " + str(hno_code) + " AND Address = " + str(hno)

    a = "a"
    MakeFeatureLayer_management(ap_fc, a, wc)
    count = getFastCount(a)

    if count > 0:
        # search cursor to get all ties

        segid_field = "NGUID_ADD"

        rd_fields = (segid_field)

        with SearchCursor(ap_fc, rd_fields, wc) as r_rows:
            for r_row in r_rows:
                segid_list.append(r_row[0])

            try:
                del r_row, r_rows
            except:
                pass

        del rd_fields

    if len(segid_list) == 1:
        segid = segid_list[0]
    elif len(segid_list) == 0:
        segid = ""
    else:
        segid = "TIES"

    Delete_management(a)
    del segid_list

    return segid


def db_compare(hno, hno_code, tempTable, addid, txt, idField):
    # type: (int, str, str, str,  str, str) -> List[Union[str, unicode]]
    # see if the text file exists already
    if exists(txt):
        method = "a"
    else:
        method = "w"

    # see if the address number is even or odd
    if hno & 1: # bitwise operation to test for odd/even (thanks to Sherry M.)
        parity = "('O','B')"
    else:
        parity = "('E','B')"

    segid_list = []

    # set up wc to query the road table accordingly
    wc = "CODE_COMPARE = " + unicode(hno_code) + " AND PARITY in " + parity

    # if the version is 2.1, make sure only the AUTH = Y records are used
    if fieldExists(tempTable, "PROV"):
        wc = wc + " AND PROV = 'Y'"

    segid_field = "NGUID_RDCL"
    side = "N"

    rd_fields = [segid_field, "FROM_ADD", "TO_ADD", "RCLSide", "PARITY"]

    with SearchCursor(tempTable, rd_fields, wc) as r_rows:
        for r_row in r_rows:

            # set the counter for the range, it'll usually be 2
            range_counter = 2
            if r_row[4] == "B": # if the range is B (both sides), the counter = 1
                range_counter = 1

            # get the range by 2s
            sideRange = list(range(r_row[1], r_row[2] + range_counter, range_counter))

            # if the range was high to low, flip it
            if sideRange == []:
                sideRange = list(range(r_row[2], r_row[1] + range_counter, range_counter))

            if hno in sideRange:
                if r_row[0] is None:
                    AddWarning("An NGUID_RDCL value is blank/null. Matching records cannot be calculated. Make sure all NGUID_RDCLs are populated and run again.")
                    segid_list.append("NULL_ID")
                else:
                    segid_list.append(r_row[0])
                    # grab the side, I'll reset later if it should be N
                    side = r_row[3]
                    # userMessage("Side that is passed with compare: %s" % side)

        try:
            del r_row, r_rows
        except:
            pass

    # del rd_fields

    if len(segid_list) == 1:
        segid = segid_list[0]
    elif len(segid_list) == 0:
        segid = ""
        side = "N"
    else:
        segids = idField + " " + addid + " TIES WHERE CLAUSE: NGSEGID in ('" + "', '".join(segid_list) + "')\n"
        writeToText(txt, segids, method)
        segid = "TIES"
        side = "N"

    del segid_list
    return [segid, side]


def writeToText(textFile, stuff, method):
    # type: (str, str, str) -> None
    FILE = open(textFile, method)
    FILE.writelines(stuff)
    FILE.close()


def launch_compare(gdb, output_table, HNO, addy_city_field, addy_field_list, queryAP, legacy_check):
    # type: (str, str, object, str, List[str], bool, str) -> None
    # addy_field_list = ["NAME_COMPARE", "PreDir", "PreTypeSep", "Street", "StreetType", "SufDir", "SufMod"]
##    start_time = time.time()
    # rd_fc = join(gdb, "NG911", "ROAD_CENTERLINE")  # type: str  # Changed to OK Fields/layer
    # ap_fc = join(gdb, "NG911", "ADDRESS_POINT")  # type: str  # Changed to OK Fields/layer
    session = NG911_Session(gdb)
    gdb_object = session.gdbObject
    rd_fc = gdb_object.RoadCenterline
    ap_fc = gdb_object.AddressPoints

    name_field = "NAME_COMPARE"  # type: str
    code_field = "CODE_COMPARE"  # type: str
    city_field = "MSAGComm"  # type: str  # Changed to OK Fields
    rd_object = getFCObject(rd_fc)
    ap_object = getFCObject(ap_fc)

    # flip switch for gdb instead of in_memory
    storage = "in_memory"
    #storage = gdb

    # In TN Tools this prep is used for the TN spreadsheets
    prep_roads_for_comparison(
        rd_fc=output_table,
        name_field=name_field,
        code_fields=[code_field],
        city_fields=[addy_city_field],
        field_list=addy_field_list
    )

    # prep road centerline with concatenated label field
    if legacy_check == "true":
        road_field_list = ["NAME_COMPARE"] + rd_object.LGCYNAME_FIELDS[1:]
    else:
        road_field_list = ["NAME_COMPARE"] + rd_object.FULLNAME_FIELDS[1:]
    version = rd_object.GDB_VERSION

    # copy the roads to a table for comparison
    rc_table_view = "rc_table_view"

    rt = join(storage, "rcTable" + version)
    if Exists(rt):
        Delete_management(rt)

    if queryAP:
        wc = "SUBMIT = 'Y' AND (%s is not null OR %s is not null)" % (rd_object.MSAGCO_L, rd_object.MSAGCO_R)
        MakeTableView_management(rd_fc, rc_table_view, wc)
        CopyRows_management(rc_table_view, rt)
        prep_roads_for_comparison(rt, name_field, [code_field + "_L", code_field + "_R"], [city_field + "_L", city_field + "_R"], road_field_list)
    else:
        wc = "SUBMIT = 'Y'"
        MakeTableView_management(rd_fc, rc_table_view, wc)
        CopyRows_management(rc_table_view, rt)
        prep_roads_for_comparison(rt, name_field, [code_field + "_L", code_field +"_R"], [city_field + "_L", city_field + "_R"], road_field_list)

    # prep address points with concatenated label field if necessary
    if queryAP:
        if legacy_check == "true":
            addy_field_list1 = ["NAME_COMPARE"] + ap_object.LGCYNAME_FIELDS[1:]
        else:
            addy_field_list1 = ["NAME_COMPARE"] + ap_object.FULLNAME_FIELDS[1:]
        prep_roads_for_comparison(ap_fc, name_field, [code_field], [city_field], addy_field_list1)

    # if version == "20":
    #
    #     l_field_info = """OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;DiscrpAgID DiscrpAgID HIDDEN NONE;RevDate RevDate HIDDEN NONE;
    #     EFF_DATE EFF_DATE HIDDEN NONE;EXP_DATE EXP_DATE HIDDEN NONE;NGSEGID NGSEGID VISIBLE NONE;STATE_L STATE_L HIDDEN NONE;
    #     STATE_R STATE_R HIDDEN NONE;COUNTY_L COUNTY_L HIDDEN NONE;COUNTY_R COUNTY_R HIDDEN NONE;MUNI_L MUNI_L HIDDEN NONE;
    #     MUNI_R MUNI_R HIDDEN NONE;Add_L_From FROM_ADD VISIBLE NONE;Add_L_To TO_ADD VISIBLE NONE;Add_R_From Add_R_From HIDDEN NONE;
    #     Add_R_To Add_R_To HIDDEN NONE;PARITY_L PARITY VISIBLE NONE;PARITY_R PARITY_R HIDDEN NONE;POSTCO_L POSTCO_L HIDDEN NONE;
    #     POSTCO_R POSTCO_R HIDDEN NONE;ZIP_L ZIP_L HIDDEN NONE;ZIP_R ZIP_R HIDDEN NONE;ESN_L ESN_L HIDDEN NONE;ESN_R ESN_R HIDDEN NONE;
    #     MSAGCO_L MSAGCO VISIBLE NONE;MSAGCO_R MSAGCO_R HIDDEN NONE;PreDir PreDir HIDDEN NONE;PreTypeSep PreTypeSep HIDDEN NONE;Street Street HIDDEN NONE;
    #     StreetType StreetType HIDDEN NONE;SufDir SufDir HIDDEN NONE;SufMod SufMod HIDDEN NONE;SPDLIMIT SPDLIMIT HIDDEN NONE;ONEWAY ONEWAY HIDDEN NONE;
    #     RDCLASS RDCLASS HIDDEN NONE;RevEditor RevEditor HIDDEN NONE;LABEL LABEL HIDDEN NONE;ELEV_F ELEV_F HIDDEN NONE;
    #     ELEV_T ELEV_T HIDDEN NONE;SURFACE SURFACE HIDDEN NONE;STATUS STATUS HIDDEN NONE;BoundLane BoundLane HIDDEN NONE;
    #     LRSKEY LRSKEY HIDDEN NONE;TopoExcept TopoExcept HIDDEN NONE;SUBMIT SUBMIT HIDDEN NONE;Comment Comment HIDDEN NONE;
    #     UNINC_L UNINC_L HIDDEN NONE;UNINC_R UNINC_R HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;ESN_C ESN_C HIDDEN NONE;
    #     NAME_COMPARE NAME_COMPARE VISIBLE NONE;CODE_COMPARE_L CODE_COMPARE VISIBLE NONE;CODE_COMPARE_R CODE_COMPARE_R HIDDEN NONE"""
    #
    #     r_field_info = """OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;DiscrpAgID DiscrpAgID HIDDEN NONE;RevDate RevDate HIDDEN NONE;
    #     EFF_DATE EFF_DATE HIDDEN NONE;EXP_DATE EXP_DATE HIDDEN NONE;NGSEGID NGSEGID VISIBLE NONE;STATE_L STATE_L HIDDEN NONE;
    #     STATE_R STATE_R HIDDEN NONE;COUNTY_L COUNTY_L HIDDEN NONE;COUNTY_R COUNTY_R HIDDEN NONE;MUNI_L MUNI_L HIDDEN NONE;
    #     MUNI_R MUNI_R HIDDEN NONE;Add_L_From Add_L_From HIDDEN NONE;Add_L_To Add_L_To HIDDEN NONE;Add_R_From FROM_ADD VISIBLE NONE;
    #     Add_R_To TO_ADD VISIBLE NONE;PARITY_L PARITY_L HIDDEN NONE;PARITY_R PARITY VISIBLE NONE;POSTCO_L POSTCO_L HIDDEN NONE;
    #     POSTCO_R POSTCO_R HIDDEN NONE;ZIP_L ZIP_L HIDDEN NONE;ZIP_R ZIP_R HIDDEN NONE;ESN_L ESN_L HIDDEN NONE;ESN_R ESN_R HIDDEN NONE;
    #     MSAGCO_L MSAGCO_L HIDDEN NONE;MSAGCO_R MSAGCO VISIBLE NONE;PreDir PreDir HIDDEN NONE;PreTypeSep PreTypeSep HIDDEN NONE;Street Street HIDDEN NONE;
    #     StreetType StreetType HIDDEN NONE;SufDir SufDir HIDDEN NONE;SufMod SufMod HIDDEN NONE;SPDLIMIT SPDLIMIT HIDDEN NONE;ONEWAY ONEWAY HIDDEN NONE;
    #     RDCLASS RDCLASS HIDDEN NONE;RevEditor RevEditor HIDDEN NONE;LABEL LABEL HIDDEN NONE;ELEV_F ELEV_F HIDDEN NONE;
    #     ELEV_T ELEV_T HIDDEN NONE;SURFACE SURFACE HIDDEN NONE;STATUS STATUS HIDDEN NONE;BoundLane BoundLane HIDDEN NONE;
    #     LRSKEY LRSKEY HIDDEN NONE;TopoExcept TopoExcept HIDDEN NONE;SUBMIT SUBMIT HIDDEN NONE;Comment Comment HIDDEN NONE;
    #     UNINC_L UNINC_L HIDDEN NONE;UNINC_R UNINC_R HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;ESN_C ESN_C HIDDEN NONE;
    #     NAME_COMPARE NAME_COMPARE VISIBLE NONE;CODE_COMPARE_L CODE_COMPARE_L HIDDEN NONE;CODE_COMPARE_R CODE_COMPARE VISIBLE NONE"""

    # elif version == "21":
        # l_field_info = """OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;DiscrpAgID DiscrpAgID HIDDEN NONE;RevDate RevDate HIDDEN NONE;
        # EFF_DATE EFF_DATE HIDDEN NONE;EXP_DATE EXP_DATE HIDDEN NONE;NGSEGID NGSEGID VISIBLE NONE;STATE_L STATE_L HIDDEN NONE;
        # STATE_R STATE_R HIDDEN NONE;COUNTY_L COUNTY_L HIDDEN NONE;COUNTY_R COUNTY_R HIDDEN NONE;MUNI_L MUNI_L HIDDEN NONE;
        # MUNI_R MUNI_R HIDDEN NONE;Add_L_From FROM_ADD VISIBLE NONE;Add_L_To TO_ADD VISIBLE NONE;Add_R_From Add_R_From HIDDEN NONE;
        # Add_R_To Add_R_To HIDDEN NONE;PARITY_L PARITY VISIBLE NONE;PARITY_R PARITY_R HIDDEN NONE;POSTCO_L POSTCO_L HIDDEN NONE;
        # POSTCO_R POSTCO_R HIDDEN NONE;ZIP_L ZIP_L HIDDEN NONE;ZIP_R ZIP_R HIDDEN NONE;ESN_L ESN_L HIDDEN NONE;ESN_R ESN_R HIDDEN NONE;
        # MSAGCO_L MSAGCO VISIBLE NONE;MSAGCO_R MSAGCO_R HIDDEN NONE;PreDir PreDir HIDDEN NONE;PreTypeSep PreTypeSep HIDDEN NONE;Street Street HIDDEN NONE;
        # StreetType StreetType HIDDEN NONE;SufDir SufDir HIDDEN NONE;SufMod SufMod HIDDEN NONE;SPDLIMIT SPDLIMIT HIDDEN NONE;ONEWAY ONEWAY HIDDEN NONE;
        # RDCLASS RDCLASS HIDDEN NONE;RevEditor RevEditor HIDDEN NONE;LABEL LABEL HIDDEN NONE;ELEV_F ELEV_F HIDDEN NONE;
        # ELEV_T ELEV_T HIDDEN NONE;SURFACE SURFACE HIDDEN NONE;STATUS STATUS HIDDEN NONE;BoundLane BoundLane HIDDEN NONE;
        # LRSKEY LRSKEY HIDDEN NONE;TopoExcept TopoExcept HIDDEN NONE;SUBMIT SUBMIT HIDDEN NONE;Comment Comment HIDDEN NONE;
        # UNINC_L UNINC_L HIDDEN NONE;UNINC_R UNINC_R HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;
        # AUTH_L AUTH VISIBLE NONE;AUTH_R AUTH_R HIDDEN NONE;GEOMSAGL GEOMSAGL HIDDEN NONE;GEOMSAGR GEOMSAGR HIDDEN NONE;
        # NAME_COMPARE NAME_COMPARE VISIBLE NONE;CODE_COMPARE_L CODE_COMPARE VISIBLE NONE;CODE_COMPARE_R CODE_COMPARE_R HIDDEN NONE"""

    # TODO: Consider replacing below l_field_info and r_field_info assignments with arcpy field mappings

    rt_fields = ListFieldNames(rt)
    for field_to_check in [u"Shape", u"Shape_Length", u"OBJECTID"]:
        if field_to_check not in rt_fields:
            rt_fields.append(field_to_check)

    # Below unindented upon removal of above `version == "21"` conditional
    visible_l_fields = {"NGUID_RDCL": "NGUID_RDCL", "Add_L_From": "FROM_ADD", "Add_L_To": "TO_ADD", "Parity_L": "Parity", "MSAGComm_L": "MSAGComm_L", "NAME_COMPARE": "NAME_COMPARE", "CODE_COMPARE_L": "CODE_COMPARE"}
    visible_r_fields = {"NGUID_RDCL": "NGUID_RDCL", "Add_R_From": "FROM_ADD", "Add_R_To": "TO_ADD", "Parity_R": "Parity", "MSAGComm_R": "MSAGComm_R", "NAME_COMPARE": "NAME_COMPARE", "CODE_COMPARE_R": "CODE_COMPARE"}
    hidden_l_fields = {}
    hidden_r_fields = {}

    for field in rt_fields:
        if field not in visible_l_fields:
            hidden_l_fields[field] = field
        if field not in visible_r_fields:
            hidden_r_fields[field] = field

    l_strings = ["%s %s HIDDEN NONE" % (k, v) for k, v in hidden_l_fields.items()]
    for k, v in visible_l_fields.items():
        l_strings.append("%s %s VISIBLE NONE" % (k, v))
    l_field_info = ";".join(l_strings)

    r_strings = ["%s %s HIDDEN NONE" % (k, v) for k, v in hidden_r_fields.items()]
    for k, v in visible_r_fields.items():
        r_strings.append("%s %s VISIBLE NONE" % (k, v))
    r_field_info = ";".join(r_strings)

    l_field_info_check = """OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;DiscrpAgID DiscrpAgID HIDDEN NONE;RevDate RevDate HIDDEN NONE;
    EffectDate EffectDate HIDDEN NONE;ExpireDate ExpireDate HIDDEN NONE;NGUID_RDCL NGUID_RDCL VISIBLE NONE;State_L State_L HIDDEN NONE;
    State_R State_R HIDDEN NONE;County_L County_L HIDDEN NONE;County_R County_R HIDDEN NONE;City_L City_L HIDDEN NONE;
    City_R City_R HIDDEN NONE;Add_L_From FROM_ADD VISIBLE NONE;Add_L_To TO_ADD VISIBLE NONE;Add_R_From Add_R_From HIDDEN NONE;
    Add_R_To Add_R_To HIDDEN NONE;Parity_L Parity VISIBLE NONE;Parity_R Parity_R HIDDEN NONE;PostComm_L PostComm_L HIDDEN NONE;
    PostComm_R PostComm_R HIDDEN NONE;Zipcode_L Zipcode_L HIDDEN NONE;Zipcode_R Zipcode_R HIDDEN NONE;Esn_L Esn_L HIDDEN NONE;Esn_R Esn_R HIDDEN NONE;
    MSAGComm_L MSAGComm_L VISIBLE NONE;MSAGComm_R MSAGComm_R HIDDEN NONE;PreDir PreDir HIDDEN NONE;PreTypeSep PreTypeSep HIDDEN NONE;Street Street HIDDEN NONE;
    StreetType StreetType HIDDEN NONE;SufDir SufDir HIDDEN NONE;SufMod SufMod HIDDEN NONE;SpeedLimit SpeedLimit HIDDEN NONE;Oneway Oneway HIDDEN NONE;
    RoadClass RoadClass HIDDEN NONE;RevEditor RevEditor HIDDEN NONE;Label Label HIDDEN NONE;FromLevel FromLevel HIDDEN NONE;
    ToLevel ToLevel HIDDEN NONE;Surface Surface HIDDEN NONE;BoundLane BoundLane HIDDEN NONE;
    SUBMIT SUBMIT HIDDEN NONE;Comment Comment HIDDEN NONE;
    UnincCommL UnincCommL HIDDEN NONE;UnincCommR UnincCommR HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;
    GeoMSAG_L GeoMSAG_L HIDDEN NONE;GeoMSAG_R GeoMSAG_R HIDDEN NONE;
    NAME_COMPARE NAME_COMPARE VISIBLE NONE;CODE_COMPARE_L CODE_COMPARE VISIBLE NONE;CODE_COMPARE_R CODE_COMPARE_R HIDDEN NONE""" # Changed to OK Fields/Layers

        # r_field_info = """OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;DiscrpAgID DiscrpAgID HIDDEN NONE;RevDate RevDate HIDDEN NONE;
        # EFF_DATE EFF_DATE HIDDEN NONE;EXP_DATE EXP_DATE HIDDEN NONE;NGSEGID NGSEGID VISIBLE NONE;STATE_L STATE_L HIDDEN NONE;
        # STATE_R STATE_R HIDDEN NONE;COUNTY_L COUNTY_L HIDDEN NONE;COUNTY_R COUNTY_R HIDDEN NONE;MUNI_L MUNI_L HIDDEN NONE;
        # MUNI_R MUNI_R HIDDEN NONE;Add_L_From Add_L_From HIDDEN NONE;Add_L_To Add_L_To HIDDEN NONE;Add_R_From FROM_ADD VISIBLE NONE;
        # Add_R_To TO_ADD VISIBLE NONE;PARITY_L PARITY_L HIDDEN NONE;PARITY_R PARITY VISIBLE NONE;POSTCO_L POSTCO_L HIDDEN NONE;
        # POSTCO_R POSTCO_R HIDDEN NONE;ZIP_L ZIP_L HIDDEN NONE;ZIP_R ZIP_R HIDDEN NONE;ESN_L ESN_L HIDDEN NONE;ESN_R ESN_R HIDDEN NONE;
        # MSAGCO_L MSAGCO_L HIDDEN NONE;MSAGCO_R MSAGCO VISIBLE NONE;PreDir PreDir HIDDEN NONE;PreTypeSep PreTypeSep HIDDEN NONE;Street Street HIDDEN NONE;
        # StreetType StreetType HIDDEN NONE;SufDir SufDir HIDDEN NONE;SufMod SufMod HIDDEN NONE;SPDLIMIT SPDLIMIT HIDDEN NONE;ONEWAY ONEWAY HIDDEN NONE;
        # RDCLASS RDCLASS HIDDEN NONE;RevEditor RevEditor HIDDEN NONE;LABEL LABEL HIDDEN NONE;ELEV_F ELEV_F HIDDEN NONE;
        # ELEV_T ELEV_T HIDDEN NONE;SURFACE SURFACE HIDDEN NONE;STATUS STATUS HIDDEN NONE;BoundLane BoundLane HIDDEN NONE;
        # LRSKEY LRSKEY HIDDEN NONE;TopoExcept TopoExcept HIDDEN NONE;SUBMIT SUBMIT HIDDEN NONE;Comment Comment HIDDEN NONE;
        # UNINC_L UNINC_L HIDDEN NONE;UNINC_R UNINC_R HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;
        # AUTH_L AUTH_L HIDDEN NONE;AUTH_R AUTH VISIBLE NONE;GEOMSAGL GEOMSAGL HIDDEN NONE;GEOMSAGR GEOMSAGR HIDDEN NONE;
        # NAME_COMPARE NAME_COMPARE VISIBLE NONE;CODE_COMPARE_L CODE_COMPARE_L HIDDEN NONE;CODE_COMPARE_R CODE_COMPARE VISIBLE NONE"""

    # Below unindented upon removal of above `version == "21"` conditional
    r_field_info_check = """OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;DiscrpAgID DiscrpAgID HIDDEN NONE;RevDate RevDate HIDDEN NONE;
    EffectDate EffectDate HIDDEN NONE;ExpireDate ExpireDate HIDDEN NONE;NGUID_RDCL NGUID_RDCL VISIBLE NONE;State_L State_L HIDDEN NONE;
    State_R State_R HIDDEN NONE;County_L County_L HIDDEN NONE;County_R County_R HIDDEN NONE;City_L City_L HIDDEN NONE;
    City_R City_R HIDDEN NONE;Add_L_From Add_L_From HIDDEN NONE;Add_L_To Add_L_To HIDDEN NONE;Add_R_From FROM_ADD VISIBLE NONE;
    Add_R_To TO_ADD VISIBLE NONE;Parity_L Parity_L HIDDEN NONE;Parity_R Parity VISIBLE NONE;PostComm_L PostComm_L HIDDEN NONE;
    PostComm_R PostComm_R HIDDEN NONE;Zipcode_L Zipcode_L HIDDEN NONE;Zipcode_R Zipcode_R HIDDEN NONE;Esn_L Esn_L HIDDEN NONE;Esn_R Esn_R HIDDEN NONE;
    MSAGComm_L MSAGComm_L HIDDEN NONE;MSAGComm_R MSAGComm_R VISIBLE NONE;PreDir PreDir HIDDEN NONE;PreTypeSep PreTypeSep HIDDEN NONE;Street Street HIDDEN NONE;
    StreetType StreetType HIDDEN NONE;SufDir SufDir HIDDEN NONE;SufMod SufMod HIDDEN NONE;SpeedLimit SpeedLimit HIDDEN NONE;Oneway Oneway HIDDEN NONE;
    RoadClass RoadClass HIDDEN NONE;RevEditor RevEditor HIDDEN NONE;Label Label HIDDEN NONE;FromLevel FromLevel HIDDEN NONE;
    ToLevel ToLevel HIDDEN NONE;Surface Surface HIDDEN NONE;BoundLane BoundLane HIDDEN NONE;
    SUBMIT SUBMIT HIDDEN NONE;Comment Comment HIDDEN NONE;
    UnincCommL UnincCommL HIDDEN NONE;UnincCommR UnincCommR HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;
    GeoMSAG_L GeoMSAG_L HIDDEN NONE;GeoMSAG_R GeoMSAG_R HIDDEN NONE;
    NAME_COMPARE NAME_COMPARE VISIBLE NONE;CODE_COMPARE_L CODE_COMPARE_L HIDDEN NONE;CODE_COMPARE_R CODE_COMPARE VISIBLE NONE""" # Changed to OK Fields/Layers

    ########## BEGIN FIELD INFO STRING GENERATION TEST CODE ##########

    l_field_set = set(l_field_info.split(";"))
    l_check_set = set(l_field_info_check.replace("\n", "").replace("    ", " ").split(";"))
    r_field_set = set(r_field_info.split(";"))
    r_check_set = set(r_field_info_check.replace("\n", "").replace("    ", " ").split(";"))

    l_field_set = set([x.strip() for x in l_field_set])
    l_check_set = set([x.strip() for x in l_check_set])
    r_field_set = set([x.strip() for x in r_field_set])
    r_check_set = set([x.strip() for x in r_check_set])

    if not l_field_set == l_check_set:
        # debugMessage("LEFT FIELD INFOS DON'T MATCH!")
        in_auto_string_only = l_field_set - l_check_set
        in_check_string_only = l_check_set - l_field_set
        # if len(in_auto_string_only) > 0:
        #     debugMessage("LEFT: These fields don't exist in CHECK list: %s" % list(in_auto_string_only))
        if len(in_check_string_only) > 0:
            debugMessage("LEFT: These fields don't exist in AUTO list: %s" % list(in_check_string_only))
    if not r_field_set == r_check_set:
        # debugMessage("RIGHT FIELD INFOS DON'T MATCH!")
        in_auto_string_only = r_field_set - r_check_set
        in_check_string_only = r_check_set - r_field_set
        # if len(in_auto_string_only) > 0:
        #     debugMessage("RIGHT: These fields don't exist in CHECK list: %s" % list(in_auto_string_only))
        if len(in_check_string_only) > 0:
            debugMessage("RIGHT: These fields don't exist in AUTO list: %s" % list(in_check_string_only))

    ########## END ##########

    # set up list of lists to look at each side of the road
    side_lists = [[rd_object.PARITY_L, rd_object.Add_L_From, rd_object.Add_L_To, rd_object.UNIQUEID, code_field + "_L", "RoadCenterline_Layer", l_field_info],
                  [rd_object.PARITY_R, rd_object.Add_R_From, rd_object.Add_R_To, rd_object.UNIQUEID, code_field + "_R", "RoadCenterline_Layer2", r_field_info]]


    # create a temp table of road segments
    # do not include 0-0 ranges or records not for submission
    for side in side_lists:
        # get the side
        side_x = side[4][-1]

        # set up field equivalences
        wanted_fields_dict = {"Parity": side[0], "FROM_ADD": side[1], "TO_ADD": side[2], "CODE_COMPARE": side[4]}
        # wanted_fields_dict = {"PARITY": side[0], "FROM_ADD": side[1], "TO_ADD": side[2],
        #                 "CODE_COMPARE": side[4]}  # Rewritten as above upon removal of below version conditional

        # if version == "21":
        # wanted_fields_dict["PROV"] = "PROV_" + side_x  # Removed with version conditional; incorporated into above

        # set up where clause
        wc = "(" + side[1] + " <> 0 or " + side[2] + " <> 0)"
        lyr = "lyr"
        # include- high, low, code field, parity, and NGSEGID_L or _R
        MakeTableView_management(rt, lyr, wc, "", side[6])

        holder = join(storage, side[5])
        if Exists(holder):
            Delete_management(holder)
        CopyRows_management(lyr, holder)
        Delete_management(lyr)

        # made sure the table has a column for what side of the street it is
        if not fieldExists(holder, ap_object.RCLSide):
            AddField_management(holder, ap_object.RCLSide, "TEXT", "", "", 1)
        CalculateField_management(holder, ap_object.RCLSide, '"' + side_x + '"', "PYTHON_9.3", "")
        # CalculateField_management(output_table, "RCLSide", '"' + side_x + '"', "PYTHON_9.3", "")

        # make sure that the side-neutral field names get added for comparison
        # wanted_fields_dict keys are "Parity", "FROM_ADD", "TO_ADD", "CODE_COMPARE"
        for w_f in wanted_fields_dict.keys():
            if not fieldExists(holder, w_f):
                if "Parity" in w_f:
                    if not fieldExists(holder, w_f):
                        AddField_management(holder, w_f, "TEXT", "", "", 1)
                    CalculateField_management(holder, w_f, "!" + wanted_fields_dict[w_f] + "!", "PYTHON", "")

                else:
                    if not fieldExists(holder, w_f):
                        AddField_management(holder, w_f, "LONG")
                    CalculateField_management(holder, w_f, "!" + wanted_fields_dict[w_f] + "!", "PYTHON", "")


    #create a temporary table of side-specific ranges
    if "TN_List" in output_table:
        tempTable = join(dirname(output_table), "RoadList_" + time.strftime('%Y%m%d'))
    else:
        tempTable = join(storage, "RoadsTemp")
    if Exists(tempTable):
        Delete_management(tempTable)

    rc_1 = join(storage, "RoadCenterline_Layer")
    rc_2 = join(storage, "RoadCenterline_Layer2")
    Merge_management([rc_1, rc_2], tempTable)

    Delete_management(rc_1)
    Delete_management(rc_2)
    Delete_management(rt)

    # make sure certain fields exist in the address point layer
    makeSureFieldDict = {"MATCH": 1, rd_object.UNIQUEID: 254, "MATCH_LAYER": 20, ap_object.RCLSide: 1}

    for fld in makeSureFieldDict.keys():
        length = makeSureFieldDict[fld]
        if not fieldExists(output_table, fld):
            AddField_management(output_table, fld, "TEXT", "", "", length)

    idField = "NGUID_ADD" # Changed to OK Fields
	
    if "TN_List" in output_table:
        idField = "NGTNID"

    addy_fields = [HNO, code_field, "MATCH", rd_object.UNIQUEID, "MATCH_LAYER", ap_object.RCLSide, idField]

    non_match_count = 0
    count = 1

    # set up reporting so the user knows how things are coming along
    total = getFastCount(output_table)
    half = round(total/2,0)
    quarter = round(half/2,0)
    three_quarters = half + quarter
    timeDict = {quarter: "1/4", half:"1/2", three_quarters:"3/4"}

    # create a text file that will report back geocoding ties
    txt = gdb.replace(".gdb", "_TIES.txt")
    if exists(txt):
        remove(txt)

    # loop through address points to compare each one
    no1_wc = "CODE_COMPARE <> 1"
    record = [val for val in SearchCursor(output_table, addy_fields, no1_wc)]
    record_len = len(record)
    SetProgressor("step", "Looping through Address Points to Compare Each One...", 0, record_len, 50)
    # row_i = 1
    checkpoint = 50
    with UpdateCursor(output_table, addy_fields, no1_wc) as rows:
        for row in rows:
            if count >= checkpoint:
                SetProgressorPosition()
                checkpoint += 50
##            r_start_time = time.time()
            # set defaults
            segid = ""
            side = ""
            addid = row[6]

            # start testing out addresses
            hno, hno_code = row[0], row[1]
            if hno not in (None, "", " "):
                try:
                    hno = int(hno)
                    match_combo = db_compare(hno, hno_code, tempTable, addid, txt, idField)
                    segid = match_combo[0]
                    side = match_combo[1]
                except:
                    hno = ""

            match = "M"
            layer = "ROAD_CENTERLINE" # Changed to OK Fields/layer

            if segid == "TIES":
                match = "T"
                side = "N"
                non_match_count += 1

            elif segid == "":
                if queryAP == True and hno not in (None, "", " "):
                    segid = ap_compare(hno, hno_code, ap_fc)
                    match = "M"
                    side = "N"
                    layer = "ADDRESS_POINT" # Changed to OK Fields/layer
                    if segid =="TIES":
                        match = "T"
                        side = "N"
                        non_match_count += 1
                    elif segid == "":
                        match = "U"
                        side = "N"
                        non_match_count += 1
                else:
                    match = "U"
                    side = "N"
                    non_match_count += 1

            if match == "U":
                layer = ""

            row[2] = match
            row[3] = segid
            row[4] = layer
            # userMessage("Passing Side: %s" % side)
            # if version == "21":
            row[5] = side

            rows.updateRow(row)
##            r_end_time = time.time()
##            print("Record time: %g seconds" % (r_end_time - r_start_time))
##            AddMessage("Record time: %g seconds" % (r_end_time - r_start_time))
            if count in timeDict:
                fraction = timeDict[count]
                AddMessage("Processing is " + fraction + " complete.")
##                partial_time = time.time()
##                AddMessage("Elapsed time s %g seconds" % (partial_time - start_time))
##
            count += 1
            # row_i += 1

    ResetProgressor()

    if non_match_count == 0:
        # print("All address points match. Good job.")
        userMessage("All address points match. Good job.")
    else:
        # print("Some address points did not match. Results are available in " + output_table + ", ties are listed in " + txt + ". Please examine the MATCH field to find U (unmatched) records or T (ties).")
        userMessage("Some address points did not match. Results are available in " + output_table + ", ties are listed in " + txt + ". Please examine the MATCH field to find U (unmatched) records or T (ties).")

##    end_time = time.time()
##    print("Elapsed time was %g seconds" % (end_time - start_time))

    # clean up
    if "TN_List" not in output_table:
        try:
            Delete_management(tempTable)
        except:
            pass

    for field in ["NAME_COMPARE", "CODE_COMPARE", "CODE_COMPARE_L", "CODE_COMPARE_R"]:
        for data in [ap_fc]:
            if fieldExists(data, field):
                try:
                    DeleteField_management(data, field)
                except:
                    pass
