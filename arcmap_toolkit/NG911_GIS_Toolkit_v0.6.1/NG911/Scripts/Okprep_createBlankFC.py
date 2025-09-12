#-------------------------------------------------------------------------------
# Name:        Okprep_createBlankFC.py
# Purpose:     Converts a standard compliant feature class
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     October 16, 2020
# Modified:    October 16, 2020
# Copyright:   (c) Emma Marie Baker 2020, Riley Baird, 2020
#-------------------------------------------------------------------------------

## Imports
from arcpy import AddField_management, CreateFeatureclass_management, Exists, Append_management
import arcpy
from os.path import join
from NG911_User_Messages import *
from NG911_arcpy_shortcuts import FieldInfo, map_NG911_feature_class

try:
    from typing import List
except:
    pass


def create_blank_feature_class(geometry, fieldFile, gdbpath, correct_name, required = True):
    # type: (str, str, str, str, bool) -> str
    """
    Creates a standards-compliant blank feature class. In order, this function:

    * Gets standard field information from a text file
    * Creates feature class based on standards

    Parameters
    ----------
    geometry : str
        One of "POINT", "POLYLINE", or "POLYGON" that describes the type of feature class to generate
    fieldFile : str
        Full path to the text file containing the standard field information

    Returns
    -------
    str
        "NAME ISSUE" - Feature class name already exists in geodatabase.
        "FIELD ISSUE" - Field could not be added to the feature class.
        "SUCCESS" - Feature class with all standards-compliant fields has been added to the geodatabase.
    """

    # Ensure geometry argument is valid; raise exception if not
    if geometry not in ["POINT", "POLYLINE", "POLYGON"]:
        raise ValueError('Argument geometry in create_feature_class must be one of "POINT", "POLYLINE", or "POLYGON".')

    # Open Field Files
    correctFields = FieldInfo.get_from_text(fieldFile)  # List of FieldInfo objects; one for each line in fieldFile
    # userMessage(inputLayer)
    # userMessage("Old Fields: %s" % str(len(fieldNames)))
    # userMessage("Correct Fields: " + str(len(correctFields)))

    # ## Create new Address layer parameters
    # indVal = inputLayer.rindex("\\")
    # nName = inputLayer[(indVal+1):] # Name
    # if Exists(join(gdbpath,correct_name)):
    #     newName = str(nName)+"_new"
    #     userWarning('%s already exists. Adding "_new" to end of already existing name.' % correct_name)
    # else:
    #     newName = correct_name

    newName = correct_name

    # gdbPath = inputLayer[0:indVal] # GDB Path
    if required:
        newdataset = join(gdbpath, "NG911")
        newfcpath = join(newdataset, newName)
    else:
        newdataset = join(gdbpath, "OptionalLayers")
        newfcpath = join(newdataset, newName)

    # fieldDict = dict(zip(correctFields, fieldNames))
    # userMessage(fieldDict)

    ## Create new Address layer
    if not Exists(newfcpath):
        userMessage("Creating new Feature Class for " + newName)
        CreateFeatureclass_management(newdataset, newName, geometry, has_z="ENABLED", has_m="ENABLED")
    else:
        userWarning("Feature Class %s already exists. Please check the input geodatabase." % newName)
        return "NAME ISSUE"

    ## Add correct field names to the new Address layer
    userMessage("Adding correct field names to " + newName)
    currentFields = arcpy.ListFields(newfcpath)
    for field_info_object in correctFields:
        if field_info_object.name not in currentFields:
            try:
                AddField_management(in_table=newfcpath, field_name=field_info_object.name,
                                    field_type=field_info_object.type, field_length=field_info_object.length,
                                    field_domain=field_info_object.domain)
            except:
                return "FIELD ISSUE"

    userMessage("Output feature class %s successfully created." % newName)
    return "SUCCESS"

