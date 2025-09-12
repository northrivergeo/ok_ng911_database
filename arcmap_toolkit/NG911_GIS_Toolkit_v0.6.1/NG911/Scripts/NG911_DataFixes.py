#-------------------------------------------------------------------------------
# Name:        NG911_DataFixes
# Purpose:     Scripts to adjust a variety of common NG911 data issues
#
# Author:      kristen (KS), Emma Baker (OK), Riley Baird (OK)
#
# Created:     21/10/2015
# Modfied:     December 4, 2020
#-------------------------------------------------------------------------------
from arcpy import (GetParameterAsText, MakeTableView_management, Frequency_analysis, CalculateField_management,
                   Delete_management,
                   env, Exists, CreateTable_management,
                   AddField_management, GetCount_management, ListFields, ListFeatureClasses)
from arcpy.da import SearchCursor, InsertCursor, UpdateCursor
from os.path import join, dirname, basename

try:
    from typing import List, Dict
except:
    pass

from NG911_DataCheck import getFieldDomain
from NG911_User_Messages import *
from time import strftime
from NG911_GDB_Objects import getGDBObject, getFCObject, NG911_Session, NG911_Session_obj
from NG911_arcpy_shortcuts import fieldExists, CalcWithWC, DomainInfo, FieldInfo, ListFieldNames


def FixDomainCase_KS(gdb, domainFolder):
    userWarning("FixDomainCase_KS is a legacy function. Calls to FixDomainCase_KS should be changed to FixDomainCase.")
    env.workspace = gdb
    gdbObject = getGDBObject(gdb)

    table = gdbObject.FieldValuesCheckResults
    fvcr_object = getFCObject(table)

    if Exists(table):

        #read FieldValuesCheckResults, limit table view to only domain errors
        tbl = "tbl"
        wc = fvcr_object.DESCRIPTION + " LIKE '%not in approved domain for field%'"
        MakeTableView_management(table, tbl, wc)

        outTableInMemory = r"in_memory\outputFrequency"

        #run frequency, store in memory
        Frequency_analysis(tbl, outTableInMemory, [fvcr_object.DESCRIPTION, fvcr_object.LAYER, fvcr_object.FIELD])

        #run search cursor on frequency, see which fields in which layers have domain issues
        freq_fields = (fvcr_object.DESCRIPTION, fvcr_object.LAYER, fvcr_object.FIELD)
        freq_wc = fvcr_object.FIELD + " is not null and " + fvcr_object.FIELD + " not in ('',' ')"

        fixDict = {}

        with SearchCursor(outTableInMemory, freq_fields, freq_wc) as rows:
            for row in rows:
                #get the offending value out of the error message
                value = ((row[0].strip("Error: Value ")).replace(" not in approved domain for field ", "|")).split("|")[0]
                layerName = row[1]
                fieldName = row[2]

                #make sure the field name is not blank
                if fieldName not in ('',' '):
                    #test if the value in upper case is in the domain
                    if fieldName[-2:] in ["_L", "_R"]:
                        fieldNameForDict = fieldName.strip("_L").strip("_R")
                    else:
                        fieldNameForDict = fieldName
                    domainDict = getFieldDomain(fieldNameForDict, domainFolder)
                    domainList = []

                    for val in domainDict:
                        domainList.append(val)

                    if value.upper() in domainList:
                        #if yes, load into a master dictionary of stuff to fix (key is layer name, value is a list of fields that need help)
                        if layerName in fixDict:
                            fieldsToFix = fixDict[layerName]

                            #see if field name is already in list of those to fix
                            if fieldName not in fieldsToFix:
                                fieldsToFix.append(fieldName)
                                fixDict[layerName] = fieldsToFix

                        else:
                            fixDict[layerName] = [fieldName]


        Delete_management("in_memory")

        #loop through resulting list
        if fixDict != {}:
            report = ""
            # userMessage(unicode(fixDict))
            for layer in fixDict:
                fields = fixDict[layer]
                report = report + layer + ": "
                #for each value in the key, calculate the attribute field to be all upper case
                for field in fields:
                    report = report + field + " "
                    CalculateField_management(layer, field, "!"+ field + "!.upper()", "PYTHON_9.3")

            debugMessage("Domain values edited to be upper case: " + report)

    else:
        userWarning(basename(table) + " must be present for this tool to run.")

