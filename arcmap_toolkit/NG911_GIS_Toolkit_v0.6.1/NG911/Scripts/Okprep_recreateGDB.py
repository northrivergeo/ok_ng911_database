#-------------------------------------------------------------------------------
# Name:        Conversion_recreateGDB
# Purpose:     Creates a new gdb with feature classes that meet OK NG911 Standards
# Requires:    Advanced Licensing
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     March 01, 2020
# Modified:    July 15, 2020
# Copyright:   (c) Emma Marie Baker, Riley Baird
#-------------------------------------------------------------------------------
## Imports
from arcpy import (GetParameterAsText, Exists,
    CreateFileGDB_management, CreateFeatureDataset_management)
from os.path import join, basename

try:
    from typing import List
except:
    pass

from Okprep_createBlankFC import create_blank_feature_class
from NG911_User_Messages import *
from glob import glob
import arcpy
from NG911_arcpy_shortcuts import DomainInfo, FieldInfo
from Okprep_AssignAllDomains import *
from NG911_GDB_Objects import NG911_Session


def main():

    # gdbCurrent = GetParameterAsText(0)
    folderPath = GetParameterAsText(0)
    newName = GetParameterAsText(1)
    proj = GetParameterAsText(2)
    # domainFolder = GetParameterAsText(3)
    addressLayer = GetParameterAsText(3)
    create_address_fc = GetParameterAsText(4)
    roadLayer = GetParameterAsText(5)
    create_road_fc = GetParameterAsText(6)
    discrepancyAgencyLayer = GetParameterAsText(7)
    create_discrepancy_agency_fc = GetParameterAsText(8)
    ESZ = GetParameterAsText(9)
    create_esz_fc = GetParameterAsText(10)
    ESB_FIRE = GetParameterAsText(11)
    create_fire_fc = GetParameterAsText(12)
    ESB_LAW = GetParameterAsText(13)
    create_law_fc = GetParameterAsText(14)
    ESB_EMS = GetParameterAsText(15)
    create_ems_fc = GetParameterAsText(16)
    PSAP = GetParameterAsText(17)
    create_psap_fc = GetParameterAsText(18)
    # cityLayer = GetParameterAsText(19)

    layers = [addressLayer, roadLayer, discrepancyAgencyLayer, ESZ, ESB_FIRE, ESB_LAW, ESB_EMS, PSAP]
    requiredLayers = ["ADDRESS_POINT", "ROAD_CENTERLINE", "DISCREPANCYAGENCY_BOUNDARY", "ESZ_BOUNDARY",
                     "ESB_FIRE_BOUNDARY", "ESB_LAW_BOUNDARY", "ESB_EMS_BOUNDARY", "PSAP_BOUNDARY"]
    optionalLayers = ["MUNICIPAL_BOUNDARY"]

    allLayers = requiredLayers + optionalLayers

    createLayers = [create_address_fc, create_road_fc, create_discrepancy_agency_fc, create_esz_fc, create_fire_fc, create_law_fc, create_ems_fc, create_psap_fc]

    if ".gdb" not in newName[-4:]:
        newName = newName + ".gdb"

    newGDB = join(folderPath, newName)

    # Create new GDB
    if not Exists(newGDB):
        CreateFileGDB_management(folderPath, newName)

    # Create new Dataset
    newDS = join(newGDB, "NG911")
    if not Exists(newDS):
        sr = proj
        CreateFeatureDataset_management(newGDB, "NG911", sr)

    # Create new Dataset
    newDS_OL = join(newGDB, "OptionalLayers")
    if not Exists(newDS_OL):
        sr = proj
        CreateFeatureDataset_management(newGDB, "OptionalLayers", sr)

    session = NG911_Session(newGDB)
    domainFolder = session.domainsFolderPath
    fields_folder = session.fieldsFolderPath

    domainFullPathList = glob(join(domainFolder, "*.txt")) # All Domains txt files
    domainList = [basename(val) for val in domainFullPathList] # Domain File Names
    # domainList = ["COUNTRY_DOMAINS.txt", "COUNTY_DOMAINS.txt", "DIRECTION_DOMAINS.txt", "EXCEPTION_DOMAINS.txt", ""LEVEL_DOMAINS.txt", "LGCYDIRECTION_DOMAINS.txt",
    #               "LGCYSTREETTYPE_DOMAINS.txt", "NUMBER_DOMAINS.txt", "ONEWAY_DOMAINS.txt", "PARITY_DOMAINS.txt", "PLACEMENT_DOMAINS.txt",
    #               "PLACETYPE_Domains.txt", "RCLSIDE_DOMAINS.txt", "ROADCLASS_DOMAINS.txt", "SEPARATOR_DOMAINS.txt", "SPEEDLIMIT_DOMAINS.txt", "STATE_DOMAINS.txt",
    #               "STORMSHELTER_DOMAINS.txt", "STREETTYPE_Domains.txt", "YESNO_DOMAINS.txt"]

    ## Fields Folder paths
    # toolpath = dirname(domainFolder) # Toolpath
    # fields_folder = join(toolpath, "Fields") # Fields Folder
    fieldsFullPathList = glob(join(fields_folder,"*.txt")) # All Fields txt files
    remove_fields = [join(fields_folder,"DASC_Communication.txt"),join(fields_folder,"FieldValuesCheckResults.txt"),join(fields_folder,"TemplateCheckResults.txt")] # txt files to be removed from Fields path list
    fieldsPathList = [i for i in fieldsFullPathList if i not in remove_fields] # Fields Path List excluding removed txt files
    fieldsList = [basename(val) for val in fieldsPathList] # Fields File names
    fields_strip = [val.replace(".txt","") for val in fieldsList]



    # Create Domain Tables
    assign_all_domains(domainFolder, newGDB)
    # existing_domains = arcpy.da.ListDomains(newGDB)
    # existing_domainnames = [existing_domain.name for existing_domain in existing_domains]
    # for dom in domainList:
    #     dmFld = join(domainFolder, dom)
    #     domain_info = DomainInfo.get_from_domainfile(dmFld)
    #     if domain_info.domain_name not in existing_domainnames:
    #         arcpy.CreateDomain_management(in_workspace=newGDB, domain_name=domain_info.domain_name, domain_description=domain_info.domain_description, field_type="TEXT")
    #
    #         for code in domain_info.domain_dict:
    #             arcpy.AddCodedValueToDomain_management(newGDB, domain_info.domain_name, code, domain_info.domain_dict[code])
    #
    #         arcpy.SortCodedValueDomain_management(newGDB, domain_info.domain_name, "CODE", "ASCENDING")
    #
    #         userMessage("Added %s domain." % domain_info.domain_name)
    #     else:
    #         userMessage("%s already exists." % domain_info.domain_name)


    # Work with Feature Class
    if len(layers) > 0:
        for key, layer in enumerate(layers):
            # userMessage(layer)
            userMessage("------------")
            # userMessage("------------")
            if layer not in ["",None,"#"]:
                # userMessage(layer)
                # Create new Feature Class with correct name
                layer_basename = basename(layer).upper()
                # optionalLayers = [val.upper() for val in optionalLayers]
                # requiredLayers = [val.upper() for val in requiredLayers]
                geometry = ""
                field_info_object = []
                gdbpath = ""
                newLayers = ""
                newLayerPath = ""
                if key >= 8: # when the key is 8 or greater, we are in optional layers
                    indValLayer = layer.rindex("\\")
                    FCName = layer[(indValLayer + 1):]
                    userMessage("Converting old " + FCName + " to new " + allLayers[key])
                    newLayers = unicode(allLayers[key])
                    gdbpath = newDS_OL
                    newLayerPath = join(newDS_OL,newLayers)
                    for key2, fieldpath in enumerate(fieldsPathList):
                        if allLayers[key] == fields_strip[key2]:
                            # userMessage("Optional: %s" % fields_strip[key2])
                            # userMessage("Optional: %s" % (allLayers[key]))
                            field_info_object = FieldInfo.get_from_text(fieldpath)
                            if fields_strip[key2] == "ADDRESS_POINT":
                                geometry = "POINT"
                            elif fields_strip[key2] == "ROAD_CENTERLINE":
                                geometry = "POLYLINE"
                            else:
                                geometry = "POLYGON"
                        else:
                            continue

                elif key < 8: # when the key is less than 8, we are in required layers
                    indValLayer = layer.rindex("\\")
                    FCName = layer[(indValLayer+1):]
                    userMessage("Converting old " + FCName + " to new " + allLayers[key])
                    newLayers = unicode(allLayers[key])
                    gdbpath = newDS
                    newLayerPath = join(newDS, newLayers)
                    for key2, fieldpath in enumerate(fieldsPathList):
                        if allLayers[key] == fields_strip[key2]:
                            # userMessage("Required: %s" %fields_strip[key2])
                            # userMessage("Required: %s" %(allLayers[key]))
                            field_info_object = FieldInfo.get_from_text(fieldpath)  # type: List[FieldInfo]
                            if fields_strip[key2] == "ADDRESS_POINT":
                                geometry = "POINT"
                            elif fields_strip[key2] == "ROAD_CENTERLINE":
                                geometry = "POLYLINE"
                            else:
                                geometry = "POLYGON"
                        else:
                            continue

                arcpy.CreateFeatureclass_management(gdbpath, newLayers, geometry, has_z="ENABLED", has_m="ENABLED")
                for field in field_info_object:
                    # userMessage("Adding %s field" %field.name)
                    arcpy.AddField_management(in_table=newLayerPath, field_name=field.name,
                                    field_type=field.type, field_length=field.length,
                                    field_domain=field.domain)
                try:
                    arcpy.Append_management(layer, newLayerPath, schema_type="TEST")
                    # arcpy.Append_management(layer, newLayerPath, schema_type="NO_TEST")
                except:
                    userWarning("Could not append old feature class %s to new feature class. Please check the schema." % FCName)
                    if createLayers[key] == "false":
                        arcpy.Delete_management(newLayerPath)
                    else:
                        userWarning("Blank feature class %s created." % allLayers[key])

            else:
                userMessage("Feature Class %s was not provided." % allLayers[key])
                if key < 8 and createLayers[key] == "true":
                    # Creates blank FCs for required layers only
                    # for key2, val in enumerate(layers[:-1]):
                    userMessage("Beginning creation of blank feature class...")
                    gdbpath = newGDB
                    if requiredLayers[key] == "ADDRESS_POINT":
                        geometry = "POINT"
                    elif requiredLayers[key] == "ROAD_CENTERLINE":
                        geometry = "POLYLINE"
                    else:
                        geometry = "POLYGON"
                    fieldFile = join(fields_folder, requiredLayers[key] + ".txt")
                    blank_result = create_blank_feature_class(geometry, fieldFile, gdbpath, requiredLayers[key])
                    if blank_result == "FIELD ISSUE":
                        userWarning("Failed to create blank feature class %s. Deleting FC." % requiredLayers[key])
                        arcpy.Delete_management(join(gdbpath, requiredLayers[key]))
                    elif blank_result == "NAME ISSUE":
                        userWarning("Failed to create blank feature class %s. Feature class name already exists." % requiredLayers[key])
                        continue
                    elif blank_result == "SUCCESS":
                        userMessage("Blank Feature Class %s has been added to the GDB." % requiredLayers[key])
                else:
                    userMessage("Not creating feature class.")
                continue

    # # Creates blank FCs for required layers only
    # if "" in layers and blankFC == "true":
    #     userMessage("Beginning creation of blank feature class...")
    #     for key, val in enumerate(layers[:-1]):
    #         if val == "":
    #             gdbpath = newGDB
    #             if requiredLayers[key] == "ADDRESS_POINT":
    #                 geometry = "POINT"
    #             elif requiredLayers[key] == "ROAD_CENTERLINE":
    #                 geometry = "POLYLINE"
    #             else:
    #                 geometry = "POLYGON"
    #             fieldFile = join(dirname(domainFolder), "Fields", requiredLayers[key] + ".txt")
    #             create_feature_class(geometry, fieldFile, gdbpath, requiredLayers[key])

