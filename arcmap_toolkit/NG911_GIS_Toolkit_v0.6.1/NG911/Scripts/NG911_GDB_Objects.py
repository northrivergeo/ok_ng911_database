#-------------------------------------------------------------------------------
# Name:        NG911_GDB_Objects
# Purpose:     Objects representing NG911 fields
#
# Author:      Kristen (KS), E Baker (OK), R Baird (OK)
#
# Created:     April 13, 2016
# Modified:	   January 6, 2022
#-------------------------------------------------------------------------------
# This is a class used represent the NG911 geodatabase
from os.path import join, basename
import arcpy

try:
    from typing import List, Union, Dict
except:
    pass

class NG911FeatureClassObject:
    """
    Base class from which all NG911 feature-class-representing classes inherit. Its attributes represent the names of
    the fields shared by all such feature classes.

    Attributes
    ----------
    ...

    Methods
    -------
    verify_field_not_none(field)
        Returns True if the given field name of the instance is not None; returns False if it is.
    verify_required_fields_not_none(get_none_fields=False, raise_on_none=False)
        Determines whether or not any of an instance's attributes given in its REQUIRED_FIELDS attribute are equal to
        None. By default, this returns True if none of those attributes are equal to None or returns False if one or
        more of these attributes are equal to None.


    """
    def __init__(self, u_DiscrpAgID=None, u_Agency_ID=None, u_RevDate=None, u_EFF_DATE=None, u_EXP_DATE=None, u_UNIQUEID=None, u_RevEditor=None, u_SUBMIT=None, u_Comment=None, u_GDB_VERSION=None, u_REQUIRED_FIELDS=None, u_FIELDS_WITH_DOMAINS=None, u_FIELD_MAP=None):
        # type: (Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[Dict[str, str], None], Union[str, None]) -> NG911FeatureClassObject

        self.DiscrpAgID = u_DiscrpAgID
        self.Agency_ID = u_Agency_ID
        self.RevDate = u_RevDate
        self.EFF_DATE = u_EFF_DATE
        self.EXP_DATE = u_EXP_DATE
        self.UNIQUEID = u_UNIQUEID
        self.RevEditor = u_RevEditor
        self.SUBMIT = u_SUBMIT
        self.Comment = u_Comment
        self.GDB_VERSION = u_GDB_VERSION
        self.REQUIRED_FIELDS = u_REQUIRED_FIELDS
        self.FIELDS_WITH_DOMAINS = u_FIELDS_WITH_DOMAINS
        self.FIELD_MAP = u_FIELD_MAP

    def verify_field_not_none(self, field):
        # type: (str) -> bool
        if getattr(self, field) is not None:
            return True
        else:
            return False

    def verify_required_fields_not_none(self, get_none_fields=False, raise_on_none=False):
        # type: (bool, bool) -> Union[List, bool]
        none_fields = []
        for field in self.REQUIRED_FIELDS:
            if self.verify_field_not_none(field) is False:
                none_fields.append(field)
        if len(none_fields) is not 0 and raise_on_none is True:
            none_fields_string = str.join(", ", none_fields)
            raise "Fields %s of %s must not be None." % (none_fields_string, self.__class__)
        if get_none_fields is True:
            return none_fields
        elif len(none_fields) is 0:
            return True
        else:
            return False



class NG911CheckResultsObject:
    def __init__(self):
        pass

class NG911_RoadCenterline_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_Agency_ID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_NGUID_RDCL, u_COUNTRY_L, u_COUNTRY_R, u_STATE_L, u_STATE_R,
                 u_COUNTY_L, u_COUNTY_R, u_MUNI_L, u_MUNI_R, u_Add_L_Pre, u_Add_R_Pre, u_Add_L_From, u_Add_L_To, u_Add_R_From,
                 u_Add_R_To, u_PARITY_L, u_PARITY_R, u_POSTCO_L, u_POSTCO_R, u_ZIP_L, u_ZIP_R, u_ESN_L, u_ESN_R,
                 u_MSAGCO_L, u_MSAGCO_R, u_PreMod, u_PreDir, u_PreType, u_PreTypeSep, u_Street, u_StreetType, u_SufDir, u_SufMod, u_SPDLIMIT, u_ONEWAY,
                 u_RDCLASS, u_RevEditor, u_LABEL, u_ELEV_F, u_ELEV_T, u_SURFACE, u_BoundLane,
                 u_TopoExcept, u_SUBMIT, u_Comment, u_UNINC_L, u_UNINC_R, u_GEOMSAGL,
                 u_GEOMSAGR, u_NbrhdCommL, u_NbrhdCommR, u_Zipcode4_L, u_Zipcode4_R, u_InitiSrce, u_InitiDate,
                 u_AltStName1, u_AltStName2, u_AltStName3, u_LgcyPreDir, u_LgcyStreet, u_LgcyType, u_LgcySufDir,
                 u_RoadLength, u_DriveTime, u_DeadEnd, u_Lanes, u_Toll, u_LtdAccess, u_Valid_L, u_Valid_R, u_FullName, u_PSAP_L, u_PSAP_R,
                 u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_Agency_ID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_NGUID_RDCL, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.SEGID = u_NGUID_RDCL
        self.COUNTRY_L = u_COUNTRY_L
        self.COUNTRY_R = u_COUNTRY_R
        self.STATE_L = u_STATE_L
        self.STATE_R = u_STATE_R
        self.COUNTY_L = u_COUNTY_L
        self.COUNTY_R = u_COUNTY_R
        self.MUNI_L = u_MUNI_L
        self.MUNI_R = u_MUNI_R
        self.Add_L_Pre = u_Add_L_Pre
        self.Add_R_Pre = u_Add_R_Pre
        self.Add_L_From = u_Add_L_From
        self.Add_L_To = u_Add_L_To
        self.Add_R_From = u_Add_R_From
        self.Add_R_To = u_Add_R_To
        self.PARITY_L = u_PARITY_L
        self.PARITY_R = u_PARITY_R
        self.POSTCO_L = u_POSTCO_L
        self.POSTCO_R = u_POSTCO_R
        self.ZIP_L = u_ZIP_L
        self.ZIP_R = u_ZIP_R
        self.ESN_L = u_ESN_L
        self.ESN_R = u_ESN_R
        self.MSAGCO_L = u_MSAGCO_L
        self.MSAGCO_R = u_MSAGCO_R
        self.PreMod = u_PreMod
        self.PreDir = u_PreDir
        self.PreType = u_PreType
        self.PreTypeSep = u_PreTypeSep
        self.Street = u_Street
        self.StreetType = u_StreetType
        self.SufDir = u_SufDir
        self.SufMod = u_SufMod
        self.SPDLIMIT = u_SPDLIMIT
        self.ONEWAY = u_ONEWAY
        self.RDCLASS = u_RDCLASS
        self.LABEL = u_LABEL
        self.ELEV_F = u_ELEV_F
        self.ELEV_T = u_ELEV_T
        self.SURFACE = u_SURFACE
        self.BoundLane = u_BoundLane
        self.TopoExcept = u_TopoExcept
        self.UNINC_L = u_UNINC_L
        self.UNINC_R = u_UNINC_R
        self.GEOMSAGL = u_GEOMSAGL
        self.GEOMSAGR = u_GEOMSAGR
        self.NbrhdCommL = u_NbrhdCommL
        self.NbrhdCommR = u_NbrhdCommR
        self.Zipcode4_L = u_Zipcode4_L
        self.Zipcode4_R = u_Zipcode4_R
        self.InitiSrce = u_InitiSrce
        self.InitiDate = u_InitiDate
        self.AltStName1 = u_AltStName1
        self.AltStName2 = u_AltStName2
        self.AltStName3 = u_AltStName3
        self.LgcyPreDir = u_LgcyPreDir
        self.LgcyStreet = u_LgcyStreet
        self.LgcyType = u_LgcyType
        self.LgcySufDir = u_LgcySufDir
        self.RoadLength = u_RoadLength
        self.DriveTime = u_DriveTime
        self.DeadEnd = u_DeadEnd
        self.Lanes = u_Lanes
        self.Toll = u_Toll
        self.LtdAccess = u_LtdAccess
        self.Valid_L = u_Valid_L
        self.Valid_R = u_Valid_R
        self.FullName = u_FullName
        self.PSAP_L = u_PSAP_L
        self.PSAP_R = u_PSAP_R
        self.LABEL_FIELDS = [self.LABEL, self.PreDir, self.PreTypeSep, self.Street, self.StreetType, self.SufDir, self.SufMod]
        self.FULLNAME_FIELDS = [self.FullName, self.PreDir, self.PreMod, self.PreType, self.PreTypeSep, self.Street, self.StreetType, self.SufDir,
                                self.SufMod]  # type: List[str]
        self.LGCYNAME_FIELDS = [None, self.LgcyPreDir, self.PreMod, self.PreType, self.PreTypeSep, self.LgcyStreet, self.LgcyType, self.LgcySufDir,
                                self.SufMod]  # type: List[str]

        # Required
        reqFields = [self.DiscrpAgID, self.Agency_ID, self.RevDate, self.UNIQUEID, self.COUNTRY_L, self.COUNTRY_R, self.STATE_L, self.STATE_R, self.COUNTY_L,
                     self.COUNTY_R, self.MUNI_L, self.MUNI_R, self.Add_L_From, self.Add_L_To, self.Add_R_From, self.Add_R_To,
                     self.PARITY_L, self.PARITY_R, self.Street, self.RevEditor, self.TopoExcept, self.InitiSrce, self.InitiDate, self.FullName,
                     self.SUBMIT, self.PSAP_L, self.PSAP_R, self.GEOMSAGL, self.GEOMSAGR]
        # ???
        fieldMap = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.STATE_L, self.STATE_R, self.COUNTY_L, self.COUNTY_R, self.MUNI_L,
                    self.MUNI_R, self.Add_L_From, self.Add_L_To, self.Add_R_From, self.Add_R_To, self.PARITY_L, self.PARITY_R, self.POSTCO_L, self.POSTCO_R, self.ZIP_L, self.ZIP_R,
                    self.ESN_L, self.ESN_R, self.MSAGCO_L, self.MSAGCO_R, self.PreDir, self.PreTypeSep, self.Street, self.StreetType, self.SufDir, self.SufMod, self.SPDLIMIT, self.ONEWAY, self.RDCLASS,
                    self.RevEditor, self.LABEL, self.ELEV_F, self.ELEV_T, self.SURFACE, self.BoundLane, self.TopoExcept, self.SUBMIT,
                    self.Comment, self.UNINC_L, self.UNINC_R]
        # Domains, updated to OK Domains
        fieldsWithDomains = {self.DiscrpAgID: "AGENCYID", self.Agency_ID: "AGENCYID", self.COUNTRY_L: "COUNTRY", self.COUNTRY_R: "COUNTRY", self.STATE_L: "STATE", self.STATE_R: "STATE", self.COUNTY_L: "COUNTY", self.COUNTY_R: "COUNTY",
                             self.PARITY_L: "PARITY", self.PARITY_R: "PARITY", self.PreTypeSep: "SEPARATOR",
                             self.PreDir: "DIRECTION", self.StreetType: "STREETTYPE", self.SufDir: "DIRECTION", self.ONEWAY: "ONEWAY",
                             self.RDCLASS: "ROADCLASS", self.LgcyPreDir: "LGCYDIRECTION", self.LgcyType: "LGCYSTREETTYPE",
                             self.LgcySufDir: "LGCYDIRECTION", self.DeadEnd: "YESNO", self.Lanes: "NUMBER", self.Toll: "YESNO",
                             self.LtdAccess: "YESNO", self.Valid_L: "YESNO", self.Valid_R: "YESNO", self.PreType: "STREETTYPE",
                             self.ELEV_F: "LEVEL", self.ELEV_T: "LEVEL", self.BoundLane: "DIRECTION",
                             self.GEOMSAGL: "YESNO", self.GEOMSAGR: "YESNO", self.SUBMIT: "YESNO", self.TopoExcept: "TOPOEXCEPT"}
        # Duplicates
        frequencyFields = self.FULLNAME_FIELDS + [self.STATE_L, self.STATE_R, self.COUNTY_L, self.COUNTY_R, self.MUNI_L, self.MUNI_R, self.COUNTY_L, self.COUNTY_R, self.Add_L_From, self.Add_L_To, self.Add_R_From, self.Add_R_To,
                           self.PARITY_L, self.PARITY_R, self.POSTCO_L, self.POSTCO_R, self.ZIP_L, self.ZIP_R, self.ESN_L, self.ESN_R, self.MSAGCO_L, self.MSAGCO_R,
                           self.SPDLIMIT, self.ONEWAY, self.RDCLASS, self.ELEV_F, self.ELEV_T,
                           self.SURFACE, self.BoundLane]

        setList = [reqFields, fieldMap, fieldsWithDomains, frequencyFields]

        # add additional field values and domains for new 2.1 fields
        # if self.GDB_VERSION == "21":
        #     for sL in setList:
        #         for rf in [self.AUTH_L, self.AUTH_R, self.GEOMSAGL, self.GEOMSAGR]:
        #             if type(sL) == list:
        #                 sL.append(rf)
        #             elif type(sL) == dict:
        #                 sL[rf] = "YESNO"

        self.REQUIRED_FIELDS = reqFields
        self.FIELD_MAP = fieldMap
        self.FIELDS_WITH_DOMAINS = fieldsWithDomains
        self.FREQUENCY_FIELDS = frequencyFields
        self.FREQUENCY_FIELDS_STRING = ";".join(self.FREQUENCY_FIELDS)

