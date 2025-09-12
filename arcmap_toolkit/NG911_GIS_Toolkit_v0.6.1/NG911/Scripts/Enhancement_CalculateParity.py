"""
------------------------------------------------------------------------------
Name:        Enhancement_CalculateParity.py
Purpose:     Takes address ranges of a road centerline feature class and, from
             them, populates Parity_L and Parity_R as appropriate.

Author:      Baird (OK), Baker (OK)

Created:     April 29, 2021
Modified:    April 29, 2021
Copyright:   (c) Riley Baird, Emma Marie Baker
------------------------------------------------------------------------------
"""

from os.path import basename, dirname

import sys

from arcpy import GetParameterAsText
from arcpy.da import UpdateCursor, Editor

from NG911_GDB_Objects import getFCObject, NG911_RoadCenterline_Object
from NG911_User_Messages import *

try:
    from typing import List
except:
    pass


def main():
    rcl_fc = GetParameterAsText(0)  # type: str
    overwrite = GetParameterAsText(1)  # type: str  # (either "true" or "false")
    rcl_object = getFCObject(basename(rcl_fc))  # type: NG911_RoadCenterline_Object
    parity_l_field = rcl_object.PARITY_L  # type: str
    parity_r_field = rcl_object.PARITY_R  # type: str
    add_l_from_field = rcl_object.Add_L_From  # type: str
    add_l_to_field = rcl_object.Add_L_To  # type: str
    add_r_from_field = rcl_object.Add_R_From  # type: str
    add_r_to_field = rcl_object.Add_R_To  # type: str
    uniqueid = rcl_object.UNIQUEID  # type: str

    fields = [
        parity_l_field,   # 0
        parity_r_field,   # 1
        add_l_from_field, # 2
        add_l_to_field,   # 3
        add_r_from_field, # 4
        add_r_to_field,   # 5
        uniqueid          # 6
    ]  # type: List[str]

    gdb = dirname(dirname(rcl_fc))
    edit = Editor(gdb)
    edit.startEditing(False, False)

    with UpdateCursor(rcl_fc, fields) as cursor:
        left_changes = 0
        right_changes = 0
        for row in cursor:
            # Determine left-size parity
            left_before = row[0]
            if row[0] not in ("E", "O", "Z", "B") or overwrite == "true":
                try:
                    if row[2] == 0 and row[3] == 0:
                        row[0] = "Z"
                    elif parity_of(row[2]) == "EVEN" and parity_of(row[3]) == "EVEN":
                        row[0] = "E"
                    elif parity_of(row[2]) == "ODD" and parity_of(row[3]) == "ODD":
                        row[0] = "O"
                    else:
                        row[0] = "B"
                except TypeError:
                    userWarning("Road centerline with ID %s on left side generated an error due to a bad/null value." % row[6])
                    row[0] = None
                except:
                    e = sys.exc_info()[0]
                    userWarning("Road centerline with ID %s on left side generated the following error: %s" % (row[6], e))
                    row[0] = None
            if row[0] != left_before:
                left_changes += 1

            # Determine right-size parity
            right_before = row[1]
            if row[1] not in ("E", "O", "Z", "B") or overwrite == "true":
                try:
                    if row[4] == 0 and row[5] == 0:
                        row[1] = "Z"
                    elif parity_of(row[4]) == "EVEN" and parity_of(row[5]) == "EVEN":
                        row[1] = "E"
                    elif parity_of(row[4]) == "ODD" and parity_of(row[5]) == "ODD":
                        row[1] = "O"
                    else:
                        row[1] = "B"
                except TypeError:
                    userWarning("Road centerline with ID %s on right side generated an error due to a bad/null value." % row[6])
                    row[1] = None
                except:
                    e = sys.exc_info()[0]
                    userWarning("Road centerline with ID %s on right side generated the following error: %s" % (row[6], e))
                    row[1] = None
            if row[1] != right_before:
                right_changes += 1

            cursor.updateRow(row)

    edit.stopEditing(True)

    userMessage("%i left-side parities were changed, and %i right-side parities were changed." % (left_changes, right_changes))

def parity_of(integer):
    # type: (int) -> str
    """
    Determines whether an integer is even or odd.

    Parameters
    ----------
    integer : int
        Any integer.

    Returns
    -------
    str
        The string "EVEN" if the input is even or "ODD" if the input is odd.

    """
    return "EVEN" if integer % 2 == 0 else "ODD"

if __name__ == "__main__":
    main()