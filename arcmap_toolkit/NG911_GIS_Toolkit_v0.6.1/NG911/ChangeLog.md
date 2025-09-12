[**Oklahoma NG911 Toolkit**](README.html) | [Adjustment] | [Comparison] | [Enhancement] | [MSAG] | [Okprep] | [Submission] | [Validation]

**Supplementary Documentation** | [Examples](Doc/Examples.html) | [Generate Fishbone Analysis Tool](Doc/FishboneAddressVerification.html) | [Topology Rules](Doc/Topology.html) | [Change Log](ChangeLog.html) | [Error Glossary](Doc/ErrorGlossary.html)

# **Oklahoma Next-Generation 9-1-1 Toolkit**

## **Credits**

### Original Codebase
Scripts written by Sherry Massey with Dickinson County, Kristen Jordan Koenig with DASC, and Kyle Gonterwitz and Dirk Talley with Kansas Department of Transportation

### Oklahoma Adaptation
Scripts written by Emma Baker and Riley Baird with the Oklahoma Department of Transportation (ODOT)

##### Last Revised:
June 17, 2022

## **Abstract**

This is a log of changes to the NG911 GIS Toolkit since Version 0.1.0.

## **Most Recent Change**

### **Version 0.6.1**
This update included:
* **CURRENTLY, MSAG and TN Tools do NOT function as intended.** Please wait for the next Standards update.
* Emergency fix for `Populate RCLMatch NO_MATCH`.
* All tools now print Toolkit version to console.

## **Previous Changes**

### **Version 0.6.0**
This update included:
* **CURRENTLY, MSAG and TN Tools do NOT function as intended.** Please wait for the next Standards update.
* Rewrote Check Topology validation check to better create and compress the errors into comprehensive messages using a new Methodology. Check Topology validation check is called in the `Check All Required` and `Verify Topology Exceptions` tools.
* Heavily modified and expanded the Documentation for the Tools.
* Added an Error Glossary to the Documentation.
* Confirmed `SUBMIT = 'Y'` usage in Validation checks.
* Confirmed methodology for Check RCLMatch and Geocompare Address Points.
* Full implementation of `FullName`/`FullAddr` throughout Toolkit and Documentation.

### **Version 0.5.0**
This update included:
* **CURRENTLY, MSAG and TN Tools do NOT function as intended.** Please wait for the next Standards update.
* Fixed `FullName`/`FullAddr` concatenations and usages
* Fixed Unicode compatibility issues
* Improved Legacy checks specifically to MSAG_CheckTNList.py.
* Finalized usage of `MSAGComm` fields in Geocompare Address Points Tool and other necessary usages
* Improved Street Name/Type/Direction parsing
* Removed null values of `MSAGComm` from appropriate feature classes before running MSAG or TN Tools.
* Added Fix `PreType` to Fix Street Type and Direction Tool.
* Replaced all usages of `Label` with `FullName`/`FullAddr` where appropriate and deleted Calculate Label Tool.
* Added Check Road FromLevel ToLevel Tool.
* Updated Documentation

### **Version 0.4.2**
This update included:
* Improved functionality within the MSAG NG911 Comparison Tool
* Deleted result tables at the beginning of sanity_check in the Validation Tool
* Fixed print statement issue with Comparison Tool
* Updated Documentation

### **Version 0.4.1**
This update included:
* Confirmed Standards-compliance of Toolkit Field and Domain data
* Added Spatial Reference check on the NG911 feature dataset
* Before `add_topology` function is called, any existing topology is deleted
* Fixed issues with Comparison Tool
* Updated Documentation

### **Version 0.4.0**
This update included:
* Updated Show Helps
* Updated Calculate Parity Enhancement Tool to handle null values
* Added feature class options to Fix Submit and Fix MSAGComm Spaces Adjustment Tools
* Created Calculate FullName and FullAddr Enhancement Tool
* Updated the AGENCYID_Domains.txt file (received June 8, 2021)
* Detected when Label, FullName, and FullAddr are too long for the field length
* Legacy options in the TN MSAG tools
* Created Change Log
* Implemented option to run an alternative Check Road ESN values requiring an Advanced license
* Updated Documentation

### **Version 0.3.2**
This update included:
* Copy-to-legacy field options in Fix Street Type and Direction Adjustment Tool
* Progress bars implementation
* Legacy option in the MSAG Comparison tool (testing still needed)
* Updated Documentation

### **Version 0.3.1**
This update included:
* Emergency fix to the 0 Create GDB tool in the Okprep toolset

### **Version 0.3.0**
This update included:
* Option to create individual blank feature classes in 0 Create GDB (Okprep tool)
* Created 7 Add Blank FCs to Okprep toolset
* Created 0 Check NENA ID Format to Validation toolset
* Updated Assign Unique NENA ID in Enhancement toolset
* Removed Fix GDB Domains from Adjustment toolset
* Created Order of Operations flowchart
* Update AGENCYID_Domains.txt with most recent Agency ID list (received April 28, 2021)
* Improved Show Help Documentation
* Updated Documentation

### **Version 0.2.1**
This update included:
* Created Fix TopoExcept tool to Adjustment toolset
* Created Fix GDB Domains tool to Adjustment toolset
* Created Check GDB Domains validation check to all appropriate Validation tools
* Removed uses of DASC_Communication table
* Fixed newline-issue in domain creation
* Improved user messaging
* Updated Documentation

### **Version 0.2.0**
This update included:
* Updated tool parameter names
* Updated Generate Fishbone Analysis tool in Enhancement toolset
* Removed domain/field file/folder parameters from Create GDB tool, Field Mapping tools, and Dissolve ESZ tool in Okprep toolset, and Fix Street Type and Direction tool in the Adjustment toolset
* Updated TOPOEXCEPT_Domains.txt and related in-code business
* Added County/Country warnings to Field Mapping tools in Okprep toolset
* Improved user messaging
* Updated Documentation

### **Version 0.1.1**
This update included:
* Updated Split ESN to Dissolve ESZ tool in Okprep toolset
* Improved user messaging
* Updated Documentation

### **Version 0.1.0**
This update included:
* Initial version release (all prior releases are by date and not included in the change log)
* Removed irrelevant files
* Updated Documentation

## **Disclaimer**

The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

[Okprep]: Doc/Okprep.html
[Adjustment]: Doc/Adjustment.html
[Comparison]: Doc/Comparison.html
[Enhancement]: Doc/Enhancement.html
[MSAG]: Doc/MSAG.html
[Submission]: Doc/Submission.html
[Validation]: Doc/Validation.html
[Generate Fishbone Analysis]: Doc/FishboneAddressVerification.html
[0 Create GDB]: Doc/Okprep.html#0-create-gdb
[6 Optional Clear Results Table]: Doc/Validation.html#6-clear-results-table-optional-
[8 Check All Required]: Doc/Validation.html#8-check-all-required
[Geocompare Address Points]: Doc/Enhancement.html#geocompare-address-points
[Populate RCLMatch NO_MATCH]: Doc/Enhancement.html#populate-rclmatch-no_match
[Kansas NG911 Toolkit]: https://github.com/kansasgis/NG911
[Examples]: Doc/Examples.html
