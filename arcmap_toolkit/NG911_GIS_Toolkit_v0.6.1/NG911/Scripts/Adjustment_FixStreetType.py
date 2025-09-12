# -*- #################
# ---------------------------------------------------------------------------
# Script for changing the Street Type from the Legacy System to the NG911 System.
# Author:  Emma Baker, Riley Baird, Oklahoma DOT GIS
# Created: April 1, 2020
# Modified: May 4, 2021
# ---------------------------------------------------------------------------

# Import arcpy module
from arcpy import GetParameterAsText
from arcpy.da import UpdateCursor, Editor
from NG911_User_Messages import *
from os.path import dirname, join
from NG911_GDB_Objects import NG911_Session, getFCObject

def fix_street_type():
    # Set the parameters and variables
    FC = GetParameterAsText(0)
    streetname_field_name = GetParameterAsText(1)
    pretype_field_name = GetParameterAsText(2)
    predir_field_name = GetParameterAsText(3)
    sufdir_field_name = GetParameterAsText(4)
    lgcy_predir_conv = GetParameterAsText(5)
    lgcy_street_conv = GetParameterAsText(6)
    lgcy_type_conv = GetParameterAsText(7)
    lgcy_sufdir_conv = GetParameterAsText(8)
    calc_lgcyadd = GetParameterAsText(9)

    gdb = dirname(dirname(FC))

    session = NG911_Session(gdb)
    fc_obj = getFCObject(FC)
    fields_dir = session.domainsFolderPath
    domainFile = join(fields_dir, "LGCYSTREETTYPE_Domains.txt")
    direction_domain = join(fields_dir, "LGCYDIRECTION_Domains.txt")

    # Layer Identifier
    word = FC.upper()
    debugMessage(word)
    FCName = FC.split("\\")

    edit = Editor(gdb)
    edit.startEditing(False, False)

    # The first expression is formatted for use with file geodatabases
    # The second is formatted for use with SDE and personal geodatabases
    if ".gdb" in FC:
        Expression = "{0} is NULL or CHAR_LENGTH({0}) = 0".format(streetname_field_name)
    else:
        Expression = "{0} is NULL or LEN([{0}]) = 0".format(streetname_field_name)

    # PreDir to LcgyPreDir
    if lgcy_predir_conv == "true":
        userMessage("Moving to %s from %s." % (fc_obj.LgcyPreDir, fc_obj.PreDir))
        fields = [fc_obj.LgcyPreDir, fc_obj.PreDir]
        with UpdateCursor(FC, fields) as cursor:
            for row in cursor:
                if row[1] in ["", " ", None]:
                    val = None
                else:
                    val = row[1].upper().strip()
                if val in ["N", "S", "E", "W", "NE", "NW", "SE", "SW"]:
                    row[0] = val
                elif val is None:
                    row[0] = None
                else:
                    row[0] = row[1]
                cursor.updateRow(row)

    # Street to LgcyStreet
    if lgcy_street_conv == "true":
        userMessage("Moving to %s from %s." % (fc_obj.LgcyStreet, fc_obj.Street))
        fields = [fc_obj.LgcyStreet, fc_obj.Street]
        with UpdateCursor(FC, fields) as cursor:
            for row in cursor:
                if row[1] in ["", " ", None]:
                    row[0] = None
                else:
                    row[0] = row[1]
                cursor.updateRow(row)

    # StreetType to LgcyType
    if lgcy_type_conv == "true":
        userMessage("Moving to %s from %s." % (fc_obj.LgcyType, fc_obj.StreetType))
        fields = [fc_obj.LgcyType, fc_obj.StreetType]
        with UpdateCursor(FC, fields) as cursor:
            for row in cursor:
                if row[1] in ["", " ", None]:
                    val = None
                else:
                    val = row[1].upper().strip()
                row[0] = val
                cursor.updateRow(row)

    # SufDir to LgcySufDir
    if lgcy_sufdir_conv == "true":
        userMessage("Moving to %s from %s." % (fc_obj.LgcySufDir, fc_obj.SufDir))
        fields = [fc_obj.LgcySufDir, fc_obj.SufDir]
        with UpdateCursor(FC, fields) as cursor:
            for row in cursor:
                if row[1] in ["", " ", None]:
                    val = None
                else:
                    val = row[1].upper().strip()
                if val in ["N", "S", "E", "W", "NE", "NW", "SE", "SW"]:
                    row[0] = val
                elif val is None:
                    row[0] = None
                else:
                    row[0] = row[1]
                cursor.updateRow(row)

    if calc_lgcyadd == "true":
        fields = fc_obj.LGCYADDR_FIELDS
        with UpdateCursor(FC, fields) as cursor:
            for row in cursor:
                expression = [unicode(x).upper().strip() for x in row[1:] if x not in ("", " ", None)]
                expression = " ".join(expression)
                if expression in ["", " ", None, []]:
                    row[0] = None
                else:
                    row[0] = expression
                cursor.updateRow(row)


    if streetname_field_name not in [None, "", " "] or pretype_field_name not in [None, "", " "]:
        # Setup for Domain.txt file to create dictionary
        domainFileSplit = domainFile.split("\\")
        openDomainFile = open(domainFile)
        openDomain = openDomainFile.readlines()
        firstline = openDomain.pop(0)
        # domainName = domainFileSplit[-1]
        # domainName = domainName[:-4]

        # Creates a dictionary for the Legacy Street Type Domain conversion data.
        dict_domain = {}
        for line in openDomain:
            lineSplit = line.split("|")

            key = lineSplit[0]
            value = lineSplit[1].strip("\n")

            dict_domain.update({key: value})

        openDomainFile.close()

        type_fields = []
        if streetname_field_name not in [None, "", " "]:
            type_fields.append(streetname_field_name)
        if pretype_field_name not in [None, "", " "]:
            type_fields.append(pretype_field_name)

        # Using the Legacy Street Type Domain Dictionary to update the Street Type field using UpdateCursor (arcpy.da)
        with UpdateCursor(FC, type_fields) as cursor:
            userMessage("Checking %s and %s in %s." % (pretype_field_name, streetname_field_name, FCName[-1]))
            change_count = 0

            # Cycle through field and dictionary to compare field to key (Legacy) and update with the value (NG911)
            for row in cursor:
                for i, value in enumerate(row):
                    if value is None:
                        row[i] = None
                    # Abbreviation in domain return long domain value (RD => ROAD)
                    elif value.upper() in dict_domain.keys():
                        row[i] = dict_domain[value.upper()]
                        change_count += 1
                    # Not included in Legacy Street Type domain file
                    elif value.upper() == "PKY":
                        row[i] = "PARKWAY"
                        change_count += 1
                    elif value.upper() == "TERR":
                        row[i] = "TERRACE"
                        change_count += 1
                    elif value.upper() == "AV":
                        row[i] = "AVENUE"
                        change_count += 1
                    elif value.upper() == "BL":
                        row[i] = "BOULEVARD"
                        change_count += 1
                    # If original value is an empty string or single space
                    elif value == ' ':
                        # userMessage("Updating blank strings to Nulls.")
                        row[i] = None
                        change_count += 1
                    elif value == '':
                        # userMessage("Updating blank strings to Nulls.")
                        row[i] = None
                        change_count += 1
                    # Else return upper original value
                    else:
                        row[i] = value.upper()

                    cursor.updateRow(row)

        userMessage("%s and/or %s was changed in %i record(s)." % (streetname_field_name, pretype_field_name, change_count))

    ##### PREDIR AND SUFDIR #####
    if predir_field_name not in [None, "", " "] or sufdir_field_name not in [None, "", " "]:
        # Setup for Domain.txt file to create dictionary
        domainFileSplit = domainFile.split("\\")
        openDomainFile = open(direction_domain)
        openDomain = openDomainFile.readlines()
        firstline = openDomain.pop(0)

        # Creates a dictionary for the Legacy Direction Domain conversion data.
        dict_domain = {}
        for line in openDomain:
            lineSplit = line.split("|")
            key = lineSplit[0]
            value = lineSplit[1].strip("\n")
            dict_domain.update({key: value})

        openDomainFile.close()

        dir_fields = []
        if predir_field_name not in [None, "", " "]:
            dir_fields.append(predir_field_name)
        if sufdir_field_name not in [None, "", " "]:
            dir_fields.append(sufdir_field_name)

        with UpdateCursor(FC, dir_fields) as cursor:
            userMessage("Checking %s and %s in %s." % (predir_field_name, sufdir_field_name, FCName[-1]))
            change_count = 0
            for row in cursor:
                for i, value in enumerate(row):
                    if value is None:
                        row[i] = None
                    elif value in ["", " "]:
                        row[i] = None
                        change_count += 1
                    elif value.upper() in dict_domain.keys():
                        row[i] = dict_domain[value.upper()]
                        change_count += 1
                    else:
                        row[i] = value.upper()
                cursor.updateRow(row)

        userMessage("%s and/or %s were changed in %i record(s)." % (predir_field_name, sufdir_field_name, change_count))

    edit.stopEditing(True)

if __name__ == "__main__":
    fix_street_type()