if __name__ == '__main__':
    main()

# openDomain = open(dmFld).readlines()
#
# firstline = openDomain.pop(0)
# firstSplit = firstline.split("|")
# descField = str(firstSplit[1].strip("\n"))
# descFieldUnder = str(descField.replace(" ", "_"))
#
# arcpy.Delete_management("in_memory")
#
# # userMessage(str(descFieldUnder) + "  |  " + str(type(descFieldUnder)))
#
# domainTable = arcpy.CreateTable_management("in_memory", domName)
# AddField_management(domainTable, 'Values', "TEXT", field_length=254)
# # AddField_management(domainTable, "Definition", "TEXT", field_length=254)
# AddField_management(domainTable, str(descFieldUnder), "TEXT", field_length=254)
#
# # fieldsduh = arcpy.ListFields(domainTable)
# # for field in fieldsduh:
# #     userMessage(field.name)
#
# # cursor = arcpy.da.InsertCursor(domainTable, ["Values", "Definition"])
# cursor = arcpy.da.InsertCursor(domainTable, ['Values', str(descFieldUnder)])
# for line in openDomain:
#     domainSplit = line.split("|")
#     domainSplit[-1] = domainSplit[-1].strip("\n")
#     # for key, val in enumerate(domainSplit):
#     cursor.insertRow([domainSplit[0], domainSplit[-1]])
#
# newDomName = str(dom[:-12])
# # userMessage(newDomName)
#
# arcpy.TableToDomain_management(in_table=domainTable, code_field="Values", description_field=descFieldUnder, in_workspace=newGDB, domain_name=newDomName)

