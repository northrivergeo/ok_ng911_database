#-------------------------------------------------------------------------------
# Name: ODOT_Validation_LocateESBGapsForTopology
# Purpose: Generate feature classes showing gaps in ESB coverage
#
# Author: Emma Baker (ebaker@odot.org), Riley Baird (rbaird@odot.org), Oklahoma DOT GIS
#
# Created: June 26, 2020
# Modified: June 29, 2020
#-------------------------------------------------------------------------------

from arcpy import GetParameterAsText, SymDiff_analysis, Exists, Delete_management
from os.path import basename, join
from NG911_GDB_Objects import getGDBObject
from NG911_arcpy_shortcuts import getFastCount
from NG911_User_Messages import userMessage

gdb = GetParameterAsText(0)

gdb_object = getGDBObject(gdb)
prov_fc = gdb_object.AuthoritativeBoundary
# ems_fc = gdb_object.EMS
# fire_fc = gdb_object.FIRE
# law_fc = gdb_object.LAW

for esb in gdb_object.esbList: # Law, Fire, EMS

    output_fc = join(gdb, "%s_Gap_%s" % (basename(prov_fc), basename(esb)))

    if Exists(output_fc):
        Delete_management(output_fc)

    SymDiff_analysis(prov_fc, esb, output_fc)
    userMessage("Difference between %s and %s represented as %i feature(s)." % (basename(prov_fc), basename(esb), getFastCount(output_fc)))