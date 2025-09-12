[**Oklahoma NG911 Toolkit**](../README.html) | [Adjustment](Adjustment.html) | [Comparison](Comparison.html) | [Enhancement](Enhancement.html) | [MSAG](MSAG.html) | [***Okprep***](Okprep.html) | [Submission](Submission.html) | [Validation](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [Topology Rules](Topology.html) | [Change Log](../ChangeLog.html) | [Error Glossary](ErrorGlossary.html)

# Okprep Toolset

## Toolset Credits
* Emma Baker, Oklahoma Department of Transportation
* Riley Baird, Oklahoma Department of Transportation

##### Last Revised:
June 15, 2022

## Abstract
The *Okprep* tools will map the feature class fields to a new feature class with the correct field names, types, lengths, and domains. The tools will also create a new user-named geodatabase in the folder location defined with a selected coordinate reference system and the correct domains from the domain files. These tools should be run to ensure the feature classes and geodatabase that will be submitted are formatted with the correct domains and field names.

## Tools

### 0 Create GDB

Script: [Okprep_recreateGDB.py](../Scripts/OKPrep_recreateGDB.py)

This tool creates a geodatabase containing the standard feature datasets and domains. Some or all feature classes may be provided, in which case each will be run through its respective field-mapping tool. If no feature classes are provided, the geodatabase and its feature datasets will not contain any feature classes, but the domains and feature dataset coordinate systems will still be set. There are also options to create blank feature classes when the feature class isn't provided **or** the feature class provided does not match the Oklahoma standards.

If you would like to maintain the current geodatabase and only need to update the Domains for the GDB, then refer to the [Fix GDB Domains](Adjustment.html#fix-gdb-domains) Tool in the Adjustment toolset.

#### Usage
1. Open this tool and set the parameters.
2. Execute this tool.

### 1 Address Field Map

Script: [Okprep_ADD.py](../Scripts/OKPrep_ADD.py)

This tool creates a new feature class with the correct field names field-mapped using the Address Points Feature Class fields defined by the User in the toolbox.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### 2 Road Field Map

Script: [Okprep_RDCL.py](../Scripts/OKPrep_RDCL.py)

This tool creates a new feature class with the correct field names field-mapped using the Road Centerline Feature Class fields defined by the User in the toolbox.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### 3 Discrepancy Agency Field Map

Script: [Okprep_PROV.py](../Scripts/OKPrep_PROV.py)

This tool creates a new feature class with the correct field names field-mapped using the Discrepancy Agency Boundary Feature Class fields defined by the User in the toolbox. **Note:** *The "discrepancy agency boundaries" have also been known in the past as "provisioning boundaries" and "authoritative boundaries".*

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### 4 PSAP Field Map

Script: [Okprep_PSAP.py](../Scripts/OKPrep_PSAP.py)

This tool creates a new feature class with the correct field names field-mapped using the PSAP Feature Class fields defined by the User in the toolbox.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### 5.1 ESB Law Field Map, 5.2 ESB Fire Field Map, and 5.3 ESB EMS Field Map

Script: [Okprep_ESB_EMS_Boundary.py](../Scripts/OKPrep_ESB_EMS_Boundary.py), [Okprep_ESB_FIRE_Boundary.py](../Scripts/OKPrep_ESB_FIRE_Boundary.py), [Okprep_ESB_LAW_Boundary.py](../Scripts/OKPrep_ESB_LAW_Boundary.py)

Each of these tools creates a new feature class with the correct field names field-mapped using the ESB Law, ESB Fire, and ESB EMS Feature Class fields, respectively, defined by the User in the toolbox.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### 5.4 Dissolve ESZ

Script: [Okprep_SplitESN.py](../Scripts/OKPrep_SplitESN.py)

This tool takes a single ESZ layer and creates separate feature classes for ESB Law, ESB Fire, and ESB EMS.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### 6 ESZ Field Map

Script: [Okprep_ESZ_Boundary.py](../Scripts/OKPrep_ESZ_Boundary.py)

This tool creates a new feature class with the correct field names field-mapped using the ESZ Feature Class fields defined by the User in the toolbox.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

### 7 Add Blank FCs

Script: [Okprep_addBlankFCs.py](../Scripts/OKPrep_addBlankFCs.py)

This tool adds blank standards-compliant feature classes to a standards-compliant geodatabase.

#### Usage
1. Open this tool and set the parameters, which includes the path to the NG911 geodatabase.
2. Execute this tool.

## Methodology

### Create Blank GDB
* For the Create GDB Tool, the function checks for an already existing GDB with the specified name. If it doesn't exist, then a new GDB is created with the specified name. The datasets `NG911` and `OptionalLayers` are then checked for and created with the specified projection. The tables for the GDB domains are then created. Looping through the list of provided values for the Feature Classes.

 * If the layer *is* provided, the layer is then sorted into the required dataset or the optional dataset. The appropriate field information is then retrieved along with determining the geometry type. A empty feature class is then created with the geometry, and the retrieved fields are then added to blank feature class. The function then tries to append the provided feature class to the empty feature class in the newly-created GDB.

 * If the layer *is not* provided and the "Create Blank FC" option is set to true, the geometry of the layer is determined, and a blank feature class with the appropriate fields is then created.

### Field Map
* The parameters for the tool are first assigned to the appropriate script parameters and then passed to the `create_feature_class` function.

* The field information is retrieved based on the inputs for the function. The function checks if the feature class already exists. If it does, the function appends "_new" to the end of the name.

* An empty feature class is first created and then the standard-compliant fields are added to the empty feature class. A field mapping between the user-specified fields and the standard-compliant fields is created. Once the field mapping is created, the function tries to append to data from the users feature class to the new standard-compliant feature class.  

## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