# Modified to OK fields
def getDefaultNG911RoadCenterlineObject(gdb_version):
    NG911_RoadCenterline_Default = NG911_RoadCenterline_Object("DiscrpAgID", "Agency_ID", "RevDate", "EffectDate", "ExpireDate", "NGUID_RDCL","Country_L", "Country_R", "State_L", "State_R", "County_L", "County_R", "City_L",
                                                               "City_R", "Add_L_Pre", "Add_R_Pre", "Add_L_From", "Add_L_To", "Add_R_From", "Add_R_To", "Parity_L", "Parity_R", "PostComm_L", "PostComm_R", "Zipcode_L", "Zipcode_R",
                                                               "Esn_L", "Esn_R", "MSAGComm_L", "MSAGComm_R", "PreMod", "PreDir", "PreType", "PreTypeSep", "Street", "StreetType", "SufDir", "SufMod", "SpeedLimit", "Oneway", "RoadClass",
                                                               "RevEditor", "Label", "FromLevel", "ToLevel", "Surface", "BoundLane", "TopoExcept", "SUBMIT",
                                                               "Comment", "UnincCommL", "UnincCommR", "GeoMSAG_L", "GeoMSAG_R", "NbrhdCommL", "NbrhdCommR",
                                                               "Zipcode4_L", "Zipcode4_R", "InitiSrce", "InitiDate","AltStName1", "AltStName2", "AltStName3", "LgcyPreDir",
                                                               "LgcyStreet","LgcyType", "LgcySufDir", "RoadLength","DriveTime", "DeadEnd", "Lanes", "Toll","LtdAccess",
                                                               "Valid_L", "Valid_R", "FullName", "PSAP_L", "PSAP_R", gdb_version)

    return NG911_RoadCenterline_Default

# For Road Alias, From (l & R) and To (L & R) need to remain null for Oklahoma roadways
class NG911_RoadAlias_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ALIASID, u_SEGID, u_A_PRD, u_A_STP, u_A_RD,
                 u_A_STS, u_A_POD, u_A_POM, u_A_L_FROM, u_A_L_TO, u_A_R_FROM, u_A_R_TO, u_LABEL, u_RevEditor, u_SUBMIT,
                 u_Comment, u_KSSEGID, u_NGKSALIASID, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ALIASID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.ALIASID = u_ALIASID
        self.SEGID = u_SEGID
        self.UNIQUEID = self.ALIASID
        self.A_PRD = u_A_PRD
        self.A_STP = u_A_STP
        self.A_RD = u_A_RD
        self.A_STS = u_A_STS
        self.A_POD = u_A_POD
        self.A_POM = u_A_POM
        self.A_L_FROM = u_A_L_FROM
        self.A_L_TO = u_A_L_TO
        self.A_R_FROM = u_A_R_FROM
        self.A_R_TO = u_A_R_TO
        self.LABEL = u_LABEL
        self.KSSEGID = u_KSSEGID
        self.NGKSALIASID = u_NGKSALIASID
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.UNIQUEID, self.SEGID, self.LABEL, self.RevEditor]
        self.FIELDS_WITH_DOMAINS = {self.DiscrpAgID: "DiscrpAgID", self.A_PRD: "PreDir", self.A_STS: "StreetType",
                                    self.A_POD: "SufDir", self.SUBMIT: "YN"}
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.SEGID, self.A_PRD,
                          self.A_STP, self.A_RD, self.A_STS, self.A_POD, self.A_POM, self.A_L_FROM, self.A_L_TO,
                          self.A_R_FROM, self.A_R_TO, self.LABEL, self.RevEditor, self.SUBMIT, self.Comment]


def getDefaultNG911RoadAliasObject(gdb_version):

    NG911_RoadAlias_Default = NG911_RoadAlias_Object("DiscrpAgID", "RevDate", "EFF_DATE", "EXP_DATE", "NGALIASID", "NGSEGID", "A_PRD", "A_STP", "A_RD", "A_STS", "A_POD",
                                                     "A_POM", "A_L_FROM", "A_L_TO", "A_R_FROM", "A_R_TO", "Label", "RevEditor", "SUBMIT", "Comment", "NGKSSEGID", "NGKSALIASID", gdb_version)

    return NG911_RoadAlias_Default


