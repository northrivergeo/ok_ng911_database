[**Oklahoma NG911 Toolkit**](../README.html) | [Adjustment](Adjustment.html) | [Comparison](Comparison.html) | [Enhancement](Enhancement.html) | [***MSAG***](MSAG.html) | [Okprep](Okprep.html) | [Submission](Submission.html) | [Validation](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [Topology Rules](Topology.html) | [Change Log](../ChangeLog.html) | [Error Glossary](ErrorGlossary.html)

# MSAG Toolset

## Toolset Credits
* Emma Baker, Oklahoma Department of Transportation
* Riley Baird, Oklahoma Department of Transportation
* Adapted from code originally by Kristen Jordan Koenig et al., Kansas Data Access and Support Center

##### Last Revised:
June 15, 2022

## Abstract
The *MSAG NG911 Comparison* tool compares a Master Street Address Guide (MSAG) Excel File with the NG911 Road Centerline address ranges. The *Telephone Number* tools compares a telephone number spreadsheet to the NG911 Road Centerline address ranges. All MSAG tools have a legacy option to use the legacy fields in the NG911 geodatabase if MSAG or TN spreadsheets are formatted with legacy format.

## Tools

### MSAG NG911 Comparison

Script: [MSAG_NG911comparison.py](../Scripts/MSAG_NG911comparison.py)

#### Tool Requirements
* MSAG as a spreadsheet with header columns including `High`, `Low`, `Dir`, `Street`, `Community`, and `ESN`.
* NG911 Geodatabase with standards-compliant Road Centerline feature class with the fields `Add_L_From`, `Add_L_To`, `Add_R_From`, `Add_R_To`, `MSAGComm_L`, `MSAGComm_R`, `ESN_L`, and `ESN_R`. Depending on if your MSAG spreadsheet uses Legacy or Next Generation format, the user will also need `LgcyPreDir`, `LgcyStreet`, `LgcyType`, `LgcySufDir` or `PreDir`, `Street`, `StreetType`, `SufDir`, respectively.

#### What the Tool Flags
* Segments in the MSAG that are not in the NG911 Road Centerline
* Segments in the NG911 Road Centerline that are not in the MSAG
* Any values or ranges in either the MSAG or NG911 Road Centerline that exist in one file but not the other.

#### Tool Tips
* The tool interface has two optional checkboxes available, one for “Recalculate Roads” and the other for “Recalculate MSAG”. If your roads or MSAG have processed correctly in past runs of the tool and you have NOT edited the roads or MSAG since the last run, you can uncheck the box. Unchecking the box will tell the tool to use the roads and/or MSAG that has already been processed and save quite a bit of time. If, however, you have edited the roads or MSAG since the last run, you will want to leave the appropriate box checked and have the tool recalculate the roads and/or MSAG. The user can select the Legacy format or the Next Generation format for certain fields for comparing the MSAG spreadsheet with the ROAD_CENTERLINE feature class.

#### Tool Output
* The tool creates a folder called *MSAG_analysis_NameOfGeodatabase* in the same folder where your NG911 geodatabase lives. Inside this folder is a geodatabase called *MSAG_analysis_NameOfGeodatabase.gdb*. All working layers and tables are saved in this geodatabase including a table version of your MSAG and a copy of your NG911 road centerline. These two copies will contain the analysis results after the tool runs.

#### Viewing the Results
* All results are recorded in a table called *MSAG_reporting*. This table’s `COMPARISON` field can be tied back to fields in other tables called `COMPARE`, `COMPARE_R` and `COMPARE_L`.
* All results are tied back to their original MSAG or Road Centerline record. To view MSAG results, open the table called *MSAG_YYYYMMDD* and look at the `REPORT` field. To view Road Centerline results, open the feature class called *Road_Centerline* inside the MSAG geodatabase and look at the `REPORT_R` and `REPORT_L` fields. The `REPORT_R` field addresses any issues with the right side of the road and `REPORT_L` addresses any issues with the left side of the road.
* Note on results: Range comparisons occur on entire road segments, and that’s how they are reported. As an example (all data made up), consider segment `1200AVE|HOPE|1112`. In the MSAG, this segment has a low of 100 and a high of 249. In the road centerline file, there are two segments, one with a low of 100 and a high of 149, and another with a low of 200 and a high of 299. In this circumstance, the MSAG segment will report that it does not have the range 250-299. In the road centerline, both segments will report that they are missing the range 150-199.

##### Table View Example

| Table          | Comparison	          | Low | High | Report                           |
| :------------: | :------------------: | :-: | :--: | :------------------------------: |
| MSAG_YYYYMMDD	 | 1200AVE\|HOPE\|1112  | 100 | 249  | Not in MSAG- Range: 250-299      |
| RoadCenterline | 1200AVE\|HOPE\|1112  | 100 | 149  | Not in NG911 road- Range 150-199 |
| RoadCenterline | 1200AVE\|HOPE\|1112	| 200 | 299  | Not in NG911 road- Range 150-199 |

#### Interpreting the results:
The term "segment" refers to the concatenation of the full street name, community and ESN such as `1200AVE|HOPE|1112`. All ranges for a given segment for both MSAG and road centerlines are compared with each other.

##### Message Meaning
* Exact MSAG match - All ranges between the MSAG and road centerline match for that segment
* Does not have an MSAG match - This segment does not appear in the MSAG file
* Does not have a road centerline match - This segment does not appear in the road centerline
* Issue with corresponding road centerline range	- This MSAG segment represents a larger range than the one in the road centerline. The corresponding road centerline segment(s) will have details regarding missing ranges.
* Issue with corresponding MSAG range	- This road centerline segment represents a larger range than the one in the MSAG file. The corresponding MSAG segment will have details regarding missing ranges.
* Not in NG911 road - Rng XX/Val XX	- This road centerline segment’s range does not match perfectly with the MSAG segment’s range. The ranges identified are the ranges missing in the road centerline.
* Not in MSAG - Rng XX/Val XX	- This MSAG segment’s range does not match perfectly with the road centerline segment’s range. The ranges identified are the ranges missing in the MSAG.

#### Editing the Data:
* All data in this analysis is a copy, and any edits to this data will have no effect on your real data. Any edits should be done in the master copies of the data. The copy of the road centerline data with the results will have consistent NGUIDs with the master version of the road centerline data. The MSAG does not have IDs, so you must manually determine which records need editing.

#### How it works:
* The criteria for comparison are a concatenation of the road pre-direction, name, street type, MSAG community and the ESN number. The comparison string looks similar to this: `1200AVE|HOPE|1112`. After the concatenation occurs for both the MSAG and Road Centerline segments, the tool compares if names exist in both places and identifies if one or the other file is missing a segment.
* After the general comparison, the tool compares the address ranges between similar MSAG and NG911 road centerline segments. For a complete comparison, all of a road segment’s ranges will be taken into consideration for a given comparison. The tool takes into account the possibility that NG911 road centerline segments can have differences between the right and left sides.

### Check AT&T TN List

Script: [MSAG_CheckTNList.py](../Scripts/MSAG_CheckTNList.py)

#### Tool Requirements
* NG911 geodatabase with Standards-compliant ADDRESS_POINT and ROAD_CENTERLINE feature classes.

* ADDRESS_POINT required fields include `Address`, `AddSuf`, `PreDir` or `LgcyPreDir`, `PreTypeSep`, `Street`/`LgcyStreet`, `StreetType`/`LgcyType`, `SufDir`/`LgcySufDir`, `SufMod`, `RCLMatch`, `RCLSide`, `MSAGComm`, `NGUID_ADD`, `SUBMIT`.

* ROAD_CENTERLINE required fields include `Add_L_From`, `Add_L_To`, `Add_R_From`, `Add_R_To`, `PreDir` or `LgcyPreDir`, `PreTypeSep`, `Street`/`LgcyStreet`, `StreetType`/`LgcyType`, `SufDir`/`LgcySufDir`, `SufMod`, `Parity_L`, `Parity_R`, `MSAGComm_L`, `MSAGComm_R`, `NGUID_RDCL`, `SUBMIT`.

* AT&T telephone number spreadsheet with the following columns ***in the indicated positions***: *House Number* (18), *House Number Suffix* (19), `PreDir`/`LgcyPreDir` (21), `Street`/`LgcyStreet` (22), *Community*/`MSAGComm` (23), `State` (25), *NPA* (3), *NXX* (4), *Phone Line* (5), *Service Class* (8).

This tool is for PSAPs who have AT&T as their provider. The tool geocodes a list of telephone number addresses against the MSAG information in the NG911 Address Points and Road Centerlines. This tool requires a TN (telephone number) list. Please see detailed tool instructions below for information on the geocoding results.

#### Using the Tool
This tool requires a telephone number list to be extracted as a spreadsheet from AT&T.

* In the “TN Spreadsheet” input box, select the TN Spreadsheet provided by the telephone company.
* In the “NG911 Geodatabase” box, select the appropriate NG911 geodatabase.
* Select Use Legacy Fields option if appropriate.
* Run the tool.

#### Understanding the Results
The results will be contained in a folder that sits next to your NG911 geodatabase. The name of the folder will be your NG911 geodatabase name with “\_TN” appended to the end. If your geodatabase name is “Oklahoma_NG911.gdb”, the folder will be named “Oklahoma_NG911_TN”. Inside this folder will be a geodatabase called “TN_Working.gdb”. In this geodatabase, you will find two tables and a feature class with the day’s date appended to the end.

Your TN list spreadsheet is copied in the geodatabase as TN_List_YYYYMMDD with one column added called `NGTNID` for a unique ID. If you had columns for NPA, NXX and PHONELINE, the unique ID is a concatenation of these columns to form the phone number. If the ID is the phone number, this ID is persistent throughout all of your MSAG reviewing and editing. If the ID is not a phone number, then the ID has been randomly generated and is persistent for this single geocoding session.

All results from the geocoding operation will be found in TN_List_YYYYMMDD. This table can be brought into ArcMap and viewed as a normal point file. The geocoding status for each record can be found in the “MATCH” column. `M` = Matched, `T` = Tied, `U` = Unmatched.

### Check Other TN List

Script: [MSAG_GeocodeTNList_Prepped.py](../Scripts/MSAG_GeocodeTNList_Prepped.py)

This tool is intended for PSAPs who do not have AT&T as their provider. This tool geocodes full addresses housed in a spreadsheet against MSAG information in an NG911 geodatabase.

#### Tool Requirements
* NG911 geodatabase ADDRESS_POINT and ROAD_CENTERLINE feature classes.

* ADDRESS_POINT required fields include `Address`, `AddSuf`, `PreDir` or `LgcyPreDir`, `PreTypeSep`, `Street`/`LgcyStreet`, `StreetType`/`LgcyType`, `SufDir`/`LgcySufDir`, `SufMod`, `RCLMatch`, `RCLSide`, `MSAGComm`, `NGUID_ADD`, `SUBMIT`.

* ROAD_CENTERLINE required fields include `Add_L_From`, `Add_L_To`, `Add_R_From`, `Add_R_To`, `PreDir` or `LgcyPreDir`, `PreTypeSep`, `Street`/`LgcyStreet`, `StreetType`/`LgcyType`, `SufDir`/`LgcySufDir`, `SufMod`, `Parity_L`, `Parity_R`, `MSAGComm_L`, `MSAGComm_R`, `NGUID_RDCL`, `SUBMIT`.

* Telephone number spreadsheet with the following columns: *House Number*, *House Number Suffix* (optional), `PreDir`/`LgcyPreDir` (optional), `Street`/`LgcyStreet`, `StreetType`/`LgcyType` (optional), `SufDir`/`LgcySufDir` (optional), *Community*/`MSAGComm`, *Telephone Number* (optional).

#### Using the Tool
* In the “NG911 Geodatabase” box, select the appropriate NG911 geodatabase.
* In “Excel Spreadsheet”, select your TN extract spreadsheet.
* For the various fields outlined in the tool, fill in all fields that are in your spreadsheet. The more fields you can fill in, the more accurate the results will be. Several fields are required like House Number, Road Name, and Community.
* Select Use Legacy Fields option if appropriate.
* Run the tool.

#### Understanding the Results
The results will be contained in a folder that sits next to your NG911 geodatabase. The name of the folder will be your NG911 geodatabase name with “\_TN” appended to the end. If your geodatabase name is “Oklahoma_NG911.gdb”, the folder will be named “Oklahoma_NG911_TN”. Inside this folder will be a geodatabase called “TN_Working.gdb”. In this geodatabase, you will find two tables and a feature class with the day’s date appended to the end.

Your TN list spreadsheet is copied in the geodatabase as TN_List_YYYYMMDD with one column added called `NGTNID` for a unique ID. If you defined a Phone Number field when running the tool, the phone number is the unique ID. If the ID is the phone number, this ID is persistent throughout all of your MSAG reviewing and editing. If the ID is not a phone number, then the ID has been randomly generated and is persistent for this single geocoding session.

All results from the geocoding operation will be found in TN_List_YYYYMMDD. This table can be brought into ArcMap. The geocoding status for each record can be found in the “MATCH” column. M = Matched, T = Tied, U = Unmatched.

## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
