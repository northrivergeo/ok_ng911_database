#-------------------------------------------------------------------------------
# Name:        Adjustment_FixTopoExcept.py
# Purpose:     Corrects the values in the TopoExcept field to the correct values; Updates the domain to the correct values.
#
# Author:      Baker, Baird (OK)
#
# Created:     March 2, 2021
# Modified:    March 2, 2021
# Copyright:   (c) Emma Marie Baker 2021, Riley Baird, 2021
#-------------------------------------------------------------------------------
## Imports
from arcpy import GetParameterAsText
from Okprep_createFC import create_feature_class
from os.path import join, dirname, basename
import os
from NG911_GDB_Objects import NG911_Session
from NG911_arcpy_shortcuts import DomainInfo
import arcpy
from arcpy.da import Editor, UpdateCursor
from NG911_User_Messages import *
from NG911_DataCheck import checkGDBDomains
import collections


def main():

    ## Get Parameters from ArcGIS Inputs and assign ArcGIS inputs to a list
    input_gdb = GetParameterAsText(0)
    iter = range(1,22)
    fix_domain_list = []
    for val in iter:
        fix_domain_list.append(GetParameterAsText(val))

    session = NG911_Session(input_gdb)
    domain_folder = session.domainsFolderPath
    correct_file = os.listdir(domain_folder)
    correct_path = []
    correct_domain_info = []
    for file in correct_file:
        correct_path.append(join(domain_folder, file))
        correct_domain_info.append(DomainInfo.get_from_domainfile(join(domain_folder, file)))

    userMessage("Checking GDB Domains.")

    check_domains = checkGDBDomains(session)
    if check_domains != 0:
        userMessage("Issues found with GDB domains. Correcting issues for all or user-selected domains.")
    elif check_domains == 0:
        userMessage("GDB domains are already correct. Exiting tool.")
        return

    dataset_path = join(input_gdb, "NG911")
    # userMessage(dataset_path)
    arcpy.env.workspace = dataset_path
    # feature_classes = arcpy.ListFeatureClasses(wild_card="*", feature_type="All", feature_dataset=dataset_path)
    feature_classes = arcpy.ListFeatureClasses()
    fc_domain_fields = []
    # userMessage(feature_classes)
    for fc in feature_classes:
        fc_fields = arcpy.ListFields(fc)
        fc_name_btw = basename(fc)
        for field in fc_fields:
            if field.domain not in (None, " ", ""):
                # userMessage("Appending to fc_domain_fields.")
                fc_domain_fields.append({fc_name_btw: (field.name, field.domain)}) # domain_fields = [{a: (a, a)},{b: (b, b)},{c: (c, c)},{d: (d, d)}...]

    for index_key, fix_domain in enumerate(fix_domain_list):
        if fix_domain not in ["", "#", None]:
            userMessage("Fixing user-selected GDB domains.")
            # userMessage(fix_domain)
            # REMOVES DOMAINS FROM FIELDS IN FEATURE CLASSES
            for fc_domain_dict in fc_domain_fields:
                fc_domain_name = fc_domain_dict.values()[0][1]
                fc_name = fc_domain_dict.keys()[0]
                fc_field = fc_domain_dict.values()[0][0]
                if fc_domain_name == fix_domain:
                    userMessage("Removing %s domain from %s field in %s feature class." % (fc_domain_name, fc_field, fc_name))
                    fc_name_path = join(dataset_path, fc_name)
                    arcpy.RemoveDomainFromField_management(fc_name_path, fc_field)

            check_name = []
            for fc_domain_dict in fc_domain_fields:
                # fc_domain_name = fc_domain_dict.values()[0][1]
                # fc_name = fc_domain_dict.keys()[0]
                fc_domain_name = fc_domain_dict.values()[0][1]
                if fix_domain not in check_name and fix_domain == fc_domain_name:
                    # DELETE DOMAIN FROM GDB
                    userMessage("Removing %s domain from GDB." % (fix_domain))
                    arcpy.DeleteDomain_management(input_gdb, fix_domain)
                    # CREATE CORRECT DOMAIN
                    userMessage("Adding %s domain to GDB." % (correct_domain_info[index_key].domain_name))
                    arcpy.CreateDomain_management(input_gdb, correct_domain_info[index_key].domain_name,
                                          correct_domain_info[index_key].domain_description,
                                          field_type="TEXT")
                    # Assign coded values to domain
                    info_dict = correct_domain_info[index_key].domain_dict
                    for code in info_dict:
                        code_desc = str(info_dict[code])
                        dom_name = str(correct_domain_info[index_key].domain_name)
                        arcpy.AddCodedValueToDomain_management(input_gdb, dom_name, str(code), code_desc)

                    check_name.append(fix_domain)
                elif fix_domain in check_name:
                    pass

            # ASSIGN DOMAINS TO FEATURE CLASSES
            for fc_domain_dict in fc_domain_fields:
                fc_name = fc_domain_dict.keys()[0]
                fc_field = fc_domain_dict.values()[0][0]
                fc_domain_name = fc_domain_dict.values()[0][1]
                fc_path = join(dataset_path, fc_name)
                if fix_domain == fc_domain_name:
                    # Assign domain to field in feature class
                    userMessage("Assigning %s domain to %s field in %s feature class." % (correct_domain_info[index_key].domain_name, fc_field, fc_name))
                    arcpy.AssignDomainToField_management(fc_path, fc_field, correct_domain_info[index_key].domain_name)

if __name__ == '__main__':
    main()
