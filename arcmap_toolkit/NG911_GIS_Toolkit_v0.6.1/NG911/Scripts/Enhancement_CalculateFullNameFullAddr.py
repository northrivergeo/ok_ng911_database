#-------------------------------------------------------------------------------
# Name:        Enhancement_CalculateFullNameFullAddr
# Purpose:     Calculates the FullName and/or FullAddr field(s) for input
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     June 08, 2021
# Modified:    June 08, 2021
#-------------------------------------------------------------------------------

#import modules
from arcpy import GetParameterAsText, CalculateField_management, MakeFeatureLayer_management, SelectLayerByAttribute_management, GetCount_management
from arcpy.da import UpdateCursor, Editor
from os.path import basename, dirname

from NG911_arcpy_shortcuts import FieldInfo
from NG911_User_Messages import *
from NG911_GDB_Objects import getFCObject, NG911_RoadCenterline_Object, NG911_Address_Object

try:
    from typing import Union, List
except:
    pass

def main():
    layer = GetParameterAsText(0)
    name_check = GetParameterAsText(1)
    addr_check = GetParameterAsText(2)

    #define object & field list
    gdb = dirname(dirname(layer))
    fc_basename = basename(layer)
    name_field_list = []
    addr_field_list = []
    if fc_basename == "ROAD_CENTERLINE":
        fc_object = getFCObject(layer)  #type: NG911_RoadCenterline_Object
        if name_check == "true":
            name_field_list = fc_object.FULLNAME_FIELDS
    elif fc_basename == "ADDRESS_POINT":
        fc_object = getFCObject(layer)  # type:NG911_Address_Object
        if name_check == "true":
            name_field_list = fc_object.FULLNAME_FIELDS
        if addr_check == "true":
            addr_field_list = fc_object.FULLADDR_FIELDS
    else:
        fc_object = None  # type: None
        userMessage(layer + " does not work with this tool. Please select the NG911 road centerline or address point file.")

    #make sure the object is something
    if fc_object is not None:
        # start edit session

        edit = Editor(gdb)
        edit.startEditing(False, False)

        if name_check == "true":
            userMessage("Calculating FullName for %s." % fc_basename)

            fullname_field_info = FieldInfo.get_from_feature_class(gdb, fc_basename, field=name_field_list[0])  # type: FieldInfo
            fullname_max_length = fullname_field_info.length

            with UpdateCursor(layer, name_field_list) as rows:
                for row in rows:
                    expression = [unicode(x) for x in row[1:] if x not in ("", " ", None)]  # Select only fields with useful values
                    expression = " ".join(expression)  # Concatenate; separate with spaces

                    if len(expression) > fullname_max_length:
                        format_string_arguments = (expression, len(expression), fullname_field_info.name, fullname_max_length)
                        userWarning("Calculated FullName is too long: \"%s\" is %i characters, but the length of the %s field is %i. This record will be set to null." % format_string_arguments)
                        expression = None

                    row[0] = expression
                    rows.updateRow(row)

        if addr_check == "true":
            userMessage("Calculating FullAddr for %s." % fc_basename)

            fulladdr_field_info = FieldInfo.get_from_feature_class(gdb, fc_basename, field=addr_field_list[0])  # type: FieldInfo
            fulladdr_max_length = fulladdr_field_info.length

            with UpdateCursor(layer, addr_field_list) as rows:
                for row in rows:
                    expression = [unicode(x) for x in row[1:] if x not in ("", " ", None)]  # Select only fields with useful values
                    expression = " ".join(expression)  # Concatenate; separate with spaces

                    if len(expression) > fulladdr_max_length:
                        format_string_arguments = (expression, len(expression), fulladdr_field_info.name, fulladdr_max_length)
                        userWarning("Calculated FullAddr is too long: \"%s\" is %i characters, but the length of the %s field is %i. This record will be set to null." % format_string_arguments)
                        expression = None

                    row[0] = expression
                    rows.updateRow(row)

        edit.stopEditing(True)

if __name__ == '__main__':
    main()
