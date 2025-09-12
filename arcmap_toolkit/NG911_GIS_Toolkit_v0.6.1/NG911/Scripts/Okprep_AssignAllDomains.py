"""
Contains assign_all_domains
"""

import arcpy
import os
from NG911_User_Messages import *
from NG911_arcpy_shortcuts import deleteExisting

def assign_all_domains(domain_dir, target_gdb):
    # # # # # CONFIG # # # # #
    # domain_dir = r"G:\ArcGIS\Project Files\NG911\NG911_Git\NG911\Domains"
    # domain_gdb = r"C:\Users\344053\Desktop\NG911_Faster_Domains_Test\Test.gdb"
    domain_gdb = "in_memory"
    # target_gdb = r"C:\Users\344053\Desktop\NG911_Faster_Domains_Test\Test.gdb"


    # # # # # CONSTRUCT DOMAIN TABLES # # # # #

    os.chdir(domain_dir)
    arcpy.env.workspace = domain_dir
    domain_files = arcpy.ListFiles("*")

    table_names = []
    domain_descriptions = {}  # e.g. { "AGENCYID": "ID Assigned to each Agency by the State of Oklahoma 911 Coordinator" }
    end_of_script_warnings = []

    for f in domain_files:
        table_name = f[:f.index("_")]
        table_names.append(table_name)
        try:
            table_path = os.path.join(domain_gdb, table_name)
            deleteExisting(table_path)
            arcpy.CreateTable_management(domain_gdb, table_name)
            with open(f, "r") as rows:
                left_column_name, right_column_name = rows.readline().strip('\n').split("|")
                domain_descriptions[table_name] = right_column_name
                arcpy.AddField_management(table_path, "Code", "TEXT", field_alias=left_column_name)
                arcpy.AddField_management(table_path, "Description", "TEXT", field_alias=right_column_name)
                key_list = []
                with arcpy.da.InsertCursor(table_path, ["Code", "Description"]) as cursor:
                    for row in rows:
                        row_tuple = tuple(row.strip('\n').split("|"))
                        if row_tuple[0] in key_list:
                            end_of_script_warnings.append("==================================================================\nDUPLICATE CODE DETECTED!\nDomain: %s\nCode: %s\nThe duplicate will be skipped.\nPLEASE REPORT THIS MESSAGE TO ebaker@odot.org AND rbaird@odot.org!\n==================================================================" % (table_name, row_tuple[0]))
                        else:
                            key_list.append(row_tuple[0])
                            cursor.insertRow(row_tuple)
            debugMessage("Created and populated table %s." % table_name)
        except Exception as e:
            userWarning("Error when creating or populating table %s." % table_name)

    userMessage("Done creating temporary domain tables!")


    # # # # # ASSIGN DOMAINS TO GEODATABASE # # # # #

    arcpy.env.workspace = domain_gdb
    for t in table_names:
        try:
            arcpy.DeleteDomain_management(target_gdb, t)
            debugMessage("Deleted existing %s domain." % t)
        except:
            pass
        try:
            arcpy.TableToDomain_management(t, "Code", "Description", target_gdb, t, domain_descriptions[t])
            debugMessage("Assigned domain %s to geodatabase." % t)
        except Exception as e:
            userWarning("Failed to assign domain %s to geodatabase." % t)

    userMessage("Done assigning domains to geodatabase!")



    # # # # # CLEANUP # # # # #

    for t in table_names:
        if arcpy.Exists(os.path.join(domain_gdb, t)):
            arcpy.Delete_management(os.path.join(domain_gdb, t))

    print("Cleared temporary tables!")

    for message in end_of_script_warnings:
        userWarning(message)

    # print("Complete!")