class NG911_Address_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_Agency_ID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_NGUID_ADD, u_COUNTRY, u_STATE, u_COUNTY, u_MUNI,
                 u_Address, u_AddSuf, u_PreDir, u_PreTypeSep, u_Street, u_StreetType, u_SufDir, u_SufMod, u_ESN, u_MSAGCO, u_POSTCO, u_ZIP, u_ZIP4, u_BldgName,
                 u_FLR, u_UNIT, u_ROOM, u_SEAT, u_LandmkName, u_AddtnlLoc, u_PlaceType, u_LONG, u_LAT, u_ELEV, u_LABEL, u_RevEditor,
                 u_MILEPOST, u_ADDURI, u_UNINC, u_SUBMIT, u_Comment, u_PreMod, u_RCLMatch,
                 u_RCLSide, u_NbrdhdComm, u_GrpQuarter, u_OccupTime, u_StrmSheltr, u_Basement, u_LgcyAdd,
                 u_LgcyPreDir, u_LgcyStreet, u_LgcyType, u_LgcySufDir, u_FullAddr, u_FullName, u_AddPre, u_PreType,
                 u_PSAP, u_Placement, u_InitiSrce, u_InitiDate, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_Agency_ID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_NGUID_ADD, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.ADDID = u_NGUID_ADD
        self.COUNTRY = u_COUNTRY
        self.STATE = u_STATE
        self.COUNTY = u_COUNTY
        self.MUNI = u_MUNI
        self.Address = u_Address
        self.AddSuf = u_AddSuf
        self.PreDir = u_PreDir
        self.PreTypeSep = u_PreTypeSep
        self.Street = u_Street
        self.StreetType = u_StreetType
        self.SufDir = u_SufDir
        self.SufMod = u_SufMod
        self.ESN = u_ESN
        self.MSAGCO = u_MSAGCO
        self.POSTCO = u_POSTCO
        self.ZIP = u_ZIP
        self.ZIP4 = u_ZIP4
        self.BldgName = u_BldgName
        self.FLR = u_FLR
        self.UNIT = u_UNIT
        self.ROOM = u_ROOM
        self.SEAT = u_SEAT
        self.LandmkName = u_LandmkName
        self.AddtnlLoc = u_AddtnlLoc
        self.PlaceType = u_PlaceType
        self.LONG = u_LONG
        self.X = self.LONG
        self.LAT = u_LAT
        self.Y = self.LAT
        self.ELEV = u_ELEV
        self.LABEL = u_LABEL
        self.MILEPOST = u_MILEPOST
        self.ADDURI = u_ADDURI
        self.UNINC = u_UNINC
        self.PreMod = u_PreMod
        self.RCLMatch = u_RCLMatch
        self.RCLSide = u_RCLSide
        self.NbrdhdComm = u_NbrdhdComm
        self.GrpQuarter = u_GrpQuarter
        self.OccupTime = u_OccupTime
        self.StrmSheltr = u_StrmSheltr
        self.Basement = u_Basement
        self.LgcyAdd = u_LgcyAdd
        self.LgcyPreDir = u_LgcyPreDir
        self.LgcyStreet = u_LgcyStreet
        self.LgcyType = u_LgcyType
        self.LgcySufDir = u_LgcySufDir
        self.FullAddr = u_FullAddr
        self.FullName = u_FullName
        self.AddPre = u_AddPre
        self.PreType = u_PreType
        self.PSAP = u_PSAP
        self.Placement = u_Placement
        self.InitiSrce = u_InitiSrce
        self.InitiDate = u_InitiDate
        self.LABEL_FIELDS = [self.LABEL, self.Address, self.AddSuf, self.PreDir, self.PreTypeSep, self.Street, self.StreetType, self.SufDir, self.SufMod, self.BldgName,
                             self.FLR, self.UNIT, self.ROOM, self.SEAT]
        self.FULLNAME_FIELDS = [self.FullName, self.PreDir, self.PreMod, self.PreType, self.PreTypeSep, self.Street, self.StreetType, self.SufDir,
                                self.SufMod]  # type: List[str]
        self.FULLADDR_FIELDS = [self.FullAddr, self.AddPre, self.Address, self.AddSuf, self.PreDir, self.PreMod, self.PreType, self.PreTypeSep, self.Street, self.StreetType, self.SufDir, self.SufMod, self.BldgName, self.UNIT]  # type: List[str]
        self.LGCYNAME_FIELDS = [None, self.LgcyPreDir, self.PreMod, self.PreType, self.PreTypeSep, self.LgcyStreet, self.LgcyType, self.LgcySufDir,
                                self.SufMod]  # type: List[str]
        self.LGCYADDR_FIELDS = [self.LgcyAdd, self.AddPre, self.Address, self.AddSuf, self.LgcyPreDir, self.PreMod, self.PreType, self.PreTypeSep, self.LgcyStreet, self.LgcyType, self.LgcySufDir,
                                self.SufMod, self.BldgName, self.UNIT]  # type: List[str]
        self.GEOCODE_LABEL_FIELDS = [self.Address, self.PreDir, self.PreTypeSep, self.Street, self.StreetType, self.SufDir, self.SufMod]

        # Required Fields
        reqFields = [self.DiscrpAgID, self.MUNI, self.RevDate, self.UNIQUEID, self.COUNTRY, self.STATE, self.COUNTY, self.RevEditor, self.SUBMIT, self.RCLMatch, self.RCLSide, self.Agency_ID, self.PSAP, self.InitiSrce, self.InitiDate]
        # Mapped Fields ???
        fieldMap = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.STATE, self.COUNTY, self.MUNI, self.Address, self.AddSuf, self.PreDir, self.PreTypeSep,
                    self.Street, self.StreetType, self.SufDir, self.SufMod, self.ESN, self.MSAGCO, self.POSTCO, self.ZIP, self.ZIP4, self.BldgName, self.FLR, self.UNIT, self.ROOM, self.SEAT, self.LandmkName,
                    self.AddtnlLoc, self.PlaceType, self.LONG, self.LAT, self.ELEV, self.LABEL, self.RevEditor,
                    self.MILEPOST, self.ADDURI,
                    self.UNINC, self.SUBMIT, self.Comment]
        # Domains, replaced with OK Domains
        fieldsWithDomains = {self.DiscrpAgID: "AGENCYID", self.COUNTRY: "COUNTRY", self.STATE: "STATE", self.COUNTY: "COUNTY", self.PreDir: "DIRECTION",
                             self.StreetType: "STREETTYPE", self.SufDir: "DIRECTION",
                             self.PlaceType: "PLACETYPE", self.GrpQuarter: "YESNO", self.Basement: "YESNO",
                             self.LgcyPreDir: "LGCYDIRECTION", self.LgcyType: "LGCYSTREETTYPE",
                             self.LgcySufDir: "LGCYDIRECTION", self.PreType: "STREETTYPE", self.PreTypeSep: "SEPARATOR",
                             self.StrmSheltr: "STORMSHELTER", self.Placement: "PLACEMENT", self.SUBMIT: "YESNO", self.RCLSide: "RCLSIDE"}
        #Frequency Fields
        frequencyFields = self.FULLADDR_FIELDS + [self.FLR, self.ROOM,
                           self.SEAT, self.AddtnlLoc, self.MUNI, self.COUNTY, self.STATE, self.COUNTRY,
                           self.MSAGCO]

        setList = [reqFields, fieldMap, frequencyFields]

        # if self.GDB_VERSION == "21":
            # only geomsag has a domain of the new 2.1 fields
            # fieldsWithDomains[self.GEOMSAG] = "YN"

        ##### BEGIN unindent with removal of version conditional #####
        fieldsWithDomains[self.RCLSide] = "RCLSide"

        for sL in setList:
            # for rf in [self.RCLMatch, self.GEOMSAG, self.RCLSide]:
            for rf in [self.RCLMatch, self.RCLSide]:
                sL.append(rf)
        ##### END unindent with removal of version conditional #####

        self.REQUIRED_FIELDS = reqFields
        self.FIELD_MAP = fieldMap
        self.FIELDS_WITH_DOMAINS = fieldsWithDomains
        self.FREQUENCY_FIELDS = frequencyFields
        self.FREQUENCY_FIELDS_STRING = ";".join(self.FREQUENCY_FIELDS)

# Modified to OK fields
def getDefaultNG911AddressObject(gdb_version):
    # type: (str) -> NG911_Address_Object

    NG911_Address_Default = NG911_Address_Object("DiscrpAgID", "Agency_ID", "RevDate", "EffectDate", "ExpireDate", "NGUID_ADD", "Country", "State", "County", "City", "Address", "AddSuf", "PreDir", "PreTypeSep",
                                                  "Street", "StreetType", "SufDir", "SufMod", "ESN", "MSAGComm", "PostComm", "Zipcode", "Zipcode4", "BldgName", "Floor", "BldgUnit", "Room", "Seat", "LandmkName",
                                                  "AddtnlLoc", "PlaceType", "Longitude", "Latitude", "Elevation", "Label", "RevEditor",
                                                  "MilePost", "AddDataURI",
                                                  "UnincComm", "SUBMIT", "Comment", "PreMod", "RCLMatch",
                                                  "RCLSide", "NbrhdComm", "GrpQuarter", "OccupTime", "StrmSheltr", "Basement", "LgcyAdd",
                                                  "LgcyPreDir", "LgcyStreet", "LgcyType", "LgcySufDir", "FullAddr", "FullName","AddPre", "PreType", "PSAP",
                                                  "Placement", "InitiSrce", "InitiDate", gdb_version)

    return NG911_Address_Default


class NG911_FieldValuesCheckResults_Object(NG911CheckResultsObject):

    def __init__(self, u_DATEFLAGGED, u_DESCRIPTION, u_LAYER, u_FIELD, u_FEATUREID, u_CHECK):
        # type: (str, str, str, str, str, str) -> None

        NG911CheckResultsObject.__init__(self)
        self.DATEFLAGGED = u_DATEFLAGGED
        self.DESCRIPTION = u_DESCRIPTION
        self.LAYER = u_LAYER
        self.FIELD = u_FIELD
        self.FEATUREID = u_FEATUREID
        self.CHECK = u_CHECK


def getDefaultNG911FieldValuesCheckResultsObject():

    NG911_FieldValuesCheckResults_Default = NG911_FieldValuesCheckResults_Object("DATEFLAGGED", "DESCRIPTION", "LAYER", "FIELD", "FEATUREID", "CHECK")

    return NG911_FieldValuesCheckResults_Default


class NG911_TemplateCheckResults_Object(NG911CheckResultsObject):

    def __init__(self, u_DATEFLAGGED, u_DESCRIPTION, u_CATEGORY, u_CHECK):
        # type: (str, str, str, str) -> None

        NG911CheckResultsObject.__init__(self)
        self.DATEFLAGGED = u_DATEFLAGGED
        self.DESCRIPTION = u_DESCRIPTION
        self.CATEGORY = u_CATEGORY
        self.CHECK = u_CHECK


