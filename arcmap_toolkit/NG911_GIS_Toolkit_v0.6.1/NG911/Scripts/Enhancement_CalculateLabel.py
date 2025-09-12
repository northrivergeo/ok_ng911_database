#-------------------------------------------------------------------------------
# Name:        Enhancement_CalculateLabel
# Purpose:     Calculates the label field for input
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     11/09/2015
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------

#import modules
from arcpy import GetParameterAsText, CalculateField_management, MakeFeatureLayer_management, SelectLayerByAttribute_management, GetCount_management
from arcpy.da import UpdateCursor, Editor
from os.path import basename, dirname
from NG911_User_Messages import *
from NG911_GDB_Objects import getFCObject, NG911_RoadCenterline_Object, NG911_Address_Object
from NG911_arcpy_shortcuts import FieldInfo

try:
    from typing import Union, List
except:
    pass

def main():
    layer = GetParameterAsText(0)
    # updateBlanksOnly = GetParameterAsText(1)

    expression = ""  # type: Union[str, List[str], None]
    #a = ""  # type: object
    field_list = []  # type: List[str]
    gdb = dirname(dirname(layer))

    #define object & field list
    fc_basename = basename(layer)
    if fc_basename in ("ROAD_CENTERLINE", "ADDRESS_POINT"): # Changed to OK Fields
        fc_object = getFCObject(layer)  # type: Union[NG911_RoadCenterline_Object, NG911_Address_Object, None]
        field_list = fc_object.LABEL_FIELDS
    else:
        fc_object = None
        userMessage(layer + " does not work with this tool. Please select the NG911 road centerline or address point file.")

    #make sure the object is something
    if fc_object is not None:
        # start edit session

        userMessage("Calculating Label.")
        label_field_info = FieldInfo.get_from_feature_class(gdb, fc_basename, field=field_list[0])  # type: FieldInfo
        label_max_length = label_field_info.length

        edit = Editor(gdb)
        edit.startEditing(False, False)

        with UpdateCursor(layer, field_list) as rows:
            for row in rows:

                # Make expression
                expression = [unicode(x) for x in row[1:] if x not in ("", " ", None)]
                expression = " ".join(expression)

                if len(expression) > label_max_length:
                    format_string_arguments = (expression, len(expression), label_field_info.name, label_max_length)
                    userWarning("Calculated Label is too long: \"%s\" is %i characters, but the length of the %s field is %i. This record will be set to null." % format_string_arguments)
                    expression = None

                # Commit expression to label field
                # userMessage("Label: " + expression)
                row[0] = expression
                rows.updateRow(row)

        edit.stopEditing(True)

if __name__ == '__main__':
    main()
