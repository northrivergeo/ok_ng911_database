[**Oklahoma NG911 Toolkit**](../README.html) | [Adjustment](Adjustment.html) | [Comparison](Comparison.html) | [Enhancement](Enhancement.html) | [MSAG](MSAG.html) | [Okprep](Okprep.html) | [Submission](Submission.html) | [***Validation***](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [Topology Rules](Topology.html) | [Change Log](../ChangeLog.html) | [Error Glossary](ErrorGlossary.html)

# Validation Toolset

## Toolset Credits
* Emma Baker, Oklahoma Department of Transportation
* Riley Baird, Oklahoma Department of Transportation
* Adapted from code originally by Kristen Jordan Koenig et al., Kansas Data Access and Support Center

##### Last Revised:
June 15, 2022

## Abstract
The data validation tools perform a variety of basic verification checks against the NG911 Data Model template to determine if the data is ready for submission. The scripts are organized to validate data by specific layers or groups of layers, and multiple optional tests are included for each set. Any issues found with the data will be reported in tables added to the geodatabase as an "Error" or a "Notice". Notices will not prevent submission.

The scripts can be run multiple times as necessary so users can correct basic issues prior to submitting their NG911 updates. Currently, these data validation tools do not provide complete quality assurance (QA) of the data.

Be advised that most of these checks do not *correct* any errors, only *make note* of them.

[Methodology](#expanded-validation-check-methodology) is expanded below for the following validation checks: **Check Feature Locations**, **Check Topology**, **Check RCLMatch**, **Check Frequency**, **Check ESN and Muni Attributes**, and **Find Overlaps**.

## Tools

A total of nine tools exist in the Validation Toolset. The individual tools and their available checks are described below. Nested bullet points indicate checks that are automatically run when the option at the top-level bullet point is selected.

### 1 Check Template
* **Check Layer List:** Checks for required layers. Missing required layers are reported in the *TemplateCheckResults* table. This also checks for a feature dataset named `NG911` and checks that it uses the correct spatial reference.
* **Check Required Fields:** Checks feature classes to ensure that they contain the required fields.
*	**Check Required Field Values:** Returns errors if required fields contain null values.
*	**Check Submission Counts:** Checks to see how many features are marked for submission.
*	**Find Invalid Geometry:** Returns errors if points, lines, or polygons have fewer than 1, 2, or 3 points, respectively.
*	**Check GDB Domains:** Returns errors if geodatabase Domains don't match the Oklahoma standards.

### 2 Check Address Points
*	**Check Values Against Domains:**
 	* Ensures that fields with domains contain values that match the domain.
  *	**Check MSAGComm Spaces:** Checks for and removes leading or trailing spaces in `MSAGComm` fields.
  * **Check `RCLMatch`:** (if it exists) Validates the `RCLMatch` field of the ADDRESS_POINT feature class against the ROAD_CENTERLINE feature class.
*	**Check Feature Locations:** Compares features in a feature class to the discrepancy agency boundary to ensure that they lie within a boundary.
*	**Check Address Point Frequency:** Checks for identical address records and returns errors if any are found.
*	**Check Unique ID:** Ensures that no address records share unique IDs and unique IDs are formatted properly.
  *	**Format:** Ensures that are unique IDs for address records are formatted properly. Example: `LAYERNAME_{ABC-123}@AGENCYID`
  *	**Frequency:** Ensures that no address records share unique IDs.
*	**Check ESN and Muni Attributes:** Selects address points using ESN or muni polygons to check `ESN` and `City` attributes match those of the polygons.

### 3 Check Roads
*	**Check Values Against Domains:**
  * Ensures that fields with domains contain values that match the domain.
  *	**Check MSAGComm Spaces:** Checks for and removes leading or trailing spaces in `MSAGComm` fields.
  * **Check Parities:** Returns a notice if address ranges do not match parity fields
*	**Check Feature Locations:** Compares features in a feature class to the discrepancy agency boundary to ensure that they lie within a boundary.
*	**Check Unique ID:** Ensures that no road centerline records share unique IDs and unique IDs are formatted properly.
  *	**Format:** Ensures that are unique IDs for road centerline records are formatted properly. Example: `LAYERNAME_{ABC-123}@AGENCYID`
  *	**Frequency:** Ensures that no road centerline records share unique IDs.
*	**Check for Cutbacks:** Returns a notice if a road centerline feature contains angle on the open interval (0, 55) degrees, which could potentially indicate a cutback.
*	**Check Directionality:**
  * Ensures that address ranges run from low to high numbers.
*	**Check Overlapping Address Ranges:** Checks for numerical overlaps in address ranges between road centerline features.

### 4 Check Boundaries
*	**Check Values Against Domains:** Ensures that fields with domains contain values that match the domain.
*	**Check Feature Locations:** Compares features in a feature class to the discrepancy agency boundary to ensure that they lie within a boundary.
*	**Check Unique ID:** Ensures that no boundary records share unique IDs and unique IDs are formatted properly.
  *	**Format:** Ensures that are unique IDs for boundary records are formatted properly. Example: `LAYERNAME_{ABC-123}@AGENCYID`
  *	**Frequency:** Ensures that no boundary records share unique IDs.

### 5 Check Additional Layers
*	**Check Values Against Domains:** Ensures that fields with domains contain values that match the domain.
*	**Check Feature Locations:** Compares features in a feature class to the discrepancy agency boundary to ensure that they lie within a boundary.
*	**Check Unique ID:** Ensures that no other records share unique IDs and unique IDs are formatted properly.
  *	**Format:** Ensures that are unique IDs for other records are formatted properly. Example: `LAYERNAME_{ABC-123}@AGENCYID`
  *	**Frequency:** Ensures that no other records share unique IDs.

### 6 Clear Results Table (Optional)
*	**Clear Template Results:** Deletes all records in table *TemplateCheckResults*.
*	**Clear Field Value Results:** Deletes all records in table *FieldValuesCheckResults*.

### 7 Verify Topology Exceptions (Optional)
*	Double-checks that all road centerline topology error are recorded as exceptions in the data and the topology.

### 7.1 ESB Gap Locations (Optional)
*	Performs a Symmetrical Difference to find gaps between the ESB layers and the Discrepancy Agency Boundary layer. Requires an advanced license. Required layers include ESB_LAW_BOUNDARY, ESB_FIRE_BOUNDARY, ESB_EMS_BOUNDARY, and DISCREPANCYAGENCY_BOUNDARY.

### 8 Check All Required
*	**Template Checks**
  * Deletes existing result tables
  * Check Spatial Reference
  * Check Layer List
  * Check GDB Domains
  * Check Required Fields
  * Check Required Field Values
  * Check Submission Numbers
  * Find Invalid Geometry
*	**Common Layers Checks**
  * Check Values Against Domain
  * Check Feature Locations
  * Check Topology - [Topology Rules](Topology.html)
  * Check Unique ID - Format and Frequency
*	**Address Point Layer Checks**
  * Check MSAGComm Spaces
  * Check RCLMatch
  * Check Frequency
  * Check ESN and Muni Attribute
*	**Road Centerline Layer Checks**
  * Check MSAGComm Spaces
  * Check Frequency
  * Check Cutbacks
  * Check Directionality
  * Check Frequency (of dual carriageways)
  * Find Overlaps
  * Check Parities


## Expanded Validation Check Methodology

### Check Feature Locations
* Function begins by establishing the outer boundary that will contain the features from the feature classes. For this function, the existence of the *COUNTY_BOUNDARY* feature class will supersede the *DISCREPANCYAGENCY_BOUNDARY* as the outer boundary. First, the function checks for the *DISCREPANCYAGENCY_BOUNDARY*. If the *COUNTY_BOUNDARY* does not exist, then the function will check for the `STATE` field within the *DISCREPANCYAGENCY_BOUNDARY* feature class. If the field does not exist, the field will be created and calculated as "OK". A feature layer is then created out of the resulting *DISCREPANCYAGENCY_BOUNDARY* feature class and dissolved in memory using the `STATE` field.

* Once the outer boundary has been established, the function will then loop through the available feature classes to query them by making feature layers. The query is `SUBMIT = 'Y'` for all feature classes. The *ROAD_CENTERLINE* feature class has an additional query to exclude features with topology exceptions. The *ADDRESS_POINT* feature class utilizes the selection method "COMPLETELY_WITHIN", while all other feature classes utilize the selection method "WITHIN". Once the feature classes have been queried, a SelectLayerByLocation ({selection method}) and a SelectLayerByAttribute ("SWITCH_SELECTION") are applied to the feature class with respect to the outer boundary to select all objects outside the outer boundary. If the count for the selection is greater than zero, an error is reported for those objects that are selected that have non-null unique IDs.


### Check Topology
* First, the function checks for and deletes pre-existing Topology and Topology error feature classes (i.e., errors that produce Points, Lines, and Polygons). The function then recreates the Topology and exports the errors to feature classes within the GDB.

* Next, the function loops through the Topology error feature classes. A feature layer is then created from the current error feature class (polygon, line, or point) to query to where `isException = 0`. If an error is returned (i.e., the fast count of the feature layer is greater than zero), the function searches through the feature layer with the error fields. The function assigns the appropriate parameters to default script parameters. General, most topology rules use only the Origin or Destination (i.e., there is only one feature class associated with the error type). The standard parameter setup includes:
  * `origin_fc` and `destination_fc` (feature class name describing a given Origin or Destination), `origin_id` and `destination_id` (`OBJECTID` for the object associated with the error within the feature class), `origin_id_field_name` and `destination_id_field_name` (error feature class origin and destination `OBJECTID` field name), and `ruleDesc` (description of the topology rule to error originated from).

* The function then checks to see if we have already looked at a given (`rule`, `origin_fc`, `destination_fc`). If not, then the tuple is added to the already_checked list.

* Next, the function then checks to make sure `origin_fc` and `destination_fc` are not None or an empty string or a blank space.
  * If both fc fields exist:
    * First, the function then creates a feature layer from current error feature layer with the query of `RuleDescription = '{current rule}'`. Then, the function creates table views from the `origin_fc` and `destination_fc` that will have the `OBJECTID` calculated to a `RecordID` field for the purposes of joining both feature classes to the error feature layer. The function then adds the two joins to the error feature layer. A query is then concatenated and field list created to accumulate a list of (`rule`, `origin_fc`, `origin_unique_id`, `destination_fc`, `destination_unique_id`).
  * If only one fc field exists:
    * First, the function then creates a feature layer from current error feature layer with the query of `RuleDescription = '{current rule}'`. Then, the function creates table views from the `fc`. The function then joins the FL to the error feature layer. A query is then concatenated and field list created to accumulate a list of (`rule`, `fc`, `unique_id`, "", "").

* The function then looks at the accumulated list of tuples returned from all error feature layers to count and concatenate the appropriate error messages to pass to the *RecordResults* function.


### Check RCLMatch
* First, it should be noted that the `MSAGComm` fields are used for the `RCLMatch` comparison between *ADDRESS_POINT* and *ROAD_CENTERLINE* feature classes. The function for the check first creates the list of fields that will be used for the `RCLMatch` comparison including the `NAME_COMPARE` field. These are the same fields used in the `FullName`/`FullAddr` concatenation, so there shouldn't be any issues.

* A table view is created out of the *ROAD_CENTERLINE* feature class to query down to `SUBMIT = 'Y'` and then a *rcTable* table is created from the table view to be used in the `prep_roads_for_comparison` function. `Prep_roads_for_comparison` is then run for the *rcTable* table with the appropriately specified parameters. The process is then repeated for the *ADDRESS_POINT* feature class with a query of `SUBMIT = 'Y' AND RCLMatch <> 'NO_MATCH'` and a table named *apTable*.

* `Error: RCLSide is null`: The analysis begins with the selection of objects in the *apTable* where `RCLSide IS NULL`. If `RCLSide` is null, the unique ID for the object is returned to the no_rclside error list. The selection is then cleared for further analysis.

* `Error: RCLMatch is reporting a NENA Unique ID that does not exist in the road centerline`: A join is completed between the *apTable* `RCLMatch` field and the *rcTable* unique ID field. A SelectLayerByAttribute is performed where the `rcTable.NGUID_RDCL IS NULL`. If the unique ID field is null, the `RCLMatch` value did not have a matching unique ID in the *rcTable* and so the *apTable* unique ID for the object is return to the ngsegid_doesnt_exist error list. The selection is then cleared for further analysis.

* `Error: RCLMatch does not correspond to a NENA Unique ID that matches attributes`: This analysis looks at both the left and right sides of the road centerline to see if the CODE_COMPARE fields resulting from the `prep_roads_for_comparison` function for *rcTable* and *apTable* match. A SelectLayerByAttribute is performed on the joined table to query down to `RCLSide = {current side} AND rcTable.NGUID_RDCL is not null AND apTable.CODE_COMPARE <> rcTable.CODE_COMPARE_{current side}`. If objects are selected, the *apTable* unique ID is added to the streets_or_msags_dont_match error list. The selection is then cleared for further analysis.

* `Error: Address does not fit in range of corresponding RCLMatch`/`Error: Road segment address ranges include one or more null values`: For a SelectLayerByAttribute on the joined table with the query of `RCLSide = {current side} AND rcTable.NGUID_RDCL is not null AND apTable.CODE_COMPARE = rcTable.CODE_COMPARE_{current side}`, this analysis compares the `Address` field in *apTable* to the `From/To` and `Parity` values in *rcTable* for a given road side. First, the function checks to see if the `From/To` values are not None type. If the `From/To` values are null, the *apTable* unique ID is added to the null_values error list. Next, the `Parity` value determines the range_counter (1 for "B", 2 for "O"/"E") to create a list of possible values using `From/To` values for a given side of the road segment. If the `Address` values is not within the range list, the *apTable* unique ID is added to the doesnt_match_range error list.

* The error lists of unique IDs are then parsed to the appropriate error string and returned to the *FieldValuesCheckResults* table.


### Check Frequency
* First, depending on whether we are looking at *ADDRESS_POINT* or *ROAD_CENTERLINE*, a table view will be made using the appropriate query (AP: `Address <> 0 AND SUBMIT = 'Y'`; RDCL: `Add_L_From <> 0 AND Add_L_To <> 0 AND Add_R_From <> 0 AND Add_R_To <> 0 AND SUBMIT = 'Y'`). A field concatenation is then created for the Statistics_analysis to get the count for the concatenation of the selected fields. A table view is then created where `FREQUENCY > 1`. If there are records returned in the table, then a duplicate concatenation exists and analysis to determine the unique IDs is performed. A full frequency check will return Errors, while a partial (dual carriageway) frequency check will return Notices.


### Check ESN and Muni Attributes
* First, the function checks for the existence of the *ADDRESS_POINT* feature class and creates a feature layer with the query `SUBMIT = 'Y'`. Then, the function checks for the ESZ (required) and Municipality (optional) feature classes inside the NG911 dataset. If the feature class exists, the function searches through the objects within the feature classes with the query `SUBMIT = 'Y'`. A query is then concatenated to make a feature layer of the current object using the unique ID. Then, a SelectLayerByLocation is performed between the address point feature layer and the current selected object. The function then searches through the selected address points. Next, the unique ID for the selected address point needs to be non-null. If this is the case, the function checks if the value of specified field for the current address point object is not equal to the value of the selected `ESN` or `City` field in the current feature layer. Notices are then returned when appropriate.


### Find Overlaps
* First, the function creates, calculates, and trims a string for the `NAME_OVERLAP` field in the *ROAD_CENTERLINE* feature class that will be used in the check analysis. The fields used in the concatenation are the same are as the ones used in the creation of the `FullName` field. The function then searches through the *ROAD_CENTERLINE* feature class with a query `SUBMIT = 'Y'`. The function checks to make sure the `MSAGComm` fields are not null or empty strings or a blank space. If the current segment of the road and side has not already been checked, the function then utilizes a MSAG label check function called `checkMsagLabelCombo`.

* The `checkMsagLabelCombo` function searches through the road centerline features that match the query created by concatenating a string using the values passed to the function. The function then determines the range for the those features that match the query. If the value in the range is not in the already-looked-at values for the segment and side, then the value is added to the already-looked-at list. Otherwise, the unique ID is then added to the overlaps error list. The overlap errors list is then returned to the main `FindOverlaps` function.

* If there are overlaps returned, the main `FindOverlaps` function will then make a feature layer of the *ROAD_CENTERLINE* feature class using the return unique IDs for the overlaps to create the query. An notice is then created for all the returned objects.


#### Usage
  1.	Open ArcCatalog and navigate to the toolbox called “Oklahoma NG911 GIS Tools”, expand the toolbox, then expand the toolset called “Validation Tools.” Use the tools in the numerical order presented with the following guidelines.
  2.	In the “Geodatabase” parameter, select the geodatabase of data to be checked.
  3.	Check which data checks you want to run. When running each tool for the first time, we recommend choosing all options.
  4.	Run the tool.
  5.	Alternatively, to run all checks, open and run [8 Check All Required](#8-check-all-required).
  6.	The basic results of the data checks are shared in the ArcGIS dialog box. A simple Pass/Fail text file is created in the folder containing the geodatabase called "[Geodatabase_Name].txt" when CheckAll validations are run. The detailed results of the data checks will appear in two tables that are added to your geodatabase: *TemplateCheckResults* & *FieldValuesCheckResults*. The results reported in these tables will accumulate until you run the script titled [6 Optional Clear Results Table](#6-clear-results-table-optional-).
  7.	Based on the results of the data check, you can edit your data as necessary.
  8.	After data is edited, the necessary data checks can be rerun.
  9.	The script called [7 Optional Verify Topology Exceptions](#7-verify-topology-exceptions-optional-) will double-check that all road centerline topology errors are recorded as exceptions in the data and the topology.
  10.	The script called [7.1 ESB Gap Locations](#7-1-esb-gap-locations-optional-) will look for the areas where the ESB Boundary layers are not overlapping with the Discrepancy Agency Boundary.


## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
