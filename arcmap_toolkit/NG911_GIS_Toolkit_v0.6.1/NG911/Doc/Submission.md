[**Oklahoma NG911 Toolkit**](../README.html) | [Adjustment](Adjustment.html) | [Comparison](Comparison.html) | [Enhancement](Enhancement.html) | [MSAG](MSAG.html) | [Okprep](Okprep.html) | [***Submission***](Submission.html) | [Validation](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [Topology Rules](Topology.html) | [Change Log](../ChangeLog.html) | [Error Glossary](ErrorGlossary.html)

# Submission Toolset

## Toolset Credits
* Emma Baker, Oklahoma Department of Transportation
* Riley Baird, Oklahoma Department of Transportation
* Adapted from code originally by Kristen Jordan Koenig et al., Kansas Data Access and Support Center

##### Last Revised:
June 15, 2022

## Abstract
The data submission tools perform a variety of validation checks against the NG911 Data Model template to determine if the data is ready for submission. Notice that the geodatabase is unready for submission will be given if any validation checks are failed.

## Tools

### Check Data and Zip

Script: [Submission_CheckAllAndZip.py](../Scripts/Submission_CheckAllAndZip.py)

Runs all required validation checks on the supplied geodatabase, and, if all checks are passed, the geodatabase is exported as a `.zip` file.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### GDB to Shapefiles

Script: [Conversion_GDBtoShapefile.py](../Scripts/Conversion_GDBtoShapefile.py)

Exports all feature classes in the supplied geodatabase's `NG911` feature dataset as shapefiles so that they can be distributed independently of a geodatabase.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### Zip NG911 Geodatabase

Script: [Conversion_ZipNG911Geodatabase.py](../Scripts/Conversion_ZipNG911Geodatabase.py)

Takes the supplied geodatabase and exports it as a `.zip` file.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