def getDefaultNG911TemplateCheckResultsObject():

    NG911_TemplateCheckResults_Default = NG911_TemplateCheckResults_Object("DATEFLAGGED", "DESCRIPTION", "CATEGORY", "CHECK")

    return NG911_TemplateCheckResults_Default


class NG911_ESB_Object(NG911FeatureClassObject):

    # def __init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ESBID, u_STATE, u_Agency_ID, u_SERV_NUM,
                 # u_DISPLAY, u_ESB_TYPE, u_LAW, u_FIRE, u_EMS, u_RevEditor, u_PSAP, u_SUBMIT, u_Comment, u_gdb_version):
    def __init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ESBID, u_Agency_ID, u_RevEditor,
                 u_SUBMIT, u_Comment, u_Agency, u_Avcard_URI, u_ServiceURN, u_ServiceURI, u_ServiceNum, u_Country,
                 u_STATE, u_InitiSrce, u_InitiDate, u_gdb_version):
        # type: (NG911_ESB_Object, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str) -> None

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_Agency_ID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ESBID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)

        self.ESBID = u_ESBID
        self.AGENCYID = u_Agency_ID
        self.Agency = u_Agency
        self.Avcard_URI = u_Avcard_URI
        self.ServiceURN = u_ServiceURN
        self.ServiceURI = u_ServiceURI
        self.ServiceNum = u_ServiceNum
        self.Country = u_Country
        self.STATE = u_STATE
        self.InitiSrce = u_InitiSrce
        self.InitiDate = u_InitiDate
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.STATE, self.AGENCYID,
                                self.RevEditor, self.SUBMIT, self.Agency, self.Avcard_URI, self.ServiceURN, self.ServiceURI, self.Country, self.InitiSrce, self.InitiDate]
        self.FIELDS_WITH_DOMAINS = {self.Country: "COUNTRY", self.STATE: "STATE", self.SUBMIT: "YESNO", self.DiscrpAgID: "AGENCYID", self.AGENCYID: "AGENCYID", self.ServiceURN: "SERVICEURN"}
        # self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.STATE, self.AGENCYID,
                          # self.SERV_NUM, self.DISPLAY, self.ESB_TYPE, self.LAW, self.FIRE, self.EMS, self.RevEditor, self.PSAP,
                          # self.SUBMIT, self.Comment]
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.STATE, self.AGENCYID,
                          self.ServiceNum, self.RevEditor, self.SUBMIT, self.Comment]

# Modified to OK fields
# def getDefaultNG911ESBObject(gdb_version):
#     raise("Call for ESB Law, Fire, or EMS object instead!")
    # NG911_ESB_Default = NG911_ESB_Object("DiscrpAgID", "RevDate", "EffectDate", "ExpireDate", "NGUID_ESB", "STATE", "Agency_ID", "SERV_NUM", "DISPLAY", "ESB_TYPE",
    #                                      "LAW", "FIRE", "EMS", "RevEditor", "PSAP", "SUBMIT", "Comment", gdb_version)
    #
    # return NG911_ESB_Default

def getDefaultNG911ESBLawObject(gdb_version):
    NG911_ESB_Default = NG911_ESB_Object("DiscrpAgID", "RevDate", "EffectDate", "ExpireDate", "NGUID_LAW", "Agency_ID",
                                        "RevEditor", "SUBMIT", "Comment", "Agency", "Avcard_URI", "ServiceURN",
                                        "ServiceURI", "ServiceNum", "Country", "State", "InitiSrce", "InitiDate", gdb_version)

    return NG911_ESB_Default

def getDefaultNG911ESBFireObject(gdb_version):
    NG911_ESB_Default = NG911_ESB_Object("DiscrpAgID", "RevDate", "EffectDate", "ExpireDate", "NGUID_FIRE", "Agency_ID",
                                        "RevEditor", "SUBMIT", "Comment", "Agency", "Avcard_URI", "ServiceURN",
                                        "ServiceURI", "ServiceNum", "Country", "State", "InitiSrce", "InitiDate", gdb_version)

    return NG911_ESB_Default

def getDefaultNG911ESBEMSObject(gdb_version):
    NG911_ESB_Default = NG911_ESB_Object("DiscrpAgID", "RevDate", "EffectDate", "ExpireDate", "NGUID_EMS", "Agency_ID",
                                        "RevEditor", "SUBMIT", "Comment", "Agency", "Avcard_URI", "ServiceURN",
                                        "ServiceURI", "ServiceNum", "Country", "State", "InitiSrce", "InitiDate", gdb_version)

    return NG911_ESB_Default


class NG911_ESZ_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ESZID, u_COUNTRY, u_STATE, u_Agency, u_AGENCYID,
                 u_ESN, u_ESZ, u_RevEditor, u_SUBMIT, u_Comment, u_Avcard_URI,  # u_ServiceURN, u_ServiceURI,
                 u_ServiceNum, u_InitiSrce, u_InitiDate, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_AGENCYID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ESZID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.ESZID = u_ESZID
        self.COUNTRY = u_COUNTRY
        self.STATE = u_STATE
        self.Agency = u_Agency
        self.AGENCYID = u_AGENCYID
        self.ESN = u_ESN
        self.ESZ = u_ESZ
        self.Avcard_URI = u_Avcard_URI
        # self.ServiceURN = u_ServiceURN
        # self.ServiceURI = u_ServiceURI
        self.ServiceNum = u_ServiceNum
        self.InitiSrce = u_InitiSrce
        self.InitiDate = u_InitiDate
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.STATE, self.AGENCYID,
                                self.RevEditor, self.SUBMIT, self.Agency, self.Avcard_URI, self.COUNTRY, self.InitiSrce, self.InitiDate, self.ESN, self.ESZ]
        self.FIELDS_WITH_DOMAINS = {self.COUNTRY: "COUNTRY", self.STATE: "STATE", self.SUBMIT: "YESNO", self.DiscrpAgID: "AGENCYID", self.AGENCYID: "AGENCYID"}
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.AGENCYID,
                          self.ESN, self.RevEditor, self.SUBMIT, self.Comment]

# Modified to OK fields
def getDefaultNG911ESZObject(gdb_version):
    # TODO: NEED UPDATED STANDARDS FOR ESZ LAYER TO VERIFY METHOD CALL
    NG911_ESZ_Default = NG911_ESZ_Object("DiscrpAgID", "RevDate", "EffectDate", "ExpireDate", "NGUID_ESZ", "Country", "State", "Agency", "Agency_ID", "ESN", "ESZ",
                                         "RevEditor", "SUBMIT", "Comment", "Avcard_URI", #"ServiceURN", "ServiceURI",
                                         "ServiceNum","InitiSrce", "InitiDate", gdb_version)

    return NG911_ESZ_Default


class NG911_CountyBoundary_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_RevDate, u_COUNTYID, u_STATE, u_COUNTY, u_RevEditor, u_SUBMIT, u_Comment,
                 u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_RevDate, None, None, u_COUNTYID, u_RevEditor, u_SUBMIT, u_Comment, u_gdb_version)
        self.COUNTYID = u_COUNTYID
        self.STATE = u_STATE
        self.COUNTY = u_COUNTY
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.STATE, self.COUNTY, self.RevEditor]
        self.FIELDS_WITH_DOMAINS = {self.STATE: 'STATE', self.COUNTY: "COUNTY"}
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.STATE, self.COUNTY, self.RevEditor, self.SUBMIT, self.Comment]


def getDefaultNG911CountyBoundaryObject(gdb_version):

    NG911_CountyBoundary_Default = NG911_CountyBoundary_Object("DiscrpAgID", "RevDate", "NGCOUNTYID", "STATE", "COUNTY", "RevEditor",
                                                               "SUBMIT", "Comment", gdb_version)

    return NG911_CountyBoundary_Default


class NG911_AuthoritativeBoundary_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ABID, u_AGENCYID, u_RevEditor,
                 u_SUBMIT, u_Comment, u_Agency, u_Avcard_URI, u_ServiceURN, u_ServiceURI, u_ServiceNum, u_Country,
                 u_STATE, u_InitiSrce, u_InitiDate, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_AGENCYID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_ABID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.ABID = u_ABID
        self.AGENCYID = u_AGENCYID
        self.Agency = u_Agency
        self.Avcard_URI = u_Avcard_URI
        self.ServiceURN = u_ServiceURN
        self.ServiceURI = u_ServiceURI
        self.ServiceNum = u_ServiceNum
        self.Country = u_Country
        self.State = u_STATE
        self.InitiSrce = u_InitiSrce
        self.InitiDate = u_InitiDate
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.State, self.AGENCYID,
                                self.RevEditor, self.SUBMIT, self.Agency, self.Avcard_URI, self.ServiceURN,
                                self.ServiceURI, self.Country, self.InitiSrce, self.InitiDate]
        self.FIELDS_WITH_DOMAINS = {self.Country: "COUNTRY", self.State: "STATE", self.SUBMIT: "YESNO",
                                    self.DiscrpAgID: "AGENCYID", self.AGENCYID: "AGENCYID",
                                    self.ServiceURN: "SERVICEURN"}
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.AGENCYID,
                          self.RevEditor, self.SUBMIT, self.Comment]

