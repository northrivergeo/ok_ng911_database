[**Oklahoma NG911 Toolkit**](../README.html) | [Adjustment](Adjustment.html) | [Comparison](Comparison.html) | [Enhancement](Enhancement.html) | [MSAG](MSAG.html) | [Okprep](Okprep.html) | [Submission](Submission.html) | [Validation](Validation.html)

**Supplementary Documentation** | [Examples](Examples.html) | [Generate Fishbone Analysis Tool](FishboneAddressVerification.html) | [***Topology Rules***](Topology.html) | [Change Log](../ChangeLog.html) | [Error Glossary](ErrorGlossary.html)

# NG911 Topology Rules

##### Last Revised:
June 15, 2022

## Abstract
The Oklahoma NG911 Standards require that a number of topological relationships exist within and among feature classes. This document discusses these rules, the validation of which is implemented in the Toolkit's *Check Topology* functionality.

An explanation of the different topology rules can be found [here](https://resources.arcgis.com/en/help/main/10.2/01mm/pdf/topology_rules_poster.pdf).

### Polygon Layer Rules

All polygon feature classes must individually conform to the rule:

* Must Not Overlap (Area)

### ESB and PSAP Layer Rules

The ESB_EMS_BOUNDARY, ESB_FIRE_BOUNDARY, ESB_LAW_BOUNDARY, and PSAP_BOUNDARY must individually conform to the rule:

* Must Not Have Gaps (Area)

### ROAD_CENTERLINE Layer Rules

The ROAD_CENTERLINE layer must conform to the following rules:

* Must Not Overlap (Line)
* *Must Not Have Dangles (Line)*
* Must Not Self-Overlap (Line)
* Must Not Self-Intersect (Line)
* Must Be Single Part (Line)

*NOTE: The rule(s) in italics may be marked as exceptions on a per-feature basis.*

### Rules Involving the DISCREPANCYAGENCY_BOUNDARY Layer

| Layer | Relationship to DISCREPANCYAGENCY_BOUNDARY |
| - | - |
| ADDRESS_POINT | Must Be Properly Inside  (Point-Area) |
| ROAD_CENTERLINE | *Must Be Inside (Line-Area)* |
| ESB_EMS_BOUNDARY | Must Cover Each Other (Area-Area) |
| ESB_FIRE_BOUNDARY | Must Cover Each Other (Area-Area) |
| ESB_LAW_BOUNDARY | Must Cover Each Other (Area-Area) |
| ESZ_BOUNDARY | Must Cover Each Other (Area-Area) |
| PSAP_BOUNDARY | Must Cover Each Other (Area-Area) |

*NOTE: The rule(s) in italics may be marked as exceptions on a per-feature basis.*

### Exceptions

The ROAD_CENTERLINE feature class includes the `TopoExcept` field, which allows the user to mark individual features as exempt from the *Must Not Have Dangles (Line)* and/or the *Must Be Inside (Line-Area)* (with DISCREPANCYAGENCY_BOUNDARY) rule. These exceptions will be accounted for when the [Verify Topology Exceptions] Validation tool is run.

[Verify Topology Exceptions]: Validation.html/#7-verify-topology-exceptions-optional-


## Support Contact
For issues or questions, please contact Emma Baker or Riley Baird with the Oklahoma Department of Transportation. Email Emma at <ebaker@odot.org> or Riley at <rbaird@odot.org>, and please include in the email which script you were running, any error messages, and a zipped copy of your geodatabase. Change the file extension from `zip` to `piz` so it gets through the email server. If there are further data transfer issues, contact Emma or Riley to make alternative data transfer arrangements.

If you have a domain issue to report, please email Emma Baker at <ebaker@odot.org>. Please indicate what type of domain the issue is with and the values needing corrections.

## Disclaimer
The Oklahoma NG9-1-1 GIS Toolbox is provided by the Oklahoma Geographic Information (GI) Council, Oklahoma 9-1-1 Management Authority, Oklahoma Department of Transportation (ODOT), Oklahoma Office of Geographic Information (OGI) , and associated contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall the Oklahoma GI Council, Oklahoma 9-1-1 Management Authority, ODOT, OGI, or associated contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
