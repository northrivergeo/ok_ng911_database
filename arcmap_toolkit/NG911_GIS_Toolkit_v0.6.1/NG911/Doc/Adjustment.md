[**Oklahoma NG911 Toolkit**](../README.html) | [***Adjustment***](Adjustment.html) | [Comparison](Comparison.html) | [Enhancement](Enhancement.html) | [MSAG](MSAG.html) | [Okprep](Okprep.html) | [Submission](Submission.html) | [Validation](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [Topology Rules](Topology.html) | [Change Log](../ChangeLog.html) | [Error Glossary](ErrorGlossary.html)

# Adjustment Toolset

## Toolset Credits
* Emma Baker, Oklahoma Department of Transportation
* Riley Baird, Oklahoma Department of Transportation
* Adapted from code originally by Kristen Jordan Koenig et al., Kansas Data Access and Support Center

##### Last Revised:
June 15, 2022

## Abstract
The adjustment tools exist to prepare data so that it passes all data validation checks prior to submission to the NG911 Portal. They fix minor errors and inconsistencies within the fields of certain feature classes.

## Tools

### Fix Domain Case

Script: [Adjustment_FixDomainCase.py](../Scripts/Adjustment_FixDomainCase.py)

This tool looks through the required layers for fields that are assigned domains and ensures that their values are cased (UPPER/lower) as specified in the domain file. If there is a mismatch, the field value is updated to reflect the value in the domain file. For example, any occurrences of `us` in `COUNTRY_L` will be edited to `US`. This tool depends upon data files in the *[Domains]* folder. Errors such as `Value us not in approved domain for field COUNTRY` in *FieldValuesCheckResults*, where the error is only due to the casing, should be corrected by running this tool.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### Fix MSAGComm Spaces

Script: [Adjustment_FixLeadingTrailingSpaces.py](../Scripts/Adjustment_FixLeadingTrailingSpaces.py)

This tool removes unnecessary (and error-causing) spaces at the beginning and end of `MSAGComm` field values.

#### Usage
1. Open this tool and set the parameters, including the path to the NG911 geodatabase.
2. Execute this tool.

### Fix Street Type and Direction

Script: [Adjustment_FixStreetType.py](../Scripts/Adjustment_FixStreetType.py)

This tool fixes the Street Type and Direction fields (`StreetType`, `PreType`, `PreDir`, and `SufDir`) to be correctly-formatted to current standards. It also optionally copies the current values of `PreDir`, `Street`, `StreetType`, and `SufDir` to `LgcyPreDir`, `LgcyStreet`, `LgcyType`, and `LgcySufDir`, respectively, before running the adjustment. If an address point feature class is provided, `LgcyAdd` can also optionally be calculated from `Address`, `BldgName`, `BldgUnit` and the four aforementioned legacy fields.

#### Usage
1. Open this tool and set the parameters, including the feature class and desired fields to adjust.
2. Execute this tool.

### Fix Submit

Script: [Adjustment_FixSubmit.py](../Scripts/Adjustment_FixSubmit.py)

The `SUBMIT` field is a required field, and therefore must not be blank. This tool updates blank `SUBMIT` field values to `Y`, indicating that a record is for submission. If a feature has a `SUBMIT` field value that is not either `Y` or `N`, this tool produces a warning.

#### Usage
1. Open this tool and set the parameters, including the path to the NG911 geodatabase.
2. Execute this tool.

### Fix TopoExcept

Script: [Adjustment_FixTopoExcept.py](../Scripts/Adjustment_FixTopoExcept.py)

This tool will convert the `TopoExcept` field from an older schema to the standards-compliant schema. Optional functionality includes filling null and blank values to `NOT_EXCEPTION` and updating the domain in the GDB for the `TopoExcept` field.

#### Usage
1. Open this tool and set the parameters, including the path to the Road Centerline feature class, the current values for the `TopoExcept` field, checkbox to fill nulls/blanks, and the option to update the domain in the GDB.
2. Execute this tool.

## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

[Domains]: ../Domains
[8 Check All Required]: Validation.html#8-check-all-required