# Modified to OK fields
def getDefaultNG911AuthoritativeBoundaryObject(gdb_version):

    NG911_AuthoritativeBoundary_Default = NG911_AuthoritativeBoundary_Object("DiscrpAgID", "RevDate", "EffectDate", "ExpireDate", "NGUID_DISC", "Agency_ID",
                                                                             "RevEditor", "SUBMIT", "Comment", "Agency", "Avcard_URI", "ServiceURN",
                                                                             "ServiceURI","ServiceNum", "Country", "State", "InitiSrce", "InitiDate", gdb_version)

    return NG911_AuthoritativeBoundary_Default


class NG911_MunicipalBoundary_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_MUNI_ID, u_STATE, u_COUNTY, u_MUNI, u_RevEditor,
                 u_SUBMIT, u_Comment, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_MUNI_ID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.MUNI_ID = u_MUNI_ID
        self.STATE = u_STATE
        self.COUNTY = u_COUNTY
        self.MUNI = u_MUNI
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.UNIQUEID, self.STATE, self.COUNTY,
                                self.MUNI, self.RevEditor, self.SUBMIT]
        self.FIELDS_WITH_DOMAINS = {self.STATE: "STATE", self.COUNTY: "COUNTY", self.SUBMIT: "YESNO"}
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.STATE, self.COUNTY, self.MUNI,
                          self.RevEditor, self.SUBMIT, self.Comment]

# Modified to OK fields
def getDefaultNG911MunicipalBoundaryObject(gdb_version):

    NG911_MunicipalBoundary_Default = NG911_MunicipalBoundary_Object("DiscrpAgID", "RevDate", "EffectDate", "ExpireDate", "NGUID_MUNI", "State", "County", "City",
                                                                     "RevEditor", "SUBMIT", "Comment", gdb_version) #RevEditor

    return NG911_MunicipalBoundary_Default


class NG911_PSAP_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_PSAP_ID, u_Agency, u_AGENCYID, u_Avcard_URI, u_ServiceURN, u_ServiceURI, u_ServiceNum, u_Country,
                 u_State, u_InitiSrc, u_InitiDate, u_RevEditor, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_SUBMIT, u_Comment,
                 u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_AGENCYID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_PSAP_ID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.PSAP_ID = u_PSAP_ID
        self.Agency = u_Agency
        self.AGENCYID = u_AGENCYID
        self.Avcard_URI = u_Avcard_URI
        self.ServiceURN = u_ServiceURN
        self.ServiceURI = u_ServiceURI
        self.ServiceNum = u_ServiceNum
        self.Country = u_Country
        self.State = u_State
        self.InitiSrce = u_InitiSrc
        self.InitiDate = u_InitiDate
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.State, self.AGENCYID,
                                self.RevEditor, self.SUBMIT, self.Agency, self.Avcard_URI, self.ServiceURN,
                                self.ServiceURI, self.Country, self.InitiSrce, self.InitiDate]
        self.FIELDS_WITH_DOMAINS = {self.Country: "COUNTRY", self.State: "STATE", self.SUBMIT: "YESNO",
                                    self.DiscrpAgID: "AGENCYID", self.AGENCYID: "AGENCYID",
                                    self.ServiceURN: "SERVICEURN"}
        self.FIELD_MAP = [self.DiscrpAgID, self.PSAP_ID, self.Agency, self.AGENCYID, self.Avcard_URI, self.ServiceURN,
                          self.ServiceNum, self.Country, self.State, self.InitiSrce, self.InitiDate, self.RevEditor,
                          self.RevDate, self.EFF_DATE, self.EXP_DATE, self.SUBMIT, self.Comment]


def getDefaultNG911PSAPObject(gdb_version):

    NG911_PSAP_Default = NG911_PSAP_Object("DiscrpAgID", "NGUID_PSAP", "Agency", "Agency_ID", "Avcard_URI",
                                             "ServiceURN", "ServiceURI", "ServiceNum", "Country", "State", "InitiSrce",
                                             "InitiDate", "RevEditor", "RevDate", "EffectDate", "ExpireDate","SUBMIT","Comment",
                                             gdb_version)

    return NG911_PSAP_Default

class NG911_Hydrant_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_HYDID, u_HYDTYPE, u_PROVIDER, u_STATUS, u_PRIVATE, u_SUBMIT, u_Comment,
                 u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, None, None, None, u_HYDID, None, u_SUBMIT, u_Comment, u_gdb_version)
        self.NGHYDID = u_HYDID
        self.HYDTYPE = u_HYDTYPE
        self.PROVIDER = u_PROVIDER
        self.STATUS = u_STATUS
        self.PRIVATE = u_PRIVATE
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.UNIQUEID, self.HYDTYPE, self.STATUS, self.PRIVATE, self.SUBMIT]
        self.FIELDS_WITH_DOMAINS = {self.DiscrpAgID: "DiscrpAgID", self.SUBMIT: "YN", self.HYDTYPE: "HYDTYPE",
                                    self.STATUS: "HYDSTATUS", self.PRIVATE: "PRIVATE"}
        self.FIELD_MAP = [self.DiscrpAgID, self.UNIQUEID, self.HYDTYPE, self.PROVIDER, self.STATUS,
                          self.SUBMIT, self.Comment, self.PRIVATE]


def getDefaultNG911HydrantObject(gdb_version):

    NG911_Hydrant_Default = NG911_Hydrant_Object("DiscrpAgID", "NGHYDID", "HYDTYPE", "PROVIDER", "HYDSTATUS",
                                                 "PRIVATE", "SUBMIT", "Comment", gdb_version)

    return NG911_Hydrant_Default


class NG911_Parcel_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_OKPID, u_SUBMIT, u_Comment, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, None, None, None, u_OKPID, u_SUBMIT, u_Comment, u_gdb_version)
        self.NGOKPID = u_OKPID
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.UNIQUEID]
        self.FIELDS_WITH_DOMAINS = {self.DiscrpAgID: "DiscrpAgID", self.SUBMIT: "YN"}
        self.FIELD_MAP = [self.DiscrpAgID, self.UNIQUEID, self.SUBMIT, self.Comment]


def getDefaultNG911ParcelObject(gdb_version):

    NG911_Parcel_Default = NG911_Parcel_Object("DiscrpAgID", "NGOKPID", "SUBMIT", "Comment", gdb_version)

    return NG911_Parcel_Default


class NG911_Gate_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_NGGATEID, u_GATE_TYPE, u_SIREN, u_RF_OP, u_KNOXBOX, u_KEYPAD, u_MAN_OPEN,
                 u_GATEOPEN, u_G_OWNER, u_SUBMIT, u_Comment, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, None, None, None, u_NGGATEID, None, u_SUBMIT, u_Comment, u_gdb_version)
        self.NGGATEID = u_NGGATEID
        self.GATE_TYPE = u_GATE_TYPE
        self.SIREN = u_SIREN
        self.RF_OP = u_RF_OP
        self.KNOXBOX = u_KNOXBOX
        self.KEYPAD = u_KEYPAD
        self.MAN_OPEN = u_MAN_OPEN
        self.GATEOPEN = u_GATEOPEN
        self.G_OWNER = u_G_OWNER
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.UNIQUEID, self.GATE_TYPE, self.SIREN, self.RF_OP, self.KNOXBOX, self.KEYPAD, self.MAN_OPEN, self.GATEOPEN]
        self.FIELDS_WITH_DOMAINS = {self.DiscrpAgID: "DiscrpAgID", self.SUBMIT: "YN", self.GATE_TYPE: "GATE_TYPE", self.SIREN: "YNU",
                                    self.RF_OP: "YNU", self.KNOXBOX: "YNU", self.KEYPAD: "YNU", self.MAN_OPEN: "YNU", self.GATEOPEN: "YNU"}
        self.FIELD_MAP = [self.DiscrpAgID, self.UNIQUEID, self.GATE_TYPE, self.SIREN, self.RF_OP, self.KNOXBOX, self.KEYPAD, self.MAN_OPEN,
                          self.GATEOPEN, self.G_OWNER, self.SUBMIT, self.Comment]


def getDefaultNG911GateObject(gdb_version):

    NG911_Gate_Default = NG911_Gate_Object("DiscrpAgID", "NGGATEID", "GATE_TYPE", "SIREN", "RF_OP", "KNOXBOX", "KEYPAD",
                                           "MAN_OPEN", "GATEOPEN", "G_OWNER", "SUBMIT", "Comment", gdb_version)

    return NG911_Gate_Default


class NG911_Utility_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_NGUSERVID, u_UTIL_NAME, u_PHONENUM, u_SUBMIT, u_Comment, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, None, None, None, u_NGUSERVID, None, u_SUBMIT, u_Comment, u_gdb_version)
        self.NGUSERVID = u_NGUSERVID
        self.UTIL_NAME = u_UTIL_NAME
        self.PHONENUM = u_PHONENUM
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.UNIQUEID, self.UTIL_NAME, self.PHONENUM]
        self.FIELDS_WITH_DOMAINS = {self.DiscrpAgID: "DiscrpAgID"}
        self.FIELD_MAP = [self.DiscrpAgID, self.UNIQUEID, self.UTIL_NAME, self.PHONENUM, self.SUBMIT, self.Comment]


def getDefaultNG911UtilityObject(gdb_version):

    NG911_Utility_Default = NG911_Utility_Object("DiscrpAgID", "NGUSERVID", "UTIL_NAME", "PHONENUM", "SUBMIT", "Comment", gdb_version)

    return NG911_Utility_Default


class NG911_Bridge_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_NGBRIDGE, u_LPA_NAME, u_STRUCT_NO, u_WEIGHT_L, u_OVERUNDER, u_STATUS, u_SUBMIT,
                 u_Comment, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, None, None, None, u_NGBRIDGE, u_SUBMIT, u_Comment, u_gdb_version)
        self.NGBRIDGE = u_NGBRIDGE
        self.LPA_NAME = u_LPA_NAME
        self.STRUCT_NO = u_STRUCT_NO
        self.WEIGHT_L = u_WEIGHT_L
        self.OVERUNDER = u_OVERUNDER
        self.STATUS = u_STATUS
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.UNIQUEID]
        self.FIELDS_WITH_DOMAINS = {self.DiscrpAgID: "DiscrpAgID", self.STATUS: "BRIDGESTATUS", self.OVERUNDER: "OVERUNDER"}
        self.FIELD_MAP = [self.DiscrpAgID, self.UNIQUEID, self.LPA_NAME, self.STRUCT_NO, self.WEIGHT_L, self.OVERUNDER, self.STATUS,
                          self.SUBMIT, self.Comment]


def getDefaultNG911BridgeObject(gdb_version):

    NG911_Bridge_Default = NG911_Bridge_Object("DiscrpAgID", "NGBRIDGE", "LPA_NAME", "STRUCT_NO", "WEIGHT_L",
                                               "OVERUNDER", "STATUS", "SUBMIT", "Comment", gdb_version)

    return NG911_Bridge_Default


class NG911_CellSite_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_RevDate, u_NGCELLID, u_EFF_DATE, u_EXP_DATE, u_STATE, u_COUNTY, u_HEIGHT,
                 u_TWR_TYP, u_RevEditor, u_SUBMIT, u_Comment, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_NGCELLID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.NGCELLID = u_NGCELLID
        self.STATE = u_STATE
        self.COUNTY = u_COUNTY
        self.HEIGHT = u_HEIGHT
        self.TWR_TYP = u_TWR_TYP
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.EFF_DATE, self.STATE, self.COUNTY, self.RevEditor]
        self.FIELDS_WITH_DOMAINS = {self.DiscrpAgID: "DiscrpAgID", self.TWR_TYP: "TWR_TYP"}
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.UNIQUEID, self.EFF_DATE, self.EXP_DATE, self.STATE, self.COUNTY,
                          self.HEIGHT, self.TWR_TYP, self.RevEditor, self.SUBMIT, self.Comment]


def getDefaultNG911CellSiteObject(gdb_version):

    NG911_CellSite_Default = NG911_CellSite_Object("DiscrpAgID", "RevDate", "NGCELLID", "EFF_DATE", "EXP_DATE", "STATE", "COUNTY",
                                                   "HEIGHT", "TWR_TYP", "RevEditor", "SUBMIT", "Comment", gdb_version)

    return NG911_CellSite_Default


class NG911_CellSector_Object(NG911FeatureClassObject):

    def __init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_NGCELLID, u_STATE, u_COUNTY, u_SITEID,
                 u_SECTORID, u_SWITCHID, u_MARKETID, u_C_SITEID, u_ESRD, u_LASTESRK, u_SECORN, u_RevEditor, u_SUBMIT,
                 u_Comment, u_gdb_version):

        NG911FeatureClassObject.__init__(self, u_DiscrpAgID, u_RevDate, u_EFF_DATE, u_EXP_DATE, u_NGCELLID, u_RevEditor, u_SUBMIT,
                                         u_Comment, u_gdb_version)
        self.NGCELLID = u_NGCELLID
        self.STATE = u_STATE
        self.COUNTY = u_COUNTY
        self.SITEID = u_SITEID
        self.SECTORID = u_SECTORID
        self.SWITCHID = u_SWITCHID
        self.MARKETID = u_MARKETID
        self.C_SITEID = u_C_SITEID
        self.ESRD = u_ESRD
        self.LASTESRK = u_LASTESRK
        self.SECORN = u_SECORN
        self.REQUIRED_FIELDS = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.UNIQUEID, self.STATE, self.COUNTY, self.SECTORID,
                                self.SECORN, self.RevEditor]
        self.FIELDS_WITH_DOMAINS = {self.STATE: "STATE", self.COUNTY: "COUNTY", self.SUBMIT: "YN", self.DiscrpAgID: "DiscrpAgID"}
        self.FIELD_MAP = [self.DiscrpAgID, self.RevDate, self.EFF_DATE, self.EXP_DATE, self.UNIQUEID, self.STATE, self.COUNTY, self.SITEID,
                          self.SECTORID, self.SWITCHID, self.MARKETID, self.C_SITEID, self.ESRD, self.LASTESRK, self.SECORN,
                          self.RevEditor, self.SUBMIT, self.Comment]


def getDefaultNG911CellSectorObject(gdb_version):

    NG911_CellSector_Default = NG911_CellSector_Object("DiscrpAgID", "RevDate", "EFF_DATE", "EXP_DATE", "NGCELLID", "STATE", "COUNTY", "SITEID",
                                                       "SECTORID", "SWITCHID", "MARKETID", "C_SITEID", "ESRD", "LASTESRK", "SECORN", "RevEditor", "SUBMIT", "Comment", gdb_version)

    return NG911_CellSector_Default


class TN_Object(object):

    def __init__(self, u_LocatorFolder, u_AddressLocator, u_RoadLocator, u_CompositeLocator, u_TN_List, u_ResultsFC, u_ResultsTable, u_UNIQUEID,
                 u_defaultFullAddress, u_tn_gdb):
        # type: (str, str, str, str, str, str, str, str, str, str) -> TN_Object
        self.LocatorFolder = u_LocatorFolder
        self.AddressLocator = u_AddressLocator
        self.RoadLocator = u_RoadLocator
        self.CompositeLocator = u_CompositeLocator
        self.TN_List = u_TN_List
        self.ResultsFC = u_ResultsFC
        self.ResultsTable = u_ResultsTable
        self.UNIQUEID = u_UNIQUEID
        self.DefaultFullAddress = u_defaultFullAddress
        self.tn_gdb = u_tn_gdb


def getTNObject(gdb):
    from os.path import join,dirname,basename
    from time import strftime

    LocatorFolder = join(dirname(gdb), basename(gdb).replace(".gdb","") + "_TN")
    today = strftime('%Y%m%d')
    tn_gdb = join(LocatorFolder, "TN_Working.gdb")
    tname = join(tn_gdb, "TN_List_" + today)
    output_fc = join(tn_gdb, "TN_GC_Output_" + today)
    resultsTable = join(tn_gdb, "TN_Geocode_Results_" + today)


    NG911_TN_Default = TN_Object(
        u_LocatorFolder = LocatorFolder,
        u_AddressLocator = join(LocatorFolder, "AddressLocator"),
        u_RoadLocator = join(LocatorFolder, "RoadLocator"),
        u_CompositeLocator = join(LocatorFolder, "CompositeLoc"),
        u_TN_List = tname,
        u_ResultsFC = output_fc,
        u_ResultsTable = resultsTable,
        u_UNIQUEID = "NGTNID",
        u_defaultFullAddress = "SingleLineInput",
        u_tn_gdb = tn_gdb
    )

    return NG911_TN_Default


class NG911_Session_obj(object):
    """
    A class whose attributes include paths to the geodatabase and the Domains folder, as well as an __NG911_GDB_Object.

    Attributes
    ----------
    gdbPath : str
        Path to the NG911 geodatabase
    domainsFolderPath : str
        Path to the Domains folder, which contains text files with easily-parsable pipe-delimited information about the
        domains used in the fields of the NG911 geodatabase's feature classes and tables
    fieldsFolderPath : str
        Path to the Fields folder, which contains text files with easily-parsable pipe-delimited information about the
        fields used in the NG911 geodatabase's feature classes and tables
    gdbObject : __NG911_GDB_Object
        An object whose attributes provide information about the NG911 geodatabase and its contents
    checkList : str
        ??? [Please fill in if you figure out what this attribute is for!]

    """
    def __init__(self, gdb, folder, folder2, gdbObject):
        self.gdbPath = gdb  # type: str
        self.domainsFolderPath = folder  # type: str
        self.fieldsFolderPath = folder2  # type: str
        self.gdbObject = gdbObject  # type: __NG911_GDB_Object # contains fcList & esbList
        self.checkList = ""  # type: Union[str, List[str]]


def getProjectionFile():
    # prj = r"\\vesta\d$\NG911_Pilot_Agg\KDOT_Lambert.prj"
    prj = r"G:\ArcGIS\Project Files\Traffic Safety\Grid System\gdb\Lambert_Conformal_Conic_2SP.prj" # Oklahoma Projection
    return prj


def NG911_Session(gdb):
    # type: (str) -> NG911_Session_obj
    """Constructs and returns an NG911_Session_obj, which contains the path to the GDB, the path to the Domains folder,
    and an __NG911_GDB_obj.

    Parameters
    ----------
    gdb : str
        Path to the geodatabase

    Returns
    -------
    NG911_Session_obj
        An object containing the path to the GDB, the path to the Domains folder, and an __NG911_GDB_obj

    """
    from os.path import dirname, join, realpath

    folder = join(dirname(dirname(realpath(__file__))), "Domains")
    folder2 = join(dirname(dirname(realpath(__file__))), "Fields")

    # get geodatabase object set up
    gdbObject = getGDBObject(gdb)  # type: __NG911_GDB_Object
    NG911_obj = NG911_Session_obj(gdb, folder, folder2, gdbObject)  # type: NG911_Session_obj

    return NG911_obj


