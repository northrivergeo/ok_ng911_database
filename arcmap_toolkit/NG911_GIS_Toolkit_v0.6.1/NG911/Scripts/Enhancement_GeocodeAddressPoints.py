#-------------------------------------------------------------------------------
# Name:        Enhancement_GeocodeAddressPoints
# Purpose:     Geocodes address points against road centerline
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     26/07/2016, Edited 10/28/2016, Edited 12/13/2016, edited 5/12/2017
# Modified:    January 6, 2022
# Copyright:   (c) kristen 2016
#-------------------------------------------------------------------------------
from arcpy import (GetParameterAsText, Exists, CopyFeatures_management, DisableEditorTracking_management,
            EnableEditorTracking_management, AddJoin_management, RemoveJoin_management, CalculateField_management,
            Delete_management, MakeFeatureLayer_management, AddIndex_management, ListFields, ListIndexes)
from MSAG_DBComparison import launch_compare
from NG911_GDB_Objects import getFCObject
from NG911_arcpy_shortcuts import fieldExists
from os.path import join


def getIndexNames(lyr):
    names = map(lambda x: x.name, ListIndexes(lyr))
    return names


def geocompare(gdb, version, emptyOnly):
    addy_fc = join(gdb, "NG911", "ADDRESS_POINT") # Changed to OK Fields
    rd_fc = join(gdb, "NG911", "ROAD_CENTERLINE") # Changed to OK Fields
    addy_object = getFCObject(addy_fc)
    addy_field_list = addy_object.FULLNAME_FIELDS
    addy_field_list[0] = "NAME_COMPARE"  # Replace FullName field with NAME_COMPARE

    a_id = addy_object.UNIQUEID

    # create output results
    out_name = "AddressPt_GC_Results"
    output_table = join(gdb, out_name)
    fl = "fl"

    # set up where clause if the user only wants empty records done
    if emptyOnly == "true":
        # wc = "SUBMIT = 'Y' AND (" + addy_object.RCLMatch + " is null or " + addy_object.RCLMatch + " in ('', ' ','TIES','NO_MATCH','NULL_ID'))"  # WHERE clause for Address Point
        wc = "SUBMIT = 'Y' AND (%s IS NULL OR %s IN ('', ' ', 'TIES', 'NO_MATCH', 'NULL_ID'))" % (addy_object.RCLMatch, addy_object.RCLMatch)
    else:
        wc = "SUBMIT = 'Y'"  # WHERE clause for Address Point

    # make sure we're dealing with a clean output table
    if Exists(output_table):
        Delete_management(output_table)

    # create output table
    MakeFeatureLayer_management(addy_fc, fl, wc)
    CopyFeatures_management(fl, output_table)
    Delete_management(fl)

    # turn off editor tracking
    # DisableEditorTracking_management(addy_fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")
    # DisableEditorTracking_management(rd_fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")

    launch_compare(
        gdb=gdb,
        output_table=output_table,
        HNO=addy_object.Address,
        addy_city_field=addy_object.MSAGCO,
        addy_field_list=addy_field_list,
        queryAP=False,
        legacy_check="false"
    )

    # if the version is 2.1...
    # ...which it will be...
    # if version == "21":
    ##### BEGIN un-indent for removing `if version == "21"` #####
    indexName = "AddrIdx"

    MakeFeatureLayer_management(addy_fc, fl)

    # check to see if MY index exists on NGADDID
    addy_fc_index = getIndexNames(fl)

    if indexName not in addy_fc_index:
        # add an index on NGADDID
        AddIndex_management(fl, a_id, indexName)

    # create a feature layer from the results
    ot_fl = "ot_fl"
    MakeFeatureLayer_management(output_table, ot_fl)

    # double check to see if the kristen index exists on the outpu
    output_index = getIndexNames(ot_fl)

    if indexName not in output_index:
        AddIndex_management(ot_fl, a_id, indexName)

    # join the output table to the address point file
    AddJoin_management(fl, a_id, ot_fl, a_id, "KEEP_COMMON")

    # make a list of the field names in upper case
    uc_fieldNames = []
    flds = ListFields(fl)
    for fld in flds:
        uc_fieldNames.append(fld.name.upper())

    # define fields to be calculated
    rclmatch = "ADDRESS_POINT.RCLMatch" # Changed to OK Fields/Layer
    rclside = "ADDRESS_POINT.RCLSide" # Changed to OK Fields/Layer
    ngsegid_exp = "!AddressPt_GC_Results.NGUID_RDCL!"
    rclside_exp = "!AddressPt_GC_Results.RCLSide!"

    # # fix for Butler County if those fields don't exist
    # if rclmatch.upper() not in uc_fieldNames:
    #     rclmatch = "KSNG911S.DBO.%s" % rclmatch
    #     ngsegid_exp = "!KSNG911S.DBO.AddressPt_GC_Results.NGUID_RDCL!"
    # if rclside.upper() not in uc_fieldNames:
    #     rclside = "KSNG911S.DBO.%s" % rclside
    #     rclside_exp = "!KSNG911S.DBO.AddressPt_GC_Results.RCLSide!"

    # calculate field
    CalculateField_management(fl, rclmatch, ngsegid_exp, "PYTHON_9.3", "")
    CalculateField_management(fl, rclside, rclside_exp, "PYTHON_9.3", "")

    # remove the join
    RemoveJoin_management(fl)

    Delete_management(fl)
    Delete_management(ot_fl)
    ##### END un-indent for removing `if version == "21"` #####

    # turn editor tracking back on
    # EnableEditorTracking_management(addy_fc, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields
    # EnableEditorTracking_management(rd_fc, "", "", "RevEditor", "RevDate", "NO_ADD_FIELDS", "UTC") # Changed to OK Fields


def main():
    gdb = GetParameterAsText(0)
    emptyOnly = GetParameterAsText(1)
    version = "20"

    # see what version we're working with
    # Version must be "21"
    ap = join(gdb, "NG911", "ADDRESS_POINT")
    # if fieldExists(ap, "RCLMatch"):
    version = "21"

    # if version == "20" and emptyOnly == "true":
    #     emptyOnly = "false"
    geocompare(gdb, version, emptyOnly)

if __name__ == '__main__':
    main()
