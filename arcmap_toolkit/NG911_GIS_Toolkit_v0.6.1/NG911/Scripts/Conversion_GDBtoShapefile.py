#-------------------------------------------------------------------------------
# Name:        Conversion_GDBtoShapefile
# Purpose:     Converts all geodatabase tables and feature classes to dbf's and shapefiles
#
# Author:      kristen (KS), Baker (OK)
#
# Created:     09/02/2015
# Modified:    January 15, 2020
#-------------------------------------------------------------------------------

from arcpy import GetParameterAsText, ListFeatureClasses, CopyFeatures_management, CopyRows_management, env
from os.path import join, isdir
from os import mkdir
from NG911_User_Messages import *

def main():

    #get variables
    gdb = GetParameterAsText(0)
    outputFolder = GetParameterAsText(1)

    #set workspace
    env.workspace = join(gdb, "NG911")

    if not isdir(outputFolder):
        mkdir(outputFolder)

    #list all feature classes
    fcs = ListFeatureClasses()

    #loop through feature classes
    for fc in fcs:
        #create output name
        outFC = join(outputFolder, fc + ".shp")
        #copy features
        CopyFeatures_management(fc, outFC)
        userMessage("Successfully exported %s feature class to shapefile." % fc)

    #set variabes for road alias table
    # roadAliasTable = join(gdb, "Road_Alias")
    # outRoadAliasTable = join(outputFolder, "Road_Alias.dbf")
    # try:
    #     #copy road alias table
    #     CopyRows_management(roadAliasTable, outRoadAliasTable)
    #     userMessage("Exported %s as %s." % (roadAliasTable, outRoadAliasTable))
    # except:
    #     userMessage("No RoadAlias table found to export.")
    #     pass

if __name__ == '__main__':
    main()