def FixDomainCase(gdb, session):
    # type: (str, NG911_Session_obj) -> None
    '''
    In all of the required layers in a given geodatabase, each field with a domain is checked for values that are the
    same as in the domain specification but have incorrect casing and corrected if necessary.

    Parameters
    ----------
    gdb : str
        Full path to the geodatabase whose layers should be checked
    session : NG911_Session_obj
        A session object initialized to the geodatabase
    '''
    gdb_object = session.gdbObject
    domains_folder = session.domainsFolderPath
    fields_folder = session.fieldsFolderPath
    required_layers = gdb_object.requiredLayers  # type: List[str]  # Full paths to required layers
    # required_layers = [r"G:\ArcGIS\Project Files\NG911\NG911 GIS TOOL\1 - TEST DATA\BeaverCounty\Beaver_2019_0927_OK_Standards_old.gdb\NG911\ADDRESS_POINT"]
    # userMessage("FIX DOMAIN CASE ONLY RUNNING ON ADDRESS_POINT FOR TESTING PURPOSES")

    domains = {}  # type: Dict[str, DomainInfo]

    for layer in required_layers:
        layer_basename = basename(layer)
        if not Exists(layer):
            userWarning("Required layer %s not found!" % layer_basename)
            continue
        userMessage("Checking layer %s." % layer_basename)
        fields_filename = "%s.txt" % layer_basename
        fields_info = FieldInfo.get_from_text(join(fields_folder,fields_filename))  # type: List[FieldInfo]
        cursor_fields = [field_info.name for field_info in fields_info]
        # userMessage("Getting fields: %s" % ", ".join(cursor_fields))
        # fields_in_input = ListFieldNames(layer)
        # fields_exist_check = [field in ]
        for field_info in fields_info:
            if field_info.domain is not "":  # If this field has a domain...
                # userMessage("Field is %s" % field_info.name, True)
                if field_info.domain not in domains.keys():  # If domain file not already loaded into domains dict...
                    domain_filename = join(domains_folder, field_info.domain + "_Domains.txt")
                    domains[field_info.domain] = DomainInfo.get_from_domainfile(domain_filename)
                domain_codes = domains[field_info.domain].domain_dict.keys()  # Get all the codes of this domain as a list
                domain_codes_upper = [domain_code.upper() for domain_code in domain_codes]  # All the codes, but in all caps
                if not fieldExists(layer, field_info.name):
                    userWarning("Field %s does not exist!" % field_info.name)
                    continue
                cursor = UpdateCursor(layer, field_info.name)
                for row in cursor:
                    if row[0] is not None:
                        row_value = row[0]  # Get the value of this field of row
                        row_value_upper = row_value.upper()  # Above, but in all caps
                        if row_value_upper in domain_codes_upper and row_value not in domain_codes:
                            code_index = domain_codes_upper.index(row_value_upper)
                            row[0] = domain_codes[code_index]
                            cursor.updateRow(row)


def FixMSAGCOspaces(gdb, check):

    gdbObject = getGDBObject(gdb)
    if check[0] == "true":
        addressPoints = gdbObject.AddressPoints
        ap_object = getFCObject(addressPoints)
        fields = [ap_object.MSAGCO]
        with UpdateCursor(addressPoints, fields) as cursor:
            for row in cursor:
                if row[0] is None:
                    continue
                row[0] = unicode(row[0]).strip()
                cursor.updateRow(row)
        # CalculateField_management(addressPoints, "MSAGComm", "!MSAGComm!.strip()", "PYTHON_9.3", "") # Changed to OK Fields

    if check[1] == "true":
        roadCenterlines = gdbObject.RoadCenterline
        rcl_object = getFCObject(roadCenterlines)
        fields = [rcl_object.MSAGCO_L, rcl_object.MSAGCO_R]
        with UpdateCursor(roadCenterlines, fields) as cursor:
            for row in cursor:
                if row[0] is not None:
                    row[0] = unicode(row[0]).strip()
                if row[1] is not None:
                    row[1] = unicode(row[1]).strip()
                cursor.updateRow(row)
        # for val in ["MSAGComm_L", "MSAGComm_R"]:
        #     CalculateField_management(roadCenterlines, val, "!" + val + "!.strip()", "PYTHON_9.3", "") # Changed to OK Fields

    debugMessage("Leading and trailing spaces removed from MSAGComm field(s), if there were any.")


def fixSubmit(gdb, fcs):
    fds = join(gdb, "NG911")

    # list all fcs
    env.workspace = fds
    # fcs = ListFeatureClasses()

    # set up where clause
    wc = "SUBMIT IS NULL"
    debugMessage(fcs)

    # loop through feature classes and edit the field
    for fc in fcs:
        # full_path = join(fds, fc)
        full_path = fc
        fc_name = basename(fc)
    # CalcWithWC(full_path, "SUBMIT", '"Y"', wc)
        fc_obj = getFCObject(full_path)
        unique_id_field = fc_obj.UNIQUEID
        submit_field = fc_obj.SUBMIT
        debugMessage("Unique ID field: %s" % unique_id_field)
        debugMessage("Submit field: %s" % submit_field)
        with UpdateCursor(full_path, [unique_id_field, submit_field]) as cursor:
            debugMessage("Opened cursor for %s." % fc_name)
            for row in cursor:
                if row[1] in (None, "", " "):
                    row[1] = "Y"
                if row[1] not in ("Y", "N"):
                    userWarning('SUBMIT field for feature with unique ID %s is %s. It must by "Y" or "N".' % (row[0], row[1]))
                cursor.updateRow(row)

    # make sure the road alias record gets updated too
	# fl_calc = "fl_calc"
	# if Exists(join(gdb, "Road_Alias")): # Changed to OK Fields/Layer
	# 	ra = join(gdb, "Road_Alias") # Changed to OK Fields/Layer
	# 	MakeTableView_management(ra, fl_calc, wc)
	# 	CalculateField_management(fl_calc, "SUBMIT", '"Y"', "PYTHON_9.3", "")
	# 	Delete_management(fl_calc)