# domainList = arcpy.da.ListDomains(newGDB)
# for domain in domainList:
#     if domain.description == descFieldUnder:
#         domain.description = descField
#         arcpy.AlterDomain_management(newGDB, domain_name=domain, new_domain_description=descField)
#     else:
#         continue

# # Cycle through fields to remove domain from field
# domainArray = []
# for field in fields:
#     nfield = str(field.name)
#     nDomain = str(field.domain)
#     # userMessage(field.domain)
#     if nDomain != "":
#         domainArray.append(nDomain)
#         userMessage("Removing " + str(field.domain) + " from new Feature Class Field " + nfield)
#         arcpy.RemoveDomainFromField_management(newLayerPath, nfield)
#
# # Cycle through fields to find out if removal was successful
# newfields = arcpy.ListFields(newLayerPath)
# for field in newfields:
#     nfield = str(field.name)
#     nDomain = str(field.domain)
#     if nDomain != "":
#         userMessage("Issues with removing domain " + nDomain + " in field " + nfield)
#
# # Delete old domains from new GDB
# # domainsNew = arcpy.da.ListDomains(newGDB)
# domainArrayUni = list(set(domainArray))
# # userMessage(domainArrayUni)
# # userMessage(len(domainArrayUni))
#
# for dom in domainArrayUni:
#     domStr = str(dom)
#     userMessage("Deleting domain from gdb: " + domStr)
#     arcpy.DeleteDomain_management(newGDB, domStr)
#
# # Assign correct domains to the correct fields
# newfields = arcpy.ListFields(newLayerPath)
# # userMessage("------------")
# userMessage("Assigning Domains to Fields.")
# # domainsNew = arcpy.da.ListDomains(newGDB)
# for field in newfields:
#     if field.name == 'PreDir':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "DIRECTION")
#     elif field.name == 'PreType':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "STREETTYPE")
#     elif field.name == 'PreTypeSep':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "SEPARATOR")
#     elif field.name == 'StreetType':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "STREETTYPE")
#     elif field.name == 'SufDir':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "DIRECTION")
#     elif field.name == 'Country':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "COUNTRY")
#     elif field.name == 'Country_L':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "COUNTRY")
#     elif field.name == 'Country_R':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "COUNTRY")
#     elif field.name == 'State':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "STATE")
#     elif field.name == 'State_L':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "STATE")
#     elif field.name == 'State_R':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "STATE")
#     elif field.name == 'County':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "COUNTY")
#     elif field.name == 'County_L':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "COUNTY")
#     elif field.name == 'County_R':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "COUNTY")
#     elif field.name == 'GrpQuarter':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == 'StrmSheltr':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "STORMSHELTER")
#     elif field.name == 'Basement':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == 'PlaceType':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "PLACETYPE")
#     elif field.name == 'Placement':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "PLACEMENT")
#     elif field.name == 'LgcyPreDir':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "LGCYDIRECTION")
#     elif field.name == 'LgcyType':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "LGCYSTREETTYPE")
#     elif field.name == 'LgcySufDir':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "LGCYDIRECTION")
#     elif field.name == 'Parity_L':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "PARITY")
#     elif field.name == 'Parity_R':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "PARITY")
#     elif field.name == 'RoadClass':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "ROADCLASS")
#     elif field.name == 'OneWay':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "ONEWAY")
#     elif field.name == 'FromLevel':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "LEVEL")
#     elif field.name == 'ToLevel':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "LEVEL")
#     elif field.name == 'BoundLane':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "LGCYDIRECTION")
#     elif field.name == 'DeadEnd':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == 'Lanes':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "NUMBER")
#     elif field.name == 'Toll':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == 'LtdAccess':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == 'Valid_L':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == 'Valid_R':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == 'SpeedLimit':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "SPEEDLIMIT")
#     elif field.name == 'TopoExcept':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "TopoExcept")
#     elif field.name == 'RCLSide':
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "RCLSide")
#     elif field.name == "PROV_L":
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == "PROV_R":
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == "GEOMSAG_L":
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")
#     elif field.name == "GEOMSAG_R":
#         arcpy.AssignDomainToField_management(newLayerPath, field.name, "YESNO")

#  "G:\ArcGIS\Project Files\NG911\NG911 GIS TOOL\1 - TEST DATA\BeaverCounty\Beaver_2019_0927.gdb\NG911\ESZ_BOUNDARY"