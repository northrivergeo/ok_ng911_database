#-------------------------------------------------------------------------------
# Name:        Adjustment_FishboneAnalysis.py
# Purpose:
#
# Author:      Baker (OK), Baird (OK)
#
# Created:     September 30, 2020
# Modified:    January 6, 2022
# Copyright:   (c) Emma Marie Baker 2020, Riley Baird, 2020
#-------------------------------------------------------------------------------

from arcpy import (XYToLine_management, CreateAddressLocator_geocoding, GeocodeAddresses_geocoding, GetParameterAsText,
                   MakeFeatureLayer_management, FeatureClassToFeatureClass_conversion, Intersect_analysis, AddField_management,
                   CalculateField_management, DeleteField_management, Project_management, AddGeometryAttributes_management, SetProgressor,
                   SetProgressorPosition, ResetProgressor, SetProgressorLabel)
import arcpy.da
from NG911_User_Messages import *
from NG911_GDB_Objects import NG911_Session, getFCObject, NG911_Address_Object, NG911_RoadCenterline_Object
from NG911_arcpy_shortcuts import getFastCount, deleteExisting
from os.path import dirname, join, basename

try:
    import typing
except:
    pass

def main():
    gdb = GetParameterAsText(0)
    locator_folder = GetParameterAsText(1)
    intersect_check = GetParameterAsText(2)
    locator_file = join(locator_folder, "Locator")

    session = NG911_Session(gdb)
    gdb_object = session.gdbObject
    ap_path = gdb_object.AddressPoints
    address_points = getFCObject(ap_path)  # type: NG911_Address_Object
    rcl_path = gdb_object.RoadCenterline  # path to ROAD_CENTERLINE
    road_centerlines = getFCObject(rcl_path)  # type: NG911_RoadCenterline_Object

    ######################################
    ##### CREATE THE ADDRESS LOCATOR #####
    ######################################
    fish_len = 8
    SetProgressor("step", "Beginning Fishbone Analysis...", 0, fish_len, 1)
    userMessage("Creating address locator from %s..." % basename(rcl_path))

    locator_style = "US Address - Dual Ranges"

    rcl_path_argument = "'%s' 'Primary Table'" % rcl_path
    # debugMessage(rcl_path_argument)

    rcl_fields = [
        road_centerlines.UNIQUEID,
        road_centerlines.Add_L_From,
        road_centerlines.Add_L_To,
        road_centerlines.Add_R_From,
        road_centerlines.Add_R_To,
        road_centerlines.PARITY_L,
        road_centerlines.PARITY_R,
        road_centerlines.FullName,
        road_centerlines.PreDir,
        road_centerlines.PreType,
        road_centerlines.Street,
        road_centerlines.StreetType,
        road_centerlines.SufDir,
        road_centerlines.MUNI_L,
        road_centerlines.MUNI_R,
        road_centerlines.COUNTY_L,
        road_centerlines.COUNTY_R,
        road_centerlines.STATE_L,
        road_centerlines.STATE_R,
        "''",
        "''",
        road_centerlines.ZIP_L,
        road_centerlines.ZIP_R
    ]

    target_fields = ['Feature ID', '*From Left', '*To Left', '*From Right', '*To Right', 'Left Parity', 'Right Parity',
                     'Full Street Name', 'Prefix Direction', 'Prefix Type', '*Street Name', 'Suffix Type',
                     'Suffix Direction', 'Left City or Place', 'Right City or Place', 'Left County', 'Right County',
                     'Left State', 'Right State', 'Left State Abbreviation', 'Right State Abbreviation',
                     'Left ZIP Code', 'Right ZIP Code']

    field_strings = []
    for rcl_field, target_field in zip(rcl_fields, target_fields):
        current_string = "'%s' %s VISIBLE NONE" % (target_field, rcl_field)
        field_strings.append(current_string)
    field_map_string = ";".join(field_strings)
    # debugMessage(field_map_string)
    deleteExisting(locator_file)

    SetProgressorPosition()
    SetProgressorLabel("Creating Address Locator...")
    CreateAddressLocator_geocoding(locator_style, rcl_path_argument, field_map_string, locator_file, config_keyword="", enable_suggestions="DISABLED")
    SetProgressorPosition()
    #################################
    ##### GEOCODE THE ADDRESSES #####
    #################################

    userMessage("Geocoding %s..." % basename(ap_path))
    SetProgressorLabel("Preparing for Address Geocoding...")

    deleteExisting("ap_query_layer")
    MakeFeatureLayer_management(ap_path, "ap_query_layer", "Longitude NOT IN (0, NULL) AND Latitude NOT IN (0, NULL)")  # Filter out APs with bad lat/lon
    ap_count = getFastCount(ap_path)
    ap_query_layer_count = getFastCount("ap_query_layer")
    ap_removed_count = ap_count - ap_query_layer_count
    if ap_removed_count == 0:
        userMessage("Geocoding all address points.")
    else:
        userWarning("Removed %i address points with Longitude and Latitude 0 or null." % ap_removed_count)

    ap_query_dir = dirname(locator_file)
    ap_query_fc_name = "Address_Points_With_LatLon.shp"
    ap_query_path = join(ap_query_dir, ap_query_fc_name)
    deleteExisting(ap_query_path)
    FeatureClassToFeatureClass_conversion("ap_query_layer", ap_query_dir, ap_query_fc_name)

    field_map_string = "'Street or Intersection' %s VISIBLE NONE;'City or Placename' %s VISIBLE NONE;State %s VISIBLE NONE;'ZIP Code' %s VISIBLE NONE" % (address_points.FullAddr, address_points.MUNI, address_points.STATE, address_points.ZIP)
    output_path = join(dirname(locator_file), "Geocode_Results.shp")
    debugMessage(output_path)
    deleteExisting(output_path)

    SetProgressorPosition()
    SetProgressorLabel("Geocoding Addresses...")
    GeocodeAddresses_geocoding(ap_query_path, locator_file, field_map_string, output_path, "STATIC")  # TODO: (11-Feb-2021) See if "STATIC" causes a licensing issue
    SetProgressorPosition()
    #####################################
    ##### CREATE THE FISHBONE LINES #####
    #####################################

    userMessage("Generating fishbone analysis line features...")
    SetProgressorLabel("Preparing for Fishbone Analysis...")

    fish_path = join(dirname(locator_file), "Fishbone_Results.shp")
    deleteExisting(fish_path)
    debugMessage(fish_path)

    MakeFeatureLayer_management(output_path, "geocode_nonzero_layer", "X NOT IN (0, NULL) AND Y NOT IN (0, NULL)")
    geo_count = getFastCount(output_path)
    geo_query_layer_count = getFastCount("geocode_nonzero_layer")
    geo_removed_count = geo_count - geo_query_layer_count
    if geo_removed_count == 0:
        userMessage("All geocoded address points to be included in fishbone analysis.")
    else:
        userWarning("Removed %i geocoded address points from fishbone analysis with X and Y 0 or null." % geo_removed_count)

    deleteExisting(join(dirname(locator_file), "Matched_Geocode_Results.shp"))

    SetProgressorPosition()
    SetProgressorLabel("Creating Fishbone lines and projecting...")
    XYToLine_management("geocode_nonzero_layer", fish_path, "X", "Y", "Longitude", "Latitude")  # Creates fishbone line feature class
    FeatureClassToFeatureClass_conversion("geocode_nonzero_layer", dirname(locator_file), "Matched_Geocode_Results.shp")  # Creates point feature class from matched geocoded address points

    # Project Fishbone_Results.shp and calculate geometry
    fish_proj_path = join(dirname(locator_file), "Fishbone_Results_Projected.shp")
    Project_management(fish_path, fish_proj_path, arcpy.SpatialReference(2267)) # projection: Oklahoma North
    AddGeometryAttributes_management(fish_proj_path, "LENGTH", "FEET_US")
    SetProgressorPosition()

    #####################################
    ##### INTERSECTION OF FISHBONES #####
    #####################################

    if intersect_check == "true":
        userMessage("Searching for intersections...")
        SetProgressorLabel("Preparing for Fishbone intersection creation...")

        fishbone_intersect_path = join(locator_folder, "Fishbone_Intersect.shp")
        deleteExisting(fishbone_intersect_path)
        Intersect_analysis(in_features="'%s' #" % fish_proj_path, out_feature_class=fishbone_intersect_path, join_attributes="ALL", output_type="POINT")

        SetProgressor("step", "Creating and counting Fishbone intersections...", 0, fish_len, 1)
        SetProgressorPosition(fish_len-2)

        AddField_management(fishbone_intersect_path, "X_INTER", "DOUBLE")
        AddField_management(fishbone_intersect_path, "Y_INTER", "DOUBLE")

        with arcpy.da.UpdateCursor(fishbone_intersect_path, ["SHAPE@XY", "X_INTER", "Y_INTER"]) as cursor:
            for row in cursor:
                row[1] = row[0][0]  # X_INTER = x-coord
                row[2] = row[0][1]  # Y_INTER = y-coord
                cursor.updateRow(row)

        # SetProgressorLabel("Creating and counting Fishbone intersections...")

        intersect_count_path = join(locator_folder, "Fishbone_Intersect_Count.shp")
        deleteExisting(intersect_count_path)
        arcpy.Dissolve_management(in_features=fishbone_intersect_path, out_feature_class=intersect_count_path,
                                  dissolve_field="X_INTER;Y_INTER", statistics_fields="FID_Fishbo COUNT;LENGTH MEAN;LENGTH MIN;LENGTH MAX",
                                  multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
        AddField_management(intersect_count_path, "FISH_COUNT", "LONG")
        CalculateField_management(in_table=intersect_count_path, field="FISH_COUNT", expression="[COUNT_FID_]", expression_type="VB", code_block="")  # Field COUNT_FID_ is trimmed from COUNT_FID_Fishbo
        DeleteField_management(in_table=intersect_count_path, drop_field="COUNT_FID_")

        number_of_intersection_locations = getFastCount(intersect_count_path)
        if number_of_intersection_locations > 0:
            userMessage("Fishbone lines intersect at %i locations." % number_of_intersection_locations)
        else:
            userMessage("No fishbone lines intersect.")
        SetProgressorPosition()
    else:
        SetProgressorPosition()
        SetProgressorPosition()
        pass

    ResetProgressor()

if __name__ == "__main__":
    main()