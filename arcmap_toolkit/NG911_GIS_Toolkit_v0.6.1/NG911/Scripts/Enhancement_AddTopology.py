#-------------------------------------------------------------------------------
# Name:        Enhancement_AddTopology
# Purpose:     Makes sure that the NG911 topology has all current rules
#
# Author:      Kristen Jordan Koenig (KS), Emma Baker (OK), Riley Baird (OK)
#
# Created:     10/12/2018
# Modified:    July 6, 2021
# Copyright:   (c) kristen 2018
#-------------------------------------------------------------------------------
from arcpy import (AddRuleToTopology_management, ValidateTopology_management,
                AddFeatureClassToTopology_management, Exists, CreateTopology_management,
                GetParameterAsText, AddError, Describe, Delete_management)
from NG911_GDB_Objects import NG911_Session
from os.path import join, basename
import sys
from NG911_User_Messages import *


def main():
    gdb = GetParameterAsText(0)
    validate_topology = GetParameterAsText(1)

    session = NG911_Session(gdb)
    gdb_object = session.gdbObject
    if Exists(gdb_object.Topology):
        debugMessage("Will delete existing topology.")
        Delete_management(gdb_object.Topology)
    add_topology(gdb, validate_topology)

def add_topology(gdb, validate_topology):

    session = NG911_Session(gdb)
    gdb_object = session.gdbObject

    feature_dataset = gdb_object.NG911_FeatureDataset
    # topology = join(feature_dataset, topology_name)
    topology = gdb_object.Topology
    topology_name = basename(topology)

    # see if topology exists
    if len(sys.argv) == 4 and sys.argv[3] == "newTopoOnly" and Exists(topology):
        AddError("Topology already exists and argument to fail upon existing topology is true.")
        exit(1)

    if not Exists(topology):
        CreateTopology_management(feature_dataset, topology_name)
        userMessage("Created NG911 topology")

    # list feature classes already in the topology
    # check out http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-functions/topology-properties.htm
    topology_desc = Describe(topology)
    fc_topology = topology_desc.featureClassNames

    # userMessage(fc_topology)

    # Dissolve Provisioning Boundary to outer edge
    # userMessage("Creating Provisioning Boundary outer boundary per 'Display' field")
    # name1="Provisioning_Boundary"
    # provisioning = join(ds, name1)
    # name2="PROV_BTW"
    # prov_btw = join(ds, name2)
    # if not Exists(prov_btw):
    #     Dissolve_management(provisioning, prov_btw, "DISPLAY", "", "MULTI_PART", "DISSOLVE_LINES")

    # list of feature classes to be added to the topology
    fc_list= ["ROAD_CENTERLINE", "ADDRESS_POINT", "ESB", "ESB_LAW_BOUNDARY", "ESB_EMS_BOUNDARY", "ESB_FIRE_BOUNDARY", "DISCREPANCYAGENCY_BOUNDARY", "MUNICIPAL_BOUNDARY",
              "ESZ_BOUNDARY", "PSAP_BOUNDARY", "ESB_RESCUE_BOUNDARY", "ESB_FIREAUTOAID_BOUNDARY"]  # Changed to OK Fields
    # fc_list= ["Road_Centerline", "Address_Point", "ESB", "ESB_LAW_Boundary", "ESB_EMS_Boundary", "ESB_FIRE_Boundary", "Provisioning_Boundary", "Municipal_Boundary",
    #             "ESZ_Boundary", "PSAP_Boundary", "ESB_RESCUE_Boundary", "ESB_FIREAUTOAID_Boundary", "PROV_BTW"] # Changed to OK Fields

    esb_list = ["ESB_EMS_BOUNDARY", "ESB_FIRE_BOUNDARY", "ESB_LAW_BOUNDARY", "PSAP_BOUNDARY", "ESZ_BOUNDARY", "ESB_RESCUE_BOUNDARY", "ESB_FIREAUTOAID_BOUNDARY"] # Changed to OK Fields

    # add all feature classes that exist to the topology
    for fc in fc_list:
        fc_full = join(feature_dataset, fc)

        if Exists(fc_full):

            # if the feature class isn't in the topology, add it
            if fc not in fc_topology:
                present = False
                AddFeatureClassToTopology_management(topology, fc_full)
            else:
                present = True

            # if it's a polygon, add the no overlap rule
            if fc.upper() not in ["ROAD_CENTERLINE", "ADDRESS_POINT"]: # Changed to OK Fields
                AddRuleToTopology_management(topology, "Must Not Overlap (Area)", fc_full)

            # add no gaps rule to ESB and PSAP layers
            if ("ESB" in fc or "PSAP" in fc): # and present == False:
                AddRuleToTopology_management(topology, "Must Not Have Gaps (Area)", fc_full)

    userMessage("All feature classes present in or added to topology")


    # start adding rules based on layers that exist
    # start adding single-fc stuff

    # add road rules
    # road_rules = ["Must Not Overlap (Line)", "Must Not Intersect (Line)", "Must Not Have Dangles (Line)",
                    # "Must Not Self-Overlap (Line)", "Must Not Self-Intersect (Line)", "Must Be Single Part (Line)",
                    # "Must Not Intersect Or Touch Interior (Line)"]
    road_rules = ["Must Not Overlap (Line)",  "Must Not Have Dangles (Line)", "Must Not Self-Overlap (Line)",
                  "Must Not Self-Intersect (Line)", "Must Be Single Part (Line)"]  # Changed to OK Road Rules

    road_cl = join(feature_dataset, "ROAD_CENTERLINE") # Changed to OK Fields/Layers

    if Exists(road_cl):
        # add all individual road rules
        for road_rule in road_rules:
            AddRuleToTopology_management(topology, road_rule, road_cl)
        # for esb in esb_list:
        #     full_esb = join(feature_dataset, esb)
        #     if Exists(full_esb):
        #         AddRuleToTopology_management(topology, "Must Be Inside (Line-Area)", road_cl, "", full_esb)
    else:
        userWarning("Required feature class containing road centerlines not found.")

##        # make sure roads are inside all ESB & ESZ layers
##        for esb in esb_list:
##            esb_full = join(ds, esb)
##            if Exists(esb_full):
##                AddRuleToTopology_management(topology, "Must Be Inside (Line-Area)", road, "", esb_full)

    # make sure authoritative (provisioning) boundary covers everything
    auth_bnd = join(feature_dataset, "DISCREPANCYAGENCY_BOUNDARY") # Changed to OK Fields
    # auth_bnd = join(ds, "PROV_BTW") # Changed to OK Fields
    addr_pt = join(feature_dataset, "ADDRESS_POINT") # Changed to OK Fields

    if Exists(auth_bnd):
        # points
        if Exists(addr_pt):
            AddRuleToTopology_management(topology, "Must Be Properly Inside (Point-Area)", addr_pt, "", auth_bnd)
        else:
            userWarning("Required feature class containing address points not found.")

        # lines
        if Exists(road_cl):
            AddRuleToTopology_management(topology, "Must Be Inside (Line-Area)", road_cl, "", auth_bnd)
        else:
            userWarning("Required feature class containing road centerlines not found.")

        # polygons
        for esb in esb_list:
            full_esb = join(feature_dataset, esb)
            if Exists(full_esb):
                AddRuleToTopology_management(topology, "Must Cover Each Other (Area-Area)", full_esb, "", auth_bnd)

    # psap_bnd = join(feature_dataset, "PSAP_BOUNDARY")
    # if Exists(psap_bnd) and Exists(road_cl):
    #     AddRuleToTopology_management(topology, "Must Be Inside (Line-Area)", road_cl, "", psap_bnd)

    userMessage("All validation rules verified or added")

    if validate_topology == "true":
        userMessage("Validating topology...")
        ValidateTopology_management(topology)
        userMessage("Topology validated")

    return "Done"


if __name__ == '__main__':
    main()
