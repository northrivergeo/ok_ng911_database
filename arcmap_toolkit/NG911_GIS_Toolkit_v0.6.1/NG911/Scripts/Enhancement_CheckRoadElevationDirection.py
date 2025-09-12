#-------------------------------------------------------------------------------
# Name:        Enhancement_CheckRoadElevationDirection
# Purpose:     Looks at roads to see if the elevation/bridge attributes are assigned correctly
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     10/09/2015
# Modified:    January 6, 2022
#-------------------------------------------------------------------------------
#import modules
from arcpy import GetParameterAsText, FeatureClassToFeatureClass_conversion, AddField_management
from arcpy.da import SearchCursor, UpdateCursor

from NG911_arcpy_shortcuts import getFastCount, ListFieldNames
from NG911_DataCheck import RecordResults
from NG911_User_Messages import userMessage
from time import strftime
from NG911_GDB_Objects import getFCObject, getGDBObject

def main():
    gdb = GetParameterAsText(0)

    #set variables
    gdb_object = getGDBObject(gdb)
    rd_fc = gdb_object.RoadCenterline
    rd_obj = getFCObject(rd_fc)

    #userMessage
    userMessage("Comparing %s/%s of road centerlines..." % (rd_obj.ELEV_F, rd_obj.ELEV_T))

    #limit records to those with elevation flags
    qry = rd_obj.ELEV_F + " = 1 or " + rd_obj.ELEV_T + " = 1"

    #set up search cursor
    roadFullDict = {}
    fields = (rd_obj.UNIQUEID, rd_obj.FullName, rd_obj.ELEV_F, rd_obj.ELEV_T, rd_obj.Add_L_From, "SHAPE@")
    # rd_fc_temp = "rd_fc_temp"
    # FeatureClassToFeatureClass_conversion(rd_fc, "in_memory", rd_fc_temp)
    # if "concat_check" not in ListFieldNames(rd_fc_temp):
    #     AddField_management(rd_fc_temp, "concat_check", "TEXT", field_length=254)
    # with UpdateCursor(rd_fc_temp, ["concat_check", rd_obj.FullName, rd_obj.MSAGCO_L, rd_obj.MSAGCO_R])

    # max_count = getFastCount(rd_fc_temp)
    max_count = getFastCount(rd_fc)
    bad_segs = []  # (1st ID, ToLevel, 2nd ID, FromLevel)
    # bad_segs_to = {}
    # bad_segs_from = {}
    # with SearchCursor(rd_fc_temp, fields, sql_clause=(None, "ORDER BY FullName, Add_L_From")) as rows:
    with SearchCursor(rd_fc, fields, sql_clause=(None, "ORDER BY %s, %s" % (rd_obj.FullName, rd_obj.Add_L_From))) as rows:
        row_list = [row for row in rows]
        for i, row in enumerate(row_list):
            if i < max_count - 1:
                next_row = row_list[i + 1]
                # if this row and next row have same fullname
                # AND this row and next row ARE NOT disjoint
                row_geometry = row[5]
                next_row_geometry = next_row[5]
                if row[1] == next_row[1] and not row_geometry.disjoint(next_row_geometry):
                    # ...then they have the same name AND ARE adjacent
                    # concat_from_to = "%s%s%s%s" % (row[2], row[3], next_row[2], next_row[3])
                    if row[3] != next_row[2]:  # This segment's ToLevel != Next segment's FromLevel
                        bad_segs.append((row[0], row[3], next_row[0], next_row[2]))
                        # bad_segs.append((next_row[1], next_row[2]))
                        # bad_segs_to[row[1]] = row[3]
                        # bad_segs_from[next_row[1]] = next_row[2]


    # with SearchCursor(rd_fc, fields, qry) as rows:
    #     for row in rows:
    #         fullname = row[1]
    #
    #         #create a list from the segID and a string concatonation of the elev_f & elev_t
    #         f_t = [row[0], unicode(row[2]) + unicode(row[3])]
    #
    #         #KJK theory, get the lowest left address point to sort addresses based on range
    #         leftFrom = row[4]
    #
    #         #see if fullname is already a key in the dictionary
    #         if fullname not in roadFullDict:
    #
    #             #if it isn't, create new sub dictionary
    #             subDict = {leftFrom:f_t}
    #             roadFullDict[fullname] = subDict
    #
    #         #if it is in the dictionary already, add the new info
    #         else:
    #             subDict = roadFullDict[fullname]
    #             subDict[leftFrom] = f_t
    #
    # badSegs = []
    #
    # #loop through the road fullnames
    # for fullname in roadFullDict:
    #     elevInfo = roadFullDict[fullname]
    #
    #     segIDlist = []
    #     ftelevList = []
    #     stringsum = 0
    #
    #     #sort elevInfo based on the keys (keys are the left from address)
    #     for l_from in sorted(elevInfo):
    #
    #         ftList = elevInfo[l_from]
    #         segIDlist.append(ftList[0])
    #         ftelevList.append(ftList[1])
    #         #calculate the string sum (why? see below for notes)
    #         stringsum = stringsum + int(ftList[1][0]) + int(ftList[1][1])
    #
    #     #KJK theory, based on the number of segments, we can get info about what the concatonated elevation string should look like
    #     #for example, with two segments, the elevation string should look ideally like "0110", for three segments "011110", for four segments "01111110", etc.
    #     #each of those segments have a total sum of digits. Two segments = 2, three segments = 4, four segments = 6
    #     #basically the ideal count is 2 times the number of segments minus 2
    #     #if the real count doesn't match the ideal count, it's a trigger that something is wrong
    #     #for example for two segments: real segment = "0111", count = 3, doesn't match ideal count of 2, something is wrong
    #     #example for three segments: real segment = "011010", count = 3, doesn't match ideal count of 4, something is wrong
    #     count = len(segIDlist)
    #     idealStringSum = (2 * count) - 2
    #
    #     if count == 1:
    #         #get segID and report to table
    #         badSegs.append(segIDlist[0])
    #     else:
    #         #complete the check here to see if the real string sum doesn't match the ideal string sum
    #         if stringsum != idealStringSum:
    #             #create a full concatonated real string
    #             ftelev = "".join(ftelevList)
    #             length = len(ftelev)
    #             #flag if the first digit is wrong (should be 0)
    #             if ftelev[0] == "1":
    #                 badSegs.append(segIDlist[0])
    #
    #             #flag if the last digit is wrong (should be 0)
    #             if ftelev[-1] == "1":
    #                 badSegs.append(segIDlist[-1])
    #
    #             #here's the check to see about the inside 1's (not applicable to two segment comparisons)
    #             if length > 4:
    #                 #need to use multiple counter loops to later link the error location back to the original segment ID
    #                 looper = 2
    #                 index = 1
    #
    #                 while looper < length:
    #                     #compare digits in sets
    #                     if ftelev[looper:looper+2] != "11":
    #                         badSegs.append(segIDlist[index])
    #                     looper = looper + 2
    #                     index = index + 1

    #record issues if any exist
    values = []
    resultType = "fieldValues"
    today = strftime("%Y/%m/%d")
    fc = "ROAD_CENTERLINE" # Changed to OK Fields
    # report = rd_obj.ELEV_F + " and:or " + rd_obj.ELEV_T + " are not consistent with neighboring road segments"

    if len(bad_segs) > 0:
        for bad_seg_1_id, bad_seg_1_to_level, bad_seg_2_id, bad_seg_2_level in bad_segs:
            report = "Notice: Reported segment with ID %s with %s %s does not match adjacent segment with ID %s with %s %s." % (bad_seg_1_id, rd_obj.ELEV_T, bad_seg_1_to_level, bad_seg_2_id, rd_obj.ELEV_F, bad_seg_2_level)
            val = (today, report, fc, rd_obj.ELEV_F + " " + rd_obj.ELEV_T, bad_seg_1_id, "Check Road Elevation Direction")
            values.append(val)

    if values != []:
        RecordResults(resultType, values, gdb)
        userMessage("Check complete. " + str(len(bad_segs)) + " issues found. See table FieldValuesCheckResults for results.")
    else:
        userMessage("Check complete. Elevation indicators matched correctly.")


if __name__ == '__main__':
    main()