class __NG911_GDB_Object:
    def __init__(self, gdb, version, prj, ESB, EMS, FIRE, LAW, RESCUE, esbList):
        # type: (str, str, int, str, str, str, str, str, List[str]) -> None
        self.gdbPath = gdb  # type: str
        self.GDB_VERSION = version  # type: str
        self.ProjectionFile = prj  # type: int
        self.NG911_FeatureDataset = join(gdb, "NG911")  # type: str
        self.AddressPoints = join(self.NG911_FeatureDataset, "ADDRESS_POINT")  # type: str # Changed to OK Fields
        self.RoadCenterline = join(self.NG911_FeatureDataset, "ROAD_CENTERLINE")  # type: str # Changed to OK Fields
        self.RoadAlias = join(gdb, "ROAD_ALIAS")  # type: str # Changed to OK Fields
        # self.AuthoritativeBoundary = join(self.NG911_FeatureDataset, "AuthoritativeBoundary")
        self.AuthoritativeBoundary = join(self.NG911_FeatureDataset, "DISCREPANCYAGENCY_BOUNDARY")  # type: str # Changed to OK Fields
        self.ESZ = join(self.NG911_FeatureDataset, "ESZ_BOUNDARY")  # type: str # Changed to OK Fields
        self.PSAP = join(self.NG911_FeatureDataset, "PSAP_BOUNDARY")  # type: str # Changed to OK Fields
        self.Topology = join(self.NG911_FeatureDataset, "NG911_Topology")  # type: str
        self.gc_test = join(gdb, "gc_test")  # type: str
        self.GeocodeTable = join(gdb, "GeocodeTable")  # type: str
        self.AddressPointFrequency = join(gdb, "AP_Freq")  # type: str
        self.RoadCenterlineFrequency = join(gdb, "Road_Freq")  # type: str
        self.FieldValuesCheckResults = join(gdb, "FieldValuesCheckResults")  # type: str
        self.TemplateCheckResults = join(gdb, "TemplateCheckResults")  # type: str
        self.ESB = ESB  # type: str
        self.EMS = EMS  # type: str
        self.FIRE = FIRE  # type: str
        self.LAW = LAW  # type: str
        self.RESCUE = RESCUE  # type: str

        # if self.GDB_VERSION == "20":
        #     self.HYDRANTS = join(gdb, "Hydrants")  # type: str
        #     self.PARCELS = join(gdb, "Parcels")  # type: str
        #     self.GATES = join(gdb, "Gates")  # type: str
        #     self.CELL_SECTOR = join(gdb, "Cell_Sector")  # type: str
        #     self.BRIDGES = ""  # type: str
        #     self.CELLSITES = ""  # type: str
        #     self.UT_ELECTRIC = ""  # type: str
        #     self.UT_GAS = ""  # type: str
        #     self.UT_SEWER = ""  # type: str
        #     self.UT_WATER = ""  # type: str
        # elif self.GDB_VERSION == "21":
        self.OPTIONAL_LAYERS_FD = join(gdb, "OptionalLayers")  # type: str
        self.HYDRANTS = join(self.OPTIONAL_LAYERS_FD, "HYDRANTS")  # type: str
        self.PARCELS = join(self.OPTIONAL_LAYERS_FD, "PARCELS")  # type: str
        self.GATES = join(self.OPTIONAL_LAYERS_FD, "GATES")  # type: str
        self.CELL_SECTOR = join(self.OPTIONAL_LAYERS_FD, "CELLSECTORS")  # type: str
        self.CELLSITES = join(self.OPTIONAL_LAYERS_FD, "CELLSITES")  # type: str
        self.BRIDGES = join(self.OPTIONAL_LAYERS_FD, "BRIDGES")  # type: str
        self.UT_ELECTRIC = join(self.OPTIONAL_LAYERS_FD, "UT_ELECTRIC")  # type: str
        self.UT_GAS = join(self.OPTIONAL_LAYERS_FD, "UT_GAS")  # type: str
        self.UT_SEWER = join(self.OPTIONAL_LAYERS_FD, "UT_SEWER")  # type: str
        self.UT_WATER = join(self.OPTIONAL_LAYERS_FD, "UT_WATER")  # type: str
        self.MunicipalBoundary = join(self.OPTIONAL_LAYERS_FD,
                                      "MUNICIPAL_BOUNDARY")  # type: str # Changed to OK Fields
        self.CountyBoundary = join(self.OPTIONAL_LAYERS_FD, "COUNTY_BOUNDARY")  # type: str # Changed to OK Fields

        # populate the utility list
        utList = [self.UT_ELECTRIC, self.UT_GAS, self.UT_SEWER, self.UT_WATER]  # type: List[str]

        # standard lists
        self.AdminBoundaryList = [basename(self.AuthoritativeBoundary), basename(self.CountyBoundary), basename(self.MunicipalBoundary),
                                  basename(self.ESZ), basename(self.PSAP)]  # type: List[str]
        self.AdminBoundaryFullPathList = [self.AuthoritativeBoundary, self.CountyBoundary, self.MunicipalBoundary,
                                          self.ESZ, self.PSAP]  # type: List[str]
        self.esbList = esbList  # type: List[str]
        # self.requiredLayers = [self.RoadAlias, self.AddressPoints, self.RoadCenterline, self.AuthoritativeBoundary, self.ESZ] + esbList  # type: List[str]
        self.requiredLayers = [self.AddressPoints, self.RoadCenterline, self.AuthoritativeBoundary, self.ESZ, self.PSAP] + esbList  # type: List[str]

        # variable lists
        # featureClasses = [self.AddressPoints, self.RoadCenterline, self.RoadAlias, self.AuthoritativeBoundary, self.MunicipalBoundary,
        #                   self.CountyBoundary, self.ESZ, self.PSAP, self.HYDRANTS, self.PARCELS, self.GATES, self.CELL_SECTOR]   # type: List[str]
        # TODO: Removed muni layer for testing purposes
        featureClasses = [self.AddressPoints, self.RoadCenterline, self.AuthoritativeBoundary,
                          # self.MunicipalBoundary,
                          self.CountyBoundary, self.ESZ, self.PSAP,
                          self.HYDRANTS, self.PARCELS, self.GATES,
                          self.CELL_SECTOR]  # type: List[str]


        otherLayers = [self.MunicipalBoundary, self.HYDRANTS, self.PARCELS, self.GATES, self.CELL_SECTOR]  # type: List[str]

        # make sure a 2.1 object contains the right information
        setList = [featureClasses, otherLayers]  # type: List[List[str]]

        # if version == "21":
        for sl in setList:
            for rf in utList + [self.BRIDGES, self.CELLSITES]:
                sl.append(rf)

        # add all esb layers to fcList
        for esb in esbList:
            featureClasses.append(esb)

        self.fcList = featureClasses
        self.otherLayers = otherLayers

