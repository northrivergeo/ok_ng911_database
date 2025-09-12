#-------------------------------------------------------------------------------
# Name:        Enhancement_SplitSingleESBLayer
# Purpose:     Splits a single ESB layer into separate EMS, Fire and Law boundaries
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     06/29/2020
# Modified:    06/29/2020
#-------------------------------------------------------------------------------

from NG911_User_Messages import *
from NG911_GDB_Objects import getFCObject
from NG911_arcpy_shortcuts import ListFieldNames, FieldInfo
from arcpy import GetParameterAsText, Exists, Dissolve_management, DeleteField_management, AddField_management
from arcpy.da import SearchCursor
from os.path import join, basename
from itertools import izip
from NG911_GDB_Objects import NG911_Session

def split_ESN():

    # Get parameters
    combined_input = GetParameterAsText(0)
    gdb = GetParameterAsText(1)
    # fields_dir = GetParameterAsText(2)
    ems_field = GetParameterAsText(2)
    fire_field = GetParameterAsText(3)
    law_field = GetParameterAsText(4)
    dissolve_field_list = [ems_field, fire_field, law_field]

    session = NG911_Session(gdb)
    fields_dir = session.fieldsFolderPath

    # Open Field Files
    fields_files = ["ESB_EMS_BOUNDARY", "ESB_FIRE_BOUNDARY", "ESB_LAW_BOUNDARY"]
    fields_filepaths = [join(fields_dir, fields_file + ".txt") for fields_file in fields_files]  # Compute full paths to txt files
    fields_of_outputs = {}
    for filepath, fields_file in zip(fields_filepaths, fields_files):
        field_info = FieldInfo.get_from_text(filepath)
        fields_of_outputs[fields_file] = field_info
        # open_file = open(fields_file).readlines()
        # firstline = open_file.pop(0)
        # correctFields = []
        # fieldType = []
        # fieldLength = []
        # fieldDomain = []
        # for line in open_file:
        #     lineSplit = line.split("|")
        #     correctFields.append(lineSplit[0])
        #     fieldType.append(lineSplit[1])
        #     if lineSplit[2] == "":
        #         fieldLength.append("")
        #     else:
        #         fieldLength.append(lineSplit[2])
        #     fieldDomain.append(lineSplit[3].strip("\n"))
        # fields_of_outputs[fields_file] = [correctFields, fieldType, fieldLength, fieldDomain]




    ems_output = join(gdb, "NG911/ESB_EMS_BOUNDARY")  # Changed to OK Fields
    fire_output = join(gdb, "NG911/ESB_FIRE_BOUNDARY")  # Changed to OK Fields
    law_output = join(gdb, "NG911/ESB_LAW_BOUNDARY")  # Changed to OK Fields
    output_fc_list = [ems_output, fire_output, law_output]

    for (dissolve_field, output_fc) in izip(dissolve_field_list, output_fc_list):
        Dissolve_management(combined_input, output_fc, dissolve_field)

        for existing_field in ListFieldNames(output_fc):
            if existing_field not in ["OBJECTID", "SHAPE"]:
                try:
                    DeleteField_management(output_fc, existing_field)
                except:
                    # Ignore if a certain field cannot be deleted
                    userWarning("Could not delete field %s from %s." % (existing_field, basename(output_fc)))

    for i, ems_field_info in enumerate(fields_of_outputs["ESB_EMS_BOUNDARY"]):  # Iterate over all names of fields to add
        AddField_management(
            in_table=ems_output,
            field_name=fields_of_outputs["ESB_EMS_BOUNDARY"][i].name,
            field_type=fields_of_outputs["ESB_EMS_BOUNDARY"][i].type,
            field_length=fields_of_outputs["ESB_EMS_BOUNDARY"][i].length,
            field_domain=fields_of_outputs["ESB_EMS_BOUNDARY"][i].domain
        )
        AddField_management(
            in_table=fire_output,
            field_name=fields_of_outputs["ESB_FIRE_BOUNDARY"][i].name,
            field_type=fields_of_outputs["ESB_FIRE_BOUNDARY"][i].type,
            field_length=fields_of_outputs["ESB_FIRE_BOUNDARY"][i].length,
            field_domain=fields_of_outputs["ESB_FIRE_BOUNDARY"][i].domain
        )
        AddField_management(
            in_table=law_output,
            field_name=fields_of_outputs["ESB_LAW_BOUNDARY"][i].name,
            field_type=fields_of_outputs["ESB_LAW_BOUNDARY"][i].type,
            field_length=fields_of_outputs["ESB_LAW_BOUNDARY"][i].length,
            field_domain=fields_of_outputs["ESB_LAW_BOUNDARY"][i].domain
        )

        userMessage("Successfully added field %s." % fields_of_outputs["ESB_EMS_BOUNDARY"][i].name)

if __name__ == "__main__":
    split_ESN()