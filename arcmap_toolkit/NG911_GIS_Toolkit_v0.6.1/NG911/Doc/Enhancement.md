[**Oklahoma NG911 Toolkit**](../README.html) | [Adjustment](Adjustment.html) | [Comparison](Comparison.html) | [***Enhancement***](Enhancement.html) | [MSAG](MSAG.html) | [Okprep](Okprep.html) | [Submission](Submission.html) | [Validation](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [Topology Rules](Topology.html) | [Change Log](../ChangeLog.html) | [Error Glossary](ErrorGlossary.html)

# Enhancement Toolset

## Toolset Credits
* Emma Baker, Oklahoma Department of Transportation
* Riley Baird, Oklahoma Department of Transportation
* Adapted from code originally by Kristen Jordan Koenig et al., Kansas Data Access and Support Center

##### Last Revised:
June 15, 2022

## Abstract
These tools automate various tasks involved with data creation and perform various checks to enhance the quality of the data.

## Tools

### Add/Validate NG911 Topology

Script: [Enhancement_AddTopology.py](../Scripts/Enhancement_AddTopology.py)

Creates and adds layers and rules to topology and can validate topology. To export topological errors and to account for features with non-null `TopoExcept` attributes, see [Verify Topology Exceptions (Validation)](Validation.html#7-verify-topology-exceptions-optional-) for that functionality.

#### Usage

1. Open the tool and provide the path to the NG911 geodatabase.
2. If desired, select the option to validate the topology.
3. Run the tool.

#### Methodology

* First, a topology is created using the *NG911* feature dataset. Each of *ROAD_CENTERLINE*, *ADDRESS_POINT*, *ESB*, *ESB_LAW_BOUNDARY*, *ESB_EMS_BOUNDARY*, *ESB_FIRE_BOUNDARY*, *DISCREPANCYAGENCY_BOUNDARY*, *MUNICIPAL_BOUNDARY*, *ESZ_BOUNDARY*, *PSAP_BOUNDARY*, *ESB_RESCUE_BOUNDARY*, *ESB_FIREAUTOAID_BOUNDARY* are added to the topology if present. [Topology rules](Topology.html) involving single feature classes are added during this step.

* Once the feature classes have been added, the [topology rules](Topology.html) involving multiple feature classes are added. Rules involving one or more feature classes that are not present in the *NG911* feature dataset are skipped.

* If the option to validate the topology is selected, that validation is done at this point.

### Assign Unique NENA ID

Script: [Enhancement_AssignID.py](../Scripts/Enhancement_AssignID.py)

Creates a NENA unique ID for features in a feature class. The feature class does NOT have to be Standards-compliant. Can generate new IDs for all input features or just change null IDs. The user may optionally provide a field with existing local unique IDs consisting of numbers, characters, dashes, and curly-braces to be incorporated into the newly-generated NENA IDs, or the user can allow the tool to generate sequential numbers for the NENA IDs. Required field is `Agency_ID`.

#### Usage

1. Select the name type of layer the input data contains.
2. Provide the feature class containing the features to which a unique ID will be assigned.
3. Select the name of the field to be used for the unique ID. If the field names are already Standards-compliant, this field's name will begin with `NGUID_`.
4. Select the name of the field containing the agency ID. This will be used in calculating the unique ID. If the field names are already Standards-compliant, this field's name will be `Agency_ID`.
5. If available, provide a field containing a number (or string representing a number) to be used in the unique ID. If not provided, sequential numbers starting at 1 will be used.
6. To recalculate unique IDs for all features, select the "Overwrite All Unique IDs" option. To only update features without unique IDs, leave this option unchecked.
7. Run the tool.

#### Methodology

* If "Overwrite All Unique IDs" is not selected, the tool generates a feature layer based on the input features where the specified unique ID attribute is null.

* If "Unique Local911 ID" is not provided, the tool searches for the highest ID number currently in use in the input feature class.

* An UpdateCursor is used to calculate the new unique ID based on the layer name, the agency ID, and either the Local911 ID or a sequentially-generated number. If a feature's `Agency_ID` (or equivalent) field is null, that feature is skipped.

  * If "Unique Local911 ID" is provided and a feature's Local911 ID attribute does not match the regular expression `^[{}A-Za-z\d-]+$`, that feature is skipped.

### Calculate FullName and FullAddr

Script: [Enhancement_CalculateFullNameFullAddr.py](../Scripts/Enhancement_CalculateFullNameFullAddr.py)

Calculates the `FullName` field of either an address point feature class or the road centerline feature class or `FullAddr` for the address point feature class. For the `FullAddr` field, the fields used for the calculation are: `AddPre`, `Address`, `AddSuf`, `PreDir`, `PreMod`, `PreType`, `PreTypeSep`, `Street`, `StreetType`, `SufDir`, `SufMod`, `BldgName`, `BldgUnit`. For the `FullName` field, the fields used for the calculation are: `PreDir`, `PreMod`, `PreType`, `PreTypeSep`, `Street`, `StreetType`, `SufDir`, and `SufMod`.

#### Usage

1. Open the tool and provide either an *ADDRESS_POINT* or *ROAD_CENTERLINE* feature class.
2. If the input feature class is *ADDRESS_POINT*, the options to calculate either or both of `FullName` and `FullAddr` are available. If the input feature class is *ROAD_CENTERLINE*, only the `FullName` option is available.

#### Methodology

* If "Calculate FullAddr" is selected, the tool fetches the requisite fields for the `FullAddr` field. For each feature, those attributes are concatenated (nulls are ignored), and the resulting string is written to the feature's `FullAddr` field.
  * For any feature, if a concatenated string is too long for the `FullAddr` field, that feature's `FullAddr` attribute will be set to null.

* If "Calculate FullName" is selected, the tool fetches the requisite fields for the `FullName` field. For each feature, those attributes are concatenated (nulls are ignored), and the resulting string is written to the feature's `FullName` field.
  * For any feature, if a concatenated string is too long for the `FullName` field, that feature's `FullName` attribute will be set to null.

### Calculate Parity

Script: [Enhancement_CalculateParity.py](../Scripts/Enhancement_CalculateParity.py)

Calculates the `Parity_L` and `Parity_R` fields of a road centerline feature class. The fields used for the calculation are: `Add_L_To`, `Add_L_From`, `Add_R_To`, `Add_R_From` and `NGUID_RDCL`. The tool will used the last digit on both sides to determine whether the number is `EVEN`, `ODD`, `BOTH`, or `ZERO`.

#### Usage

1. Open the tool and provide the *ROAD_CENTERLINE* feature class.
2. If desired, select "Overwrite Existing" to recalculate the parity for all features, including those where the `Parity_L` and `Parity_R` fields are non-null.

#### Methodology

* This tool utilizes a function called `parity_of`, also included in this tools's script file. Given an integer <math>a</math>, `parity_of` performs the operation <math>a mod 2</math>. A result of <math>1</math> indicates that <math>a</math> is odd, and the function returns the string `ODD`. a result of <math>0</math> indicates that it is even, and the function returns the string `EVEN`.

* The tool checks the value of each feature's `Add_L_From` and `Add_L_To` attributes to determine the appropriate value for `Parity_L`. If they are both `0`, the `Parity_L` attribute is set to `Z` (for "zero"). If `parity_of` returns `EVEN` for both, parity is set to `E`. If `parity_of` returns `ODD` for both, `Parity_L` is set to `O`. Otherwise, `Parity_L` is set to `B` (for "both").

* That process is repeated using `Add_R_From`, `Add_R_To`, and `Parity_R`.

### Check Road ESN Values <span class="uses-submit">Uses `SUBMIT`</span>

Script: [Enhancement_CheckRoadESN_Launch.py](../Scripts/Enhancement_CheckRoadESN_Launch.py)

Ensures the road centerline `Esn_L` and `Esn_R` values match the ESN values of the road’s spatial location. Results will be reported in *FieldValuesCheckResults*. This tool only produces Notices, not Errors, and therefore its results will not prevent submission. ESZ required fields include `NGUID_ESZ`, `ESN` and `SUBMIT`. Road Centerline required fields include `NGUID_RDCL`, `Esn_L`, `Esn_R`, and `SUBMIT`. There is an option to run an Advanced License Analysis, which is a faster, more thorough analysis that requires an Advanced License to run.

#### Usage

1. Open the tool and provide the path to the NG911 geodatabase.
2. If desired, select the "Run Advanced License Analysis". This requires an Advanced License.
3. Run the tool.

#### Methodology - Regular Analysis

* If the *ROAD_CENTERLINE* and *ESZ_BOUNDARY* feature classes exist, feature layers (*rd_lyr*, *esz_lyr*) with the query `SUBMIT = 'Y'` are created for both feature classes. While searching through the ESZ feature layer, a new feature layer (*eszf*) is created for each unique ID. A selection of road centerlines is then created where the lines "HAVE_THEIR_CENTER_IN" the new esz feature layer (any ESZ boundary objects with the current ESZ unique ID). A Search cursor is then opened for the currently selected road centerlines.

* If the `ESN_R` and `ESN_L` are both not zero and not equal to each other, an "analog" analysis of both sides is required. First, a feature layer (*rd_buff_lyr*) is created for the current unique ID, and a feature layer (*esz_lyr_select*) is created for the *ESZ_BOUNDARY* with all the objects. A selection of ESZ objects that "INTERSECT" the current road centerline segment is then searched through in order to create a "esn_score", "l_score", and "r_score" that will eventually correspond with a given Notice.
    * First, a list of all `ESN` values that have been selected is created for analysis and initial scores set to zero.
    * If, the values of `ESN` for the *ESZ_BOUDNARY* match any of the values of the current *ROAD_CENTERLINE* then the `esn_score` increases by 1.
    * A temporary buffer is then created `in_memory` 30 feet around the current road centerline segment. Next, an Intersection analysis is run between the temporary buffer and all the *ESZ_BOUNDARY* objects. The function then searches through the intersection output and does a SHAPE comparison analysis between the *ESZ_BOUNDARY* and the *ROAD_CENTERLINE* to make sure `ESN_L` value is on the left side and `ESN_R` value is on the right side.

* Else, the function checks to make sure that the `ESN` value is the same on both sides and non-zero.

#### Methodology - Advanced Analysis

* If the *ROAD_CENTERLINE* and *ESZ_BOUNDARY* feature classes exist, feature layers (*road_submit_layer*, *esz_submit_layer*) with the query `SUBMIT = 'Y'` are created for both feature classes.
* The function then runs the Identity tool between the *ROAD_CENTERLINE* and *ESZ_BOUNDARY* putting the output *identity_output* in_memory.
* A feature layer (*mismatch_layer*) is then created using the query `{road centerline ESN_L} <> LEFT_{ESZ ESN} OR {road centerline ESN_R} <> RIGHT_{ESZ ESN}`.
* A set (unique list) of unique IDs for *ROAD_CENTERLINE* is then created from the mismatch_layer feature layer and a feature layer (*potential_problems_layer*) is created from the *road_submit_layer* where the unique ID is in the unique ID set.
* The 30 foot buffer layers for the left and right side are then created `in_memory` using a "FLAT" end configuration. The function next creates sets of correct *ROAD_CENTERLINE* unique IDs for the left and right side using the *ROAD_CENTERLINE* and *ESZ_BOUDNARY* geometry (`SHAPE@`) and values of `ESN`, `ESN_L`, and `ESN_R`.
* The function then performs set math to get the sets that instersect (where both right and left sides match) and the sets that don't intersect (where one or both sides are mismatched). Further set analysis returns the specific Notices for the mismatching sides.

### Check Road FromLevel ToLevel

Script: [Enhancement_CheckRoadElevationDirection.py](../Scripts/Enhancement_CheckRoadElevationDirection.py)

Ensures the `FromLevel` and `ToLevel` attributes correctly depict the overpass level rise and fall along road segments that are both touching and have the same `FullName`. Required fields include `NGUID_RDCL`, `Add_L_From`, `FullName`, `FromLevel`, `ToLevel`.

#### Usage

1. Open the tool and provide the path to the NG911 geodatabase.
2. Run the tool.

#### Methodology

* First, the function searches through the *ROAD_CENTERLINE* ordered by `FullName` then `Add_L_From` to create a list of bad segments if the end of segment A is equal to the beginning segment B and the two segments are not disjointed.

* If bad segments exists, Notices are constructed and appended to *FieldValuesCheckResults*.

### Find Address Range Overlaps

Script: [Enhancement_FindAddressRangeOverlaps.py](../Scripts/Enhancement_FindAddressRangeOverlaps.py)

Finds road centerline segments where address ranges overlap. For example, if a segment of a road centerline polyline feature with `Add_L_From` and `Add_L_To` values of 900 and 1000, respectively, was adjacent to another segment of the same polyline with an `Add_L_From` value of 990, this tool would report an overlap. Overlapping address ranges can negatively affect geocoding accuracy. Road Centerline required fields include `Parity_L`, `Parity_R`, `Add_L_From`, `Add_L_To`, `Add_R_From`, `Add_R_To`, `MSAGComm_L`, `MSAGComm_R`, `GeoMSAG_L`, `GeoMSAG_R`, `NGUID_RDCL`, `SUBMIT`, `FullName`.

#### Usage

1. Open the tool and provide the path to the NG911 geodatabase.
2. Run the tool.

#### Methodology

* The tool temporarily adds a field to *ROAD_CENTERLINE* called `NAME_OVERLAP`. It opens an `UpdateCursor` with the new `NAME_OVERLAP` field and [all fields used to calculate `FullName`]. `NAME_OVERLAP` is calculated similarly to `FullName`.
* Next, a `SearchCursor` looks through *ROAD_CENTERLINE* to confirm that all features where `GeoMSAG_L` and `GeoMSAG_R` are set to `Y` have non-null `MSAGComm_L` and `MSAGComm_R` attributes, respectively. If there is a discrepancy, a Notice is reported to *FieldValuesCheckResults*.
* If the feature information is not in the list of `already_checked` and the sides check is on, the function then runs through `checkMsagLabelCombo` to find the overlaps for a given side and adds that feature's information to `already_checked`. This is done for both the left and right sides.
    * The `checkMsagLabelCombo` function searches through the *ROAD_CENTERLINE* feature class queried to the current `MSAGComm` field, the current `NAME_OVERLAP`, where `SUBMIT = 'Y'`, and where the `GeoMSAG` field for the given side is also `Y`. A dictionary of information regarding the left and right side of the road segment is then created. For either side of the road, a range list for "from" and "to" with a given "parity" is returned using the `launchRangeFinder` function.
        * The `launchRangeFinder` function checks for non-zero "from" and "to" values and a non-`Z` value for the parity. If these are true, the function then creates a list of possible range values given the "from", "to", and "parity" values.
    * If a range list is returned, the information about the segment with the side `{segid|side}` is added to the `dict_ranges` dictionary (with `segid|side` as a key) to track the values. If the value in the returned range list is currently not in the `address_list` list, then append it. Else, the function then loops through all the keys `{segid|side}` in the `dict_ranges` dictionary. If the current value in the range list is in the values of the current key then if the value of `segid` for the dictionary is not in the overlaps that have already been added, the function adds it to the overlaps list. If the value of the `segid` for the current road segment is not in the overlaps list, then it is also appended to the overlaps list. The new updated list of overlaps is then returned to the `FindOverlaps` function.
* If overlaps are returned in the analysis, an overlap notice flag is returned, and an analysis is run on the overlaps list to return the proper Notices in the *FieldValuesCheckResults* table.

### [Generate Fishbone Analysis](FishboneAddressVerification.html)

Script: [Enhancement_FishboneAnalysis.py](../Scripts/Enhancement_FishboneAnalysis.py)

Can be used to generate a "Dirty" Fishbone Analysis for Address Point Verification. The analysis is considered dirty, because the fishbone line shapefile is created without the user performing a quality check on the geocoded data. Ties and non-matches are simply removed from the analysis. This tool should be used as an aid to the QA/QC process and **not** as a complete quality check of the data. Address Point required fields include `City`, `State`, `Zipcode`, `Latitude`, `Longitude`, `FullAddr`, and [all fields used to calculate `FullAddr`]. Road Centerline required fields include `Add_L_From`, `Add_L_To`, `Add_R_From`, `Add_R_To`, `Parity_L`, `Parity_R`, `City_L`, `City_R`, `County_L`,`County_R`, `State_L`,`State_R`, `Zipcode_L`,`Zipcode_R`, `NGUID_RDCL`, `FullName`, and [all fields used to calculate `FullName`].

#### Usage &amp; Methodology

See the Supplementary Documentation: [Generate Fishbone Analysis Tool](FishboneAddressVerification.html#running-a-fishbone-analysis-without-the-generate-fishbone-analysis-tool).

### Geocompare Address Points <span class="uses-submit">Uses `SUBMIT`</span>

Script: [Enhancement_GeocodeAddressPoints.py](../Scripts/Enhancement_GeocodeAddressPoints.py)

Compares the address points against the road centerline data and computes the appropriate values for the fields `RCLMatch` and `RCLSide`. Address Point required fields include `RCLMatch`, `RCLSide`, `MSAGComm`, `NGUID_ADD`, `SUBMIT`, `FullAddr`, and [all fields used to calculate `FullAddr`]. Road Centerline required fields include `Add_L_From`, `Add_L_To`, `Add_R_From`, `Add_R_To`, `Parity_L`, `Parity_R`, `MSAGComm_L`, `MSAGComm_R`, `NGUID_RDCL`, `SUBMIT`, `FullName`, and [all fields used to calculate `FullName`].

#### Usage

1. Open the tool and provide the path to the NG911 geodatabase.
2. If desired, select "Update Empty Only" to skip features that already have a non-null `RCLMatch` attribute.

#### Methodology

* The tool creates a table called *AddressPt_GC_Results* in which results will be stored. A feature layer is created from *ADDRESS_POINT* containing records where `SUBMIT = 'Y'` (and, if "Update Empty Only" was selected, where `RCLMatch IS NULL OR RCLMatch IN ('', ' ', 'TIES', 'NO_MATCH', 'NULL_ID')`). These features are copied to *AddressPt_GC_Results*.

* `launch_compare` is called.
    * `prep_roads_for_comparison` is called, passing *AddressPt_GC_Results* as `output_table`.
        * The field `NAME_COMPARE` is added to *AddressPt_GC_Results*. It is calculated using [all fields used to calculate `FullName`].
        * The field `CODE_COMPARE` is computed using Python code inside of a string variable called `code_block` in `MSAG_DBComparison.py`. If you have any clue how this works, please tell us, because we sure don't. Its intention appears to be to produce a unique code based on a combination of a given `NAME_FIELD` attribute and an `MSAGComm` attribute.
    * A table view called *rc_table_view* is created from *ROAD_CENTERLINE* features where `SUBMIT = 'Y'`, and those rows are copied to an `in_memory` table called *rcTable*.
    * `prep_roads_for_comparison` is again called, passing *rcTable* for `output_table`.
        * `NAME_COMPARE`, `CODE_COMPARE_L`, and `CODE_COMPARE_R` are computed using `MSAGComm_L`, `MSAGComm_R`, and [all fields used to calculate `FullName`], similar to the process used for *AddressPt_GC_Results*.

* An index called `AddrIdx` is created for `NGUID_ADD`. A feature layer *fl* is created from *ADDRESS_POINT* with the same where clause used for the creation of *AddressPt_GC_Results*.

* A feature layer *ot_fl* is derived from *AddressPt_GC_Results*. *ot_fl* is joined to the target *fl* on `NGUID_ADD` using the `KEEP_COMMON` rule.

* In the joined layer, `AddressPt_GC_Results.NGUID_RDCL` is copied to `ADDRESS_POINT.RCLMatch`, and `AddressPt_GC_Results.RCLSide` is copied to `ADDRESS_POINT.RCLSide`.


### Populate RCLMatch NO_MATCH

Script: [Conversion_AP_RCLMATCH_NO_MATCH.py](../Scripts/Conversion_AP_RCLMATCH_NO_MATCH.py)

Requires the `RCLMatch` field. Populates any blank or null `RCLMatch` attributes with `NO_MATCH`. It can optionally also overwrite `RCLMatch` values of `TIES` with `NO_MATCH`.

#### Usage

1. Open the tool and provide the path to the NG911 geodatabase.
2. If desired, select the "Overwrite TIES to NO_MATCH".
3. Run the tool.

#### Methodology

* Using an `UpdateCursor`, *ADDRESS_POINT* features with values of null (and, if the option is selected, `TIES`) for their `RCLMatch` attributes have those attributes overwritten to `NO_MATCH`.


## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

[all fields used to calculate `FullName`]: <#calculate-fullname-and-fulladdr>
[all fields used to calculate `FullAddr`]: <#calculate-fullname-and-fulladdr>

<!-- CSS for styling by class -->

<style>
.invest {
    color: darkred;
    font-size: 14pt;
    font-weight: bold;
    background-color: pink;
    vertical-align: text-top;
    border: 2px solid red;
    padding: 2px;
}

.ignores-submit, .uses-submit, .ignores-topoexcept {
    padding-left: 4.5px;
    border-radius: 10px;
    vertical-align: text-middle;
    font-size: 11.5pt;
}

.ignores-submit {
    color: #997a00;
    background-color: #fff0b3;
    border: 2px solid #997a00;
}

.ignores-topoexcept {
    color: #6c6e1a;
    background-color: #b8ba20;
    border: 2px solid #6c6e1a;
}

.uses-submit {
    color: #009933;
    background-color: #ccff99;
    border: 2px solid #009933;
}
</style>