def getGDBObject(gdb):
    # type: (str) -> __NG911_GDB_Object
    from NG911_arcpy_shortcuts import fieldExists, hasRecords

    featureDataset = "NG911"

    # see what version of the database we're working with
    ap = join(gdb, featureDataset, "ADDRESS_POINT")  # type: str # Changed to OK Fields
    # if fieldExists(ap, "RCLMatch"):
    #     version = "21"  # type: str
    # else:
    #     version = "20"  # type: str
    version = "21"  # type: str

    # prep potential ESB list
    ESB = join(gdb, featureDataset, "ESB")  # type: str
    EMS = join(gdb, featureDataset, "ESB_EMS_BOUNDARY")  # type: str # Changed to OK Fields
    FIRE = join(gdb, featureDataset, "ESB_FIRE_BOUNDARY")  # type: str # Changed to OK Fields
    LAW = join(gdb, featureDataset, "ESB_LAW_BOUNDARY")  # type: str # Changed to OK Fields
    PSAP = join(gdb, featureDataset, "PSAP_BOUNDARY")  # type: str # Changed to OK Fields
    RESCUE = join(gdb, featureDataset, "ESB_RESCUE_BOUNDARY")  # type: str # Changed to OK Fields
    FIREAUTOAID = join(gdb, featureDataset, "ESB_FIREAUTOAID_BOUNDARY")  # type: str # Changed to OK Fields

    # test to see what should be included in the for-real ESB list
    esbList = [EMS, FIRE, LAW]  # type: List[str]
    # for e in [EMS, FIRE, LAW]:  # type: str
    # # for e in [ESB, EMS, FIRE, LAW, PSAP, RESCUE, FIREAUTOAID]:  # type: str
    #     if arcpy.Exists(e): # make sure the layer exists
    #         if hasRecords(e): # make sure the layer has records
    #             if e not in esbList:
    #                 esbList.append(e)

    # get the path to the projection file
    # prj = getProjectionFile()  # type: str
    prj = 4326  # type: int

    # This is a class used represent the NG911 geodatabase
    # = = = = = = = = = = = = = = = = = = =  NOTICE!  = = = = = = = = = = = = = = = = = = =
    # = = = = THIS CLASS HAS BEEN MOVED TO FILE SCOPE AS CLASS "__NG911_GDB_Object" = = = =
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # class NG911_GDB_Object:
    #     def __init__(self):
    #         self.gdbPath = gdb  # type: str
    #         self.GDB_VERSION = version  # type: str
    #         self.ProjectionFile = prj  # type: str
    #         self.NG911_FeatureDataset = join(gdb, "NG911")  # type: str
    #         self.AddressPoints = join(self.NG911_FeatureDataset, "Address_Point")  # type: str # Changed to OK Fields
    #         self.RoadCenterline = join(self.NG911_FeatureDataset, "Road_Centerline")  # type: str # Changed to OK Fields
    #         self.RoadAlias = join(gdb, "Road_Alias")  # type: str # Changed to OK Fields
    #         # self.AuthoritativeBoundary = join(self.NG911_FeatureDataset, "AuthoritativeBoundary")
    #         self.AuthoritativeBoundary = join(self.NG911_FeatureDataset, "Provisioning_Boundary")  # type: str # Changed to OK Fields
    #         self.MunicipalBoundary = join(self.NG911_FeatureDataset, "Municipal_Boundary")  # type: str # Changed to OK Fields
    #         self.CountyBoundary = join(self.NG911_FeatureDataset, "County_Boundary")  # type: str # Changed to OK Fields
    #         self.ESZ = join(self.NG911_FeatureDataset, "ESZ_Boundary")  # type: str # Changed to OK Fields
    #         self.PSAP = join(self.NG911_FeatureDataset, "PSAP_Boundary")  # type: str # Changed to OK Fields
    #         self.Topology = join(self.NG911_FeatureDataset, "NG911_Topology")  # type: str
    #         self.gc_test = join(gdb, "gc_test")  # type: str
    #         self.GeocodeTable = join(gdb, "GeocodeTable")  # type: str
    #         self.AddressPointFrequency = join(gdb, "AP_Freq")  # type: str
    #         self.RoadCenterlineFrequency = join(gdb, "Road_Freq")  # type: str
    #         self.FieldValuesCheckResults = join(gdb, "FieldValuesCheckResults")  # type: str
    #         self.TemplateCheckResults = join(gdb, "TemplateCheckResults")  # type: str
    #         self.ESB = ESB  # type: str
    #         self.EMS = EMS  # type: str
    #         self.FIRE = FIRE  # type: str
    #         self.LAW = LAW  # type: str
    #         self.RESCUE = RESCUE  # type: str
    #
    #         if self.GDB_VERSION == "20":
    #             self.HYDRANTS = join(gdb, "Hydrants")  # type: str
    #             self.PARCELS = join(gdb, "Parcels")  # type: str
    #             self.GATES = join(gdb, "Gates")  # type: str
    #             self.CELL_SECTOR = join(gdb, "Cell_Sector")  # type: str
    #             self.BRIDGES = ""  # type: str
    #             self.CELLSITES = ""  # type: str
    #             self.UT_ELECTRIC = ""  # type: str
    #             self.UT_GAS = ""  # type: str
    #             self.UT_SEWER = ""  # type: str
    #             self.UT_WATER = ""  # type: str
    #         elif self.GDB_VERSION == "21":
    #             self.OPTIONAL_LAYERS_FD = join(gdb, "OptionalLayers")  # type: str
    #             self.HYDRANTS = join(self.OPTIONAL_LAYERS_FD, "HYDRANTS")  # type: str
    #             self.PARCELS = join(self.OPTIONAL_LAYERS_FD, "PARCELS")  # type: str
    #             self.GATES = join(self.OPTIONAL_LAYERS_FD, "GATES")  # type: str
    #             self.CELL_SECTOR = join(self.OPTIONAL_LAYERS_FD, "CELLSECTORS")  # type: str
    #             self.CELLSITES = join(self.OPTIONAL_LAYERS_FD, "CELLSITES")  # type: str
    #             self.BRIDGES = join(self.OPTIONAL_LAYERS_FD, "BRIDGES")  # type: str
    #             self.UT_ELECTRIC = join(self.OPTIONAL_LAYERS_FD, "UT_ELECTRIC")  # type: str
    #             self.UT_GAS = join(self.OPTIONAL_LAYERS_FD, "UT_GAS")  # type: str
    #             self.UT_SEWER = join(self.OPTIONAL_LAYERS_FD, "UT_SEWER")  # type: str
    #             self.UT_WATER = join(self.OPTIONAL_LAYERS_FD, "UT_WATER")  # type: str
    #
    #         # populate the utility list
    #         utList = [self.UT_ELECTRIC, self.UT_GAS, self.UT_SEWER, self.UT_WATER]  # type: List[str]
    #
    #         # standard lists
    #         self.AdminBoundaryList = [basename(self.AuthoritativeBoundary), basename(self.CountyBoundary), basename(self.MunicipalBoundary),
    #                                   basename(self.ESZ), basename(self.PSAP)]  # type: List[str]
    #         self.AdminBoundaryFullPathList = [self.AuthoritativeBoundary, self.CountyBoundary, self.MunicipalBoundary,
    #                                           self.ESZ, self.PSAP]  # type: List[str]
    #         self.esbList = esbList  # type: List[str]
    #         self.requiredLayers = [self.RoadAlias, self.AddressPoints, self.RoadCenterline, self.AuthoritativeBoundary, self.ESZ] + esbList  # type: List[str]
    #
    #         # variable lists
    #         featureClasses = [self.AddressPoints, self.RoadCenterline, self.RoadAlias, self.AuthoritativeBoundary, self.MunicipalBoundary,
    #                           self.CountyBoundary, self.ESZ, self.PSAP, self.HYDRANTS, self.PARCELS, self.GATES, self.CELL_SECTOR]   # type: List[str]
    #         otherLayers = [self.HYDRANTS, self.PARCELS, self.GATES, self.CELL_SECTOR]  # type: List[str]
    #
    #         # make sure a 2.1 object contains the right information
    #         setList = [featureClasses, otherLayers]  # type: List[List[str]]
    #
    #         if version == "21":
    #             for sl in setList:
    #                 for rf in utList + [self.BRIDGES, self.CELLSITES]:
    #                     sl.append(rf)
    #
    #         # add all esb layers to fcList
    #         for esb in esbList:
    #             featureClasses.append(esb)
    #
    #         self.fcList = featureClasses
    #         self.otherLayers = otherLayers

    NG911_GDB = __NG911_GDB_Object(gdb, version, prj, ESB, EMS, FIRE, LAW, RESCUE, esbList)

    return NG911_GDB

def getFCObject(fc):
    # type: (str) -> Union[NG911FeatureClassObject, NG911CheckResultsObject, NG911_RoadCenterline_Object, NG911_RoadAlias_Object, NG911_Address_Object, NG911_FieldValuesCheckResults_Object, NG911_TemplateCheckResults_Object, NG911_ESB_Object, NG911_ESZ_Object, NG911_CountyBoundary_Object, NG911_AuthoritativeBoundary_Object, NG911_MunicipalBoundary_Object, NG911_PSAP_Object, NG911_Hydrant_Object, NG911_Parcel_Object, NG911_Gate_Object, NG911_Utility_Object, NG911_Bridge_Object, NG911_CellSite_Object, NG911_CellSector_Object, None]
    from NG911_arcpy_shortcuts import fieldExists
    from os.path import basename

    word = basename(fc).upper()  # type: str

    obj = None  # Will later be set to an instance of a subclass of NG911FeatureClassObject

    # arcpy.AddMessage("Looking for FC object for: %s" % word)

    if "ROAD_CENTERLINE" in word: # Changed to OK Fields
        # if fieldExists(fc, "PROV_L"):
        #     # 2.1 indicator
        #     version = "21"
        # else:
        #     version = "20"
        version = "21"
        obj = getDefaultNG911RoadCenterlineObject(version)

    elif "ADDRESS_POINT" in word: # Changed to OK Fields
        # if fieldExists(fc, "RCLMatch"):
        #     # 2.1 indicator
        #     version = "21"
        # else:
        #     version = "20"
        version = "21"
        obj = getDefaultNG911AddressObject(version)

    elif "ROAD_ALIAS" in word: # Changed to OK Fields
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911RoadAliasObject("x")

    # elif "AUTHORITATIVEBOUNDARY" in word:
    elif "DISCREPANCYAGENCY_BOUNDARY" in word: # Changed to OK Fields
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911AuthoritativeBoundaryObject("x")

    elif "MUNICIPAL_BOUNDARY" in word: # Changed to OK Fields
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911MunicipalBoundaryObject("x")

    elif "COUNTY_BOUNDARY" in word: # Changed to OK Fields
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911CountyBoundaryObject("x")

    elif "ESZ_BOUNDARY" in word: # Changed to OK Fields
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911ESZObject("x")

    elif "ESB_FIRE" in word:
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911ESBFireObject("x")

    elif "ESB_LAW" in word:
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911ESBLawObject("x")

    elif "ESB_EMS" in word:
        # 2.1 & 2.0 are the same
        obj = getDefaultNG911ESBEMSObject("x")

    elif "PSAP" in word:
        obj = getDefaultNG911PSAPObject("x")

    # get various optional layers
    elif "PARCELS" in word:
        obj = getDefaultNG911ParcelObject("x")
    elif "GATES" in word:
        obj = getDefaultNG911GateObject("x")
    elif "HYDRANTS" in word:
        obj = getDefaultNG911HydrantObject("x")
    elif "CELL_SECTOR" in word or "CELLSECTORS" in word:
        obj = getDefaultNG911CellSectorObject("x")
    elif "BRIDGES" in word:
        obj = getDefaultNG911BridgeObject("x")
    elif "CELLSITE" in word:
        obj = getDefaultNG911CellSiteObject("x")
    elif word[0:3] == "UT_":
        obj = getDefaultNG911UtilityObject("x")

    elif word == "FIELDVALUESCHECKRESULTS":
        obj = getDefaultNG911FieldValuesCheckResultsObject()
    elif word == "TEMPLATECHECKRESULTS":
        obj = getDefaultNG911TemplateCheckResultsObject()

    if obj is None:
        arcpy.AddWarning("Could not find proper FC object for %s." % word)

    return obj
