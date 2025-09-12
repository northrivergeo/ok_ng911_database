[**Oklahoma NG911 Toolkit**](../README.html) | [Adjustment](Adjustment.html) | [Comparison](Comparison.html) | [Enhancement](Enhancement.html) | [MSAG](MSAG.html) | [Okprep](Okprep.html) | [Submission](Submission.html) | [Validation](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [Topology Rules](Topology.html) | [Change Log](../ChangeLog.html) | [***Error Glossary***](ErrorGlossary.html)

# Error Glossary

## Documentation Credits
* Emma Baker, Oklahoma Department of Transportation
* Riley Baird, Oklahoma Department of Transportation

##### Last Revised:
June 15, 2022

## Abstract
This document lists and describes the various messages written to the geoprocessing console, the *TemplateCheckResults* table, and the *FieldValuesCheckResults* table. In cases where the exact text of a message may vary, the contents of the variable part(s) are described in `{curly braces}`.

**Errors** describe issues that impede submission. **Notices** do not impede submission.

## Template Validations

### Check Layer List <span class="ignores-submit">Ignores `SUBMIT`</span>

* `Error: No feature dataset named 'NG911' exists` - The NG911 geodatabase does not contain a feature dataset named *NG911*. (*TemplateCheckResults*)

* `Error: Required layer {feature class name} is not in geodatabase dataset.` - A required feature class with the indicated name does not exist in the *NG911* feature dataset. (*TemplateCheckResults*)

If this check generates any errors, a console warning is printed: `Not all required geodatabase datasets and/or layers are not present. See TemplateCheckResults.`

### Check GDB Domains <span class="ignores-submit">Ignores `SUBMIT`</span>

* `Error: Domain Name {domain name} is not an approved domain.` - The geodatabase contains a domain with a non-standard name. (*FieldValuesCheckResults*)

* `Error: Domain Coded Value '{code}' for {domain name} Domain is incorrect.` - A coded value that is not Standards-compliant exists in a domain. (*FieldValuesCheckResults*)

* `Error: Domain Coded Value Description '{existing code description}' for {code} coded value in {domain name} Domain is incorrect and should be '{standard code description}'.` - The description for a coded value is not Standards-compliant. The descriptions in the message may be abbreviated. (*FieldValuesCheckResults*)

* `Notice: Domain Description '{existing domain description}' for {domain name} Domain should be '{standard domain description}'.` - The domain description for a Standards-compliant domain name is not Standards-compliant. The descriptions in the message may be abbreviated. (*FieldValuesCheckResults*)

If this check generates any errors, a console warning is printed: `Completed checking GDB domains: {#} issues found. See table FieldValuesCheckResults for results.`

### Check Spatial Reference <span class="ignores-submit">Ignores `SUBMIT`</span>

* `Error: Spatial reference of feature dataset is incorrect.` - The *NG911* feature dataset does not have the correct spatial reference. (*TemplateCheckResults*)

If this check generates any errors, the above error is also printed to the console as a warning.

### Check Required Fields <span class="ignores-submit">Ignores `SUBMIT`</span>

* `Error: {feature class name} does not have required field {field name}` - A field required by the Standards does not exist in a feature class. (*TemplateCheckResults*)

* `Error: HNO/Address field of Address Points is not an integer or a double, it is a {field data type}` - The data type of the `Address` field in the *ADDRESS_POINT* feature class should be numeric. (*TemplateCheckResults*)

If a required feature class does not exist inside the *NG911* feature dataset, a console warning is printed: `Required layer {feature class name} does not exist`

If this check generates any errors, a console warning is printed: `Completed check for required fields: {#} issues found. See table FieldValuesCheckResults for results.`

### Check Required Field Values <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: {field name} is null for Feature ID {NGUID}` - A required field is null for a specific feature. (*FieldValuesCheckResults*)

If a feature class does not have a field named `SUBMIT`, a console warning is printed: `Cannot check required field values for {feature class name}`

If a feature class is missing one or more required fields, a console warning is printed: `Could not check all fields in {feature class name}. Looking for: {list of required fields}`

If a feature class has no features where `SUBMIT` is `Y`, a console warning is printed: `{Feature class name} has no records marked for submission. Data will not be verified.`

If a required feature class does not exist inside the *NG911* feature dataset, a console warning is printed: `Required layer {feature class name} does not exist`

If this check generates any errors, a console warning is printed: `Completed check for required field values: {#} issues found. See table FieldValuesCheckResults for results.`

### Check Submission Numbers <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: {feature class name} has 0 records for submission` - A required feature class has no features where `SUBMIT` is `Y`. (*TemplateCheckResults*)

If a feature class does not have a field named `SUBMIT`, a console warning is printed: `SUBMIT field does not exist in required layer {feature class name}`

If a required feature class does not exist inside the *NG911* feature dataset, a console warning is printed: `Required layer {feature class name} does not exist`

If this check generates any errors, a console warning is printed: `One or more layers had no features to submit. See table TemplateCheckResults.`

### Find Invalid Geometry <span class="ignores-submit">Ignores `SUBMIT`</span>

* `Error: Invalid geometry` - A feature does not contain the minimum necessary number of points per its indicated geometry. (Point: &ge;1, Line: &ge;2, Polygon: &ge;3) (*FieldValuesCheckResults*)

If a feature class has no NGUID field, a console warning is printed: `NGUID field {field name} does not exist in {feature class name}`

If a required feature class does not exist inside the *NG911* feature dataset, a console warning is printed: `Required layer {feature class name} does not exist`

If this check generates any errors, a console warning is printed: `Completed for invalid geometry: {#} issues found. See FieldValuesCheckResults.`

### Check Values Against Domain <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: Value {field value} not in approved domain for field {field name}` - A field contains a value (other than null or an empty string) that is not in the Standards-compliant domain. (*FieldValuesCheckResults*)

* `Error: Value {field value} not in approved domain for field {field name}` - The value of the `Address` field is either less than 0 or greater than 999999. (*FieldValuesCheckResults*)

If a feature class has no features where `SUBMIT` is `Y`, a console warning is printed: `No features are marked for submission in {feature class name}. Please mark records for submission by placing Y in the SUBMIT field.`

If a feature class does not have a field named `SUBMIT`, a console warning is printed: `Cannot check required field values for {feature class name} because the SUBMIT field does not exist.`

If a feature class is missing one or more fields with domains, a console warning is printed: `Field {field name} in feature class {feature class name} does not exist, and its values cannot be checked against domain {domain name}.`

If a required feature class does not exist inside the *NG911* feature dataset, a console warning is printed: `Required layer {feature class name} does not exist`

If this check generates any errors, a console warning is printed: `Completed checking fields against domains: {#} issues found. See table FieldValuesCheckResults for results.`

### Check Feature Locations <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: Feature not inside discrepancy agency boundary` - A feature was found to not be within any *DISCREPANCYAGENCY_BOUNDARY* feature, **and** the feature does not have a `TopoExcept` value of `INSIDE_EXCEPTION` or `BOTH_EXCEPTION` (if applicable). Detailed information on topology rules involving the *DISCREPANCYAGENCY_BOUNDARY* feature class can be found in the [NG911 Topology Rules](Topology.html#rules-involving-the-discrepancyagency_boundary-layer) documentation. (*FieldValuesCheckResults*)

If neither *DISCREPANCYAGENCY_BOUNDARY* (in the *NG911* feature dataset) nor *COUNTY_BOUNDARY* (in the *OptionalLayers* feature dataset) exist, a console warning is printed: `Check Feature Locations could not run because the discrepancy agency and/or county boundary feature classes are absent or misnamed.`

<!--

=========================================================
= = = = = = = = = = INVESTIGATE THIS! = = = = = = = = = =
=========================================================

DUE TO THE TRY/EXCEPT BLOCK STARTING WITH LINE 2912, IT APPEARS THAT THIS CHECK MAY NOT PRODUCE ANY OUTPUT ERRORS IF IT ENCOUNTERS AN ISSUE DURING EXECUTION BEFORE RECORDS ARE ADDED TO THE values LIST!

-->

<!-- SEE DATACHECK LINE 2922 IF | If the Standards do not specify an NGUID field for a feature class, a console warning is printed: `Could not process features in {feature class name} because unique ID is empty.`-->

<!-- SEE DATACHECK LINE 2912 TRY | If there is an execution error, a console warning is printed: `Could not check locations of {feature class name}`-->

If this check generates any errors, a console warning is printed: `{Feature class name}: issues with some feature locations` <!-- MADE REDUNDANT BY BELOW? -->

If this check generates any errors, a console warning is printed: `Completed check on feature locations: {#} issues found. See table FieldValuesCheckResults.`

### Check Topology <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: Both origin and destination feature class names are null.` - Both Origin and Destination feature class name fields in an error feature class are None, a blank string, or a space. (*FieldValuesCheckResults*)

* `Error: Topology issue- {topology rule} | Number of errors- {#}` - A topology rule was violated, and the violating feature was not marked as an exception with its `TopoExcept` field (if applicable). Detailed information on topology rules can be found in the [NG911 Topology Rules](Topology.html) documentation. (*FieldValuesCheckResults*)

If this check generates any errors, a console warning is printed: `Topology check complete. {#} issues found. Results in FieldValuesCheckResults.`

### Check Unique ID Format and Frequency <span class="ignores-submit">Ignores `SUBMIT`</span>

* `Error: {NGUID} is a duplicate ID` - The same NGUID was found on multiple records (i.e. that unique ID is not unique). (*FieldValuesCheckResults*)

* `Error: Unique ID format wrong.` - The unique ID is not in the Standards-compliant format. (*FieldValuesCheckResults*)

* `Error: {#} records with null Unique IDs.` - One or more features have a [null\*] unique ID attribute. (*FieldValuesCheckResults*)

If a required feature class is not found, a console warning is printed: `{Feature class name} does not exist`

If this check generates any errors, a console warning is printed: `There are {#} records in {feature class name} with null or incorrectly-formatted unique IDs.`

If this check generates any errors, a console warning is printed: `Checked unique ID frequency. There were {#} issues. Results are in table FieldValuesCheckResults.`

## Address Point Validations

If the *ADDRESS_POINT* feature class was not found in its expected location, a console warning is printed: `Layer ADDRESS_POINT does not exist and therefore cannot be checked. This will prevent submission.`

### Check MSAGComm Spaces <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: {MSAGComm field name} has a leading or trailing space.` - A feature's `MSAGComm`, `MSAGComm_L`, or `MSAGComm_R` attribute begins or ends with a space. `MSAGComm`, `MSAGComm_L`, and `MSAGComm_R` attributes should consist neither of a space followed by one or more characters nor of one or more characters followed by a space. (*FieldValuesCheckResults*)

* `Notice: {MSAGComm field name} is a blank string or has only a space.` - A feature's `MSAGComm`, `MSAGComm_L`, or `MSAGComm_R` attribute is not null, but consists of a text string either with no characters or with a single space as the only character. (*FieldValuesCheckResults*)

If this check generates any errors, a console warning is printed: `Check complete. {#} issues found. See table FieldValuesCheckResults for results.`

### Check RCLMatch <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: RCLMatch is reporting a NENA Unique ID that does not exist in the road centerline` - The `RCLMatch` attribute of an *ADDRESS_POINT* feature is not null, but there is no *ROAD_CENTERLINE* feature with that `NGUID_RDCL` attribute. (*FieldValuesCheckResults*)

* `Error: RCLMatch does not correspond to a NENA Unique ID that matches attributes` - The matching *ROAD_CENTERLINE* feature's street-name-related or `MSAGComm` attributes don't match those of the *ADDRESS_POINT* feature. (*FieldValuesCheckResults*)

* `Error: Address does not fit in range of corresponding RCLMatch` - The *ADDRESS_POINT* feature's `Address` attribute is not within the matching *ROAD_CENTERLINE* feature's address range (defined by `Add_L_From`, `Add_L_To`, `Add_R_From`, `Add_R_To`). (*FieldValuesCheckResults*)

* `Error: Road segment address ranges include one or more null values` - One or more of the matching *ROAD_CENTERLINE* feature's `Add_L_From`, `Add_L_To`, `Add_R_From`, and `Add_R_To` attributes are null instead of numeric. (*FieldValuesCheckResults*)

* `Error: RCLSide is null` - The *ADDRESS_POINT* feature's `RCLSide` attribute is null. (*FieldValuesCheckResults*)

If the *ADDRESS_POINT* feature class does not have an `RCLMatch` field, a console warning is printed: `Missing required field RCLMatch.`

If this check generates any errors, a console warning is printed: `Check complete. {#} issues found. See table FieldValuesCheckResults for results.`

### Check Frequency <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: Frequency table exists; please delete or close and rerun the check.` - The frequency table exists, and the tool failed to delete it. (*FieldValuesCheckResults*)

* `Error: {NGUID} has duplicate field information` - A record has a combination of certain attributes identical to that of another record where this combination should be unique. For example, an error involving an *ADDRESS_POINT* feature means there are multiple features represent the same address. (*FieldValuesCheckResults*)

* `Error: Could not complete duplicate record check. {Error technical information}` - The program encountered an execution error. (*FieldValuesCheckResults*)

* `Notice: {NGUID_RDCL} has duplicate address range information` - Multiple *ROAD_CENTERLINE* features have one or more of their `Add_L_From`, `Add_L_To`, `Add_R_From`, and `Add_R_To` attributes that are identical. (*FieldValuesCheckResults*)

If the frequency table (*AP_Freq* or *Road_Freq*) exists and the script cannot delete it, a console warning is printed: `Please manually delete {frequency table name} and then run the frequency check again.`

If the `Address` field of the *ADDRESS_POINT* feature class is not of type `Integer` or `Double`, a console warning is printed: `Address field of Address Points is not an integer or a double field.`

If this check generates any errors, a console warning is printed: `Checked frequency. There were {#} duplicate records. Individual results are in table FieldValuesCheckResults`

### Check ESN and Municipality Attribute <span class="uses-submit">Uses `SUBMIT`</span>

* `Notice: Address point {OBJECTID} does not match {either "ESN" or "City"} in {either "ESZ_BOUNDARY" or "MUNICIPAL_BOUNDARY"} layer.` - (*FieldValuesCheckResults*)

* `Notice: Address point with OBJECTID {OBJECTID} does not have a NENA Unique ID. Its {either "ESN" or "City"} attribute was not checked against its containing {either "ESZ_BOUNDARY" or "MUNICIPAL_BOUNDARY"} polygon.` - (*FieldValuesCheckResults*)

* `Notice: ESN/Municipality check did not run. {Error technical information}` - The program encountered an execution error. (*FieldValuesCheckResults*)

If the *ADDRESS_POINT* feature class was not found in its expected location, a console warning is printed: `{Input path to ADDRESS_POINT} does not exist`

If the *ESZ_BOUNDARY* feature class was not found in its expected location, a console warning is printed: `ESZ layer does not exist. Cannot complete check.`

## Road Centerline Validations

### Check MSAGComm Spaces <span class="uses-submit">Uses `SUBMIT`</span>

[See entry in Address Point Validations section.](#check-msagcomm-spaces)

### Check Frequency <span class="uses-submit">Uses `SUBMIT`</span>

[See entry in Address Point Validations section.](#check-frequency)

### Check Cutbacks <span class="uses-submit">Uses `SUBMIT`</span>

* `Notice: This segment might contain a geometry cutback.` - A *ROAD_CENTERLINE* polyline feature has two adjacent segments that form an angle sharper than 55&deg;. This **may** indicate a data error, or it may simply represent a road with an exceptionally sharp curve. (*FieldValuesCheckResults*)

If the *ROAD_CENTERLINE* feature class was not found in its expected location, a console warning is printed: `{Input path to ROAD_CENTERLINE} does not exist`

If this check generates any **notices**, a console warning is printed: `Completed check on cutbacks: {#} issues found. See FieldValuesCheckResults.`

### Check Directionality <span class="uses-submit">Uses `SUBMIT`</span>

* `Notice: Segment's address range is from high to low instead of low to high` - For the indicated feature, `Add_L_From` > `Add_L_To` and/or `Add_R_From` > `Add_R_To` instead of the other way around. (*FieldValuesCheckResults*)

If this check generates any **notices**, a console warning is printed: `Completed road directionality check. There were {#} issues. Results are in table FieldValuesCheckResults.`

### Check Address Range Overlaps <span class="uses-submit">Uses `SUBMIT`</span>

* `Notice: {MSAGComm field} needs to be a real value` - The value of `MSAGComm_L` or `MSAGComm_R` (as specified in the notice) is [null\*]. (*FieldValuesCheckResults*)

* `Notice: {NGUID_RDCL} has an overlapping address range.` - A *ROAD_CENTERLINE* feature overlaps an address range of another feature. (*FieldValuesCheckResults*)

If this check generates any **notices**, a console warning is printed: `{#} overlapping address range segments found. Please see {full path to AddressRange_Overlap output} for overlap results.`

### Check Parities <span class="uses-submit">Uses `SUBMIT`</span>

* `Error: Could not process parity check. Look for null values.` - One or more parity attributes are null. (*FieldValuesCheckResults*)

* `Error: Could not process parity check for a road segment with a null unique ID.` - A *ROAD_CENTERLINE* feature has a null unique ID, and a parity report could not be created. (*FieldValuesCheckResults*)

* `Error: One or more address ranges are null` - One or more address range attributes are null. (*FieldValuesCheckResults*)

* `Notice: {"L" or "R"} Side- Address range is 0-0, but the parity is recorded as {parity type} instead of Z` - The address range from and to attributes are both 0, so the parity should be set to `Z` (zero). (*FieldValuesCheckResults*)

* `Notice: {"L" or "R"} Side- Parity is Z (zero), but the address range is filled in with non-zero numbers.` - One or more address range attributes are non-zero, but the corresponding parity attribute is Z (zero). (*FieldValuesCheckResults*)

* `Notice: {"L" or "R"} Side- Parity is marked as {parity type} but the ranges filled in are {parity type} and {parity type}` - The parity attribute does not match the actual parities of the address range attributes. (*FieldValuesCheckResults*)

* `Notice: A wild error appeared! The wild error used {generic video game attack move}! It's a one-hit KO! {Message}` - The developers do not expect this situation to ever occur, but if it does, please email the support contacts listed below. (*FieldValuesCheckResults*)

If any *ROAD_CENTERLINE* feature's `Parity_L` or `Parity_R` attribute is null, a console warning is printed: `You have one or more parities set as null. Please populate those fields.`

If this check generates any errors, a console warning is printed: `Completed parity check. There were {#} issues. Results are in table FieldValuesCheckResults.`

<hr />

##### Note on Null

Where "null" is followed by an asterisk, "null" refers to any of the following: SQL `NULL`, Python `None`, a blank string (`''`), or a string consisting only of a single space (`' '`).

## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

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
    color: #b8ba20;
    background-color: #ccff99;
    border: 2px solid #009933;
}

.uses-submit {
    color: #009933;
    background-color: #ccff99;
    border: 2px solid #009933;
}
</style>

<!-- Script for styling error, warning, and notice text. -->

<script>
opacity = 0.07
for (codeElem of document.querySelectorAll("code")) {
    if (codeElem.innerText.startsWith("Error: ")) {
        codeElem.style.backgroundColor = `rgba(255,31,35,${opacity})`
    }
    else if (codeElem.innerText.startsWith("Notice: ")) {
        codeElem.style.backgroundColor = `rgba(27,31,255,${opacity})`
    }
}
for (pElem of document.querySelectorAll("p")) {
    if (pElem.innerText.search("a console warning is printed:") >= 0) {
        pElem.querySelector("code:last-of-type").style.backgroundColor = `rgba(255,255,35,${opacity})`
    }
}
line = document.querySelector("h2#abstract + * + p")
line.querySelector("strong:first-of-type").style.backgroundColor = `rgba(255,31,35,${opacity})`
line.querySelector("strong:last-of-type").style.backgroundColor = `rgba(27,31,255,${opacity})`
</script>

[null\*]: #note-on-null
