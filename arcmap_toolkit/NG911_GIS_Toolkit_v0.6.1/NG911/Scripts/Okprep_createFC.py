#-------------------------------------------------------------------------------
# Name:        Okprep_createFC.py
# Purpose:     Converts ArcGIS field inputs from a Point, Polyline, or Polygon
#              layer to standard compliant field names.
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     February 13, 2020
# Modified:    February 11, 2021
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


def create_feature_class(geometry, inputLayer, fieldFile, fieldNames, gdbpath, correct_name, required = True):
    # type: (str, str, str, List[str], str, str, bool) -> None
    """
    Performs the field mapping with parameters from other Okprep tools. In order, this function:

    * Gets standard field information from a text file
    * Creates feature class based on standards
    * Creates field map based on user inputs
    * Appends records from old (non-standards-compliant) to new (standards-compliant) feature class using field map

    The resulting feature class will have the same name as the input with the suffix "_new" and will need to be renamed
    to the standards-compliant name.

    Parameters
    ----------
    geometry : str
        One of "POINT", "POLYLINE", or "POLYGON" that describes the type of feature class to generate
    inputLayer : str
        Full path to the input (old, non-standards-compliant) feature class
    fieldFile : str
        Full path to the text file containing the standard field information
    fieldNames : list of str
        List of user-entered (old, non-standards-compliant) field names for field mapping
    """

    # Ensure geometry argument is valid; raise exception if not
    if geometry not in ["POINT", "POLYLINE", "POLYGON"]:
        raise ValueError('Argument geometry in create_feature_class must be one of "POINT", "POLYLINE", or "POLYGON".')

    # Open Field Files
    correctFields = FieldInfo.get_from_text(fieldFile)  # List of FieldInfo objects; one for each line in fieldFile
    # userMessage(inputLayer)
    # userMessage("Old Fields: %s" % str(len(fieldNames)))
    # userMessage("Correct Fields: " + str(len(correctFields)))

    ## Create new Address layer parameters
    indVal = inputLayer.rindex("\\")
    nName = inputLayer[(indVal+1):] # Name
    if Exists(join(gdbpath,correct_name)):
        newName = unicode(nName)+"_new"
        userWarning('Feature class name "%s" is already in use in output GDB. The feature class created by this tool will be called "%s_new". This new feature class must be renamed properly before submission.' % (correct_name, correct_name))
    else:
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
        userMessage("Creating new Feature Class for " + nName)
        CreateFeatureclass_management(newdataset, newName, geometry, has_z="ENABLED", has_m="ENABLED")

    ## Add correct field names to the new Address layer
    userMessage("Adding correct field names to " + newName)
    currentFields = arcpy.ListFields(newfcpath)
    for field_info_object in correctFields:
        if field_info_object.name not in currentFields:
            AddField_management(in_table=newfcpath, field_name=field_info_object.name,
                                    field_type=field_info_object.type, field_length=field_info_object.length,
                                    field_domain=field_info_object.domain)

    ## Mapping fields between the old Address layer (ArcGIS Inputs) and the new Address layer
    userMessage("Mapping Fields")
    conversion_dict = {
        new_name.name: old_name for new_name, old_name in zip(correctFields, fieldNames)
    }
    fieldMappings = map_NG911_feature_class(inputLayer, newfcpath, conversion_dict, correct_fields=correctFields)

    # Country/county check
    for new_name, old_name in conversion_dict.items():
        # debugMessage("New: %s ... Old: %s" % (new_name, old_name))
        if "COUNTRY" in new_name.upper():
            if "TR" not in old_name.upper():
                # TR could be expected to be in most reasonable abbreviations for "country", like "CTRY", "CNTRY"
                userWarning('The value "%s" was provided for the "%s" field. Ensure provided field is correct.' % (old_name, new_name))
        if "COUNTY" in new_name.upper():
            if "TR" in old_name.upper():
                # There might be an "R" in the old field (as in "right"), but probably not a "TR" in any "county" field
                userWarning('The value "%s" was provided for the "%s" field. Ensure provided field is correct.' % (old_name, new_name))

    ## Append old Address values to new Address layer base on field mapping
    userMessage("Append from old to new.")
    try:
        Append_management(inputLayer, newfcpath, schema_type="NO_TEST", field_mapping=fieldMappings)
    except Exception as e:
        userWarning("Error in Append function: \n" + unicode(e))
        userWarning('The feature class "%s" was created, but no records were written to it due to a field mapping error. Check the parameters.' % newName)
    else:
        userMessage("Output feature class %s successfully created." % newName)
    # userMessage("NOTICE: New feature class may not have a standards-compliant name. It must be renamed properly before submission.")