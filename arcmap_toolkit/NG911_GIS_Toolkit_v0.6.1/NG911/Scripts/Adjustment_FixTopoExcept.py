#-------------------------------------------------------------------------------
# Name:        Adjustment_FixTopoExcept.py
# Purpose:     Corrects the values in the TopoExcept field to the correct values; Updates the domain to the correct values.
#
# Author:      Baker, Baird (OK)
#
# Created:     March 2, 2021
# Modified:    March 2, 2021
# Copyright:   (c) Emma Marie Baker 2021, Riley Baird, 2021
#-------------------------------------------------------------------------------
## Imports
from arcpy import GetParameterAsText
from Okprep_createFC import create_feature_class
from os.path import join, dirname
from NG911_GDB_Objects import NG911_Session
from NG911_arcpy_shortcuts import DomainInfo
import arcpy
from arcpy.da import Editor, UpdateCursor
from NG911_User_Messages import *


def main():

    ## Get Parameters from ArcGIS Inputs and assign ArcGIS inputs to a list
    input_layer = GetParameterAsText(0)
    topo_field = GetParameterAsText(1)
    not_except = GetParameterAsText(2)
    dangles_except = GetParameterAsText(3)
    inside_except = GetParameterAsText(4)
    both_except = GetParameterAsText(5)
    check_null = GetParameterAsText(6)
    fix_domain = GetParameterAsText(7)
    fix_domain_value = GetParameterAsText(8)

    output_gdb = dirname(dirname(input_layer))

    edit = Editor(output_gdb)
    edit.startEditing(False, False)

    session = NG911_Session(output_gdb)
    domain_folder = session.domainsFolderPath
    file_name = "TOPOEXCEPT_Domains.txt"
    domain_file = join(domain_folder, file_name)

    topo_info = DomainInfo.get_from_domainfile(domain_file)

    userMessage("Correcting TopoExcept field values.")

    with UpdateCursor(input_layer, topo_field) as cursor:
        for row in cursor:
            if not_except not in ("", " ", None, "#") and row[0] == not_except:
                row[0] = "NO_EXCEPTION"
            elif dangles_except not in ("", " ", None, "#") and row[0] == dangles_except:
                row[0] = "DANGLE_EXCEPTION"
            elif inside_except not in ("", " ", None, "#") and row[0] == inside_except:
                row[0] = "INSIDE_EXCEPTION"
            elif both_except not in ("", " ", None, "#") and row[0] == both_except:
                row[0] = "BOTH_EXCEPTION"
            if check_null == "true" and row[0] in (None, "", " "):
                row[0] = "NO_EXCEPTION"

            cursor.updateRow(row)

    edit.stopEditing(True)

    if fix_domain == "true":
        userMessage("Fixing to Domain for TOPOEXCEPT in GDB.")
        gdb_domains = arcpy.da.ListDomains(output_gdb)
        for gdb_domain in gdb_domains:
            if gdb_domain.name == fix_domain_value:
                # UNASSIGN DOMAIN FROM FIELD
                arcpy.RemoveDomainFromField_management(input_layer, topo_field)
                # DELETE DOMAIN
                arcpy.DeleteDomain_management(output_gdb, fix_domain_value)
                # ADD CORRECT DOMAIN
                arcpy.CreateDomain_management(output_gdb, topo_info.domain_name, topo_info.domain_description, field_type = "TEXT")
                # Assign coded values to domain
                topo_dict = topo_info.domain_dict
                for code in topo_dict:
                    code_desc = unicode(topo_dict[code])
                    dom_name = unicode(topo_info.domain_name)
                    arcpy.AddCodedValueToDomain_management(output_gdb, dom_name, unicode(code), code_desc)
                # Assign domain to field in feature class
                arcpy.AssignDomainToField_management(input_layer, topo_field, topo_info.domain_name)

if __name__ == '__main__':
    main()
