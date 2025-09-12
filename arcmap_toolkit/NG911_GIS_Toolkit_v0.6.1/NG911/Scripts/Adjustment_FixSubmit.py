#-------------------------------------------------------------------------------
# Name:        Adjustment_FixSubmit
# Purpose:     Fix SUBMIT field so all blanks or nulls become "Y"
#
# Author:      kristen (KS), Emma Baker (OK), Riley Baird (OK)
#
# Created:     10/23/2017
# Modified:    December 4, 2020
#-------------------------------------------------------------------------------
from arcpy import GetParameterAsText
from arcpy.da import Editor
from NG911_DataFixes import fixSubmit
from NG911_GDB_Objects import NG911_Session

def main():
    gdb = GetParameterAsText(0)
    ap_check = GetParameterAsText(1)
    road_check = GetParameterAsText(2)
    da_check = GetParameterAsText(3)
    esz_check = GetParameterAsText(4)
    psap_check = GetParameterAsText(5)
    ems_check = GetParameterAsText(6)
    fire_check = GetParameterAsText(7)
    law_check = GetParameterAsText(8)

    edit = Editor(gdb)
    edit.startEditing(False, False)

    fcs_check = [ap_check, road_check, da_check, esz_check, psap_check, ems_check, fire_check, law_check]

    session = NG911_Session(gdb)
    gdb_obj = session.gdbObject
    required = gdb_obj.requiredLayers
    # [self.AddressPoints, self.RoadCenterline, self.AuthoritativeBoundary, self.ESZ, self.PSAP] + [EMS, FIRE, LAW]

    fcs_list = []

    for key, val in enumerate(fcs_check):
        if val == "true":
            fcs_list.append(required[key])

    fixSubmit(gdb, fcs_list)

    edit.stopEditing(True)

if __name__ == '__main__':
    main()
