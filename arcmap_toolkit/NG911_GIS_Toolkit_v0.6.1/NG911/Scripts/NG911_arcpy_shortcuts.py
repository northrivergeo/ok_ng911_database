# coding=utf-8
#-------------------------------------------------------------------------------
# Name:        NG911_arcpy_shortcuts
# Purpose:     Short cuts for repetitive arcpy coding
#
# Author:      kristen (KS), Baker (OK), Baird (OK)
#
# Created:     13/05/2016
# Modified:    June 10, 2022
#-------------------------------------------------------------------------------

# def addItemIfUnique(item, mList):
#     if item not in mList:
#         mList.append(item)
#     return mList

# def countQueryResults(fc, wc):
#     from arcpy import Delete_management
#     lyr = MakeLayer(fc, "lyrSelectStuff", wc)
#     count = getFastCount(lyr)
#     Delete_management(lyr)
#     return count

# def countLayersGetSize(folder):
#     from os import walk
#     from os.path import getsize, join
#
#     size = 0
#     for root, dirs, files in walk(folder):
#         for name in files:
#             ##get full pathname
#             if name[-4:] != 'lock':
#                 filename = join(root, name)
#                 fSize = getsize(filename)
#                 size = size + fSize
#
#     #add piece to calculate the size in MiB or GiB, whatever is better
#     # Note about units:
#     # The kibibyte (KiB) is equal to 1024 (=2^13) bytes (approx. 1.02 kilobytes)
#     # The mebibyte (MiB) is equal to 1024 (=2^23) KiB or 1048576 bytes (approx. 1049 kilobytes)
#     # The gibibyte (GiB) is equal to 1024 (=2^33) MiB or 1073741824 bytes (approx. 1074 megabytes)
#     sizeReport = ""
#     if size < 1048576:
#         kb = round(size/1024.00, 2)
#         sizeReport = str(kb) + " KiB"
#     elif 1048576 <= size < 1073741824:
#         mb = round(size/1048576.00, 2)
#         sizeReport = str(mb) + " MiB"
#     elif size >= 1073741824:
#         gb = round(size/1073741824.00, 2)
#         sizeReport = str(gb) + " GiB"
#
#     count = countLayers(folder)
#
#     return {"size":sizeReport, "count":count}
from os.path import exists, basename, join
from NG911_User_Messages import *
from collections import OrderedDict
from NG911_GDB_Objects import NG911_Session

try:
    from typing import Union, Tuple, List, Optional, Dict
except:
    pass

__vb_alert_string = u"VB expressions are not supported in 64-bit ArcGIS products. Use Python instead!\n\nFrom the ArcMap 10.7 documentation at https://desktop.arcgis.com/en/arcmap/10.7/tools/data-management-toolbox/calculate-field.htm:\nField calculations with a VB Expression type are not supported on 64-bit products, including ArcGIS Desktop—Background Geoprocessing (64-bit)—and ArcGIS Server. To successfully use Calculate Field in these products, expressions should be converted to Python, or in the case of Background Geoprocessing (64-bit), background processing can alternatively be disabled."  # type: unicode

def hasRecords(fc):
    # type: (str) -> bool
    """Returns a bool indicating whether or not a given feature class or table contains any records.

    Parameters
    ----------
    fc : str
        Name of the feature class or table to check for records

    Returns
    -------
    bool
        True if the input has records or False if it does not

    """
    if getFastCount(fc) > 0:
        return True
    else:
        return False

def AddFieldAndCalculate(fc, field, fieldType, length, expression, exp_lang):
    # type: (str, str, str, str, str, str) -> None
    """Adds a field to a feature class or table and immediately calculates its values using a Python or VB expression.

    Parameters
    ----------
    fc : str
        The input feature class or table (passed to arcpy's AddField_management)
    field : str
        Name of the field to be added and calculated (passed to arcpy's AddField_management)
    fieldType : str
        The type to assign to the new field. Must be one of "TEXT", "FLOAT", "DOUBLE", "SHORT", "LONG", "DATE", "BLOB",
        "RASTER", or "GUID" (passed to arcpy's AddField_management)
    length : long
        The length of the new field (passed to arcpy's AddField_management)
    expression : str
        Python or VB expression used to calculate the values of the new field (passed to arcpy's AddField_management)
    exp_lang : str
        One of "VB", "PYTHON", or "PYTHON_9.3". Providing "VB" will produce a warning, as there may be compatibility
        issues. (Passed to arcpy's AddField_management)
    """
    from arcpy import AddField_management, CalculateField_management

    # Validate exp_land
    if exp_lang is "VB":
        __vb_alert_message("AddFieldAndCalculate", "WARNING")
    elif exp_lang not in ["VB", "PYTHON", "PYTHON_9.3"]:
        # exp_lang not valid
        raise ValueError('AddFieldAndCalculate: exp_lang "%s" not valid. Must be one of "VB", "PYTHON", or "PYTHON_9.3 '
                         '.' % exp_lang)

    # Set length to None if value is one of the below null-like values
    if length in ["", " ", None, "#"]:
        length = None

    # Validate fieldType
    if fieldType not in ["TEXT", "FLOAT", "DOUBLE", "SHORT", "LONG", "DATE", "BLOB", "RASTER", "GUID"]:
        # Field type not valid
        raise ValueError('AddFieldAndCalculate: fieldType "%s" not valid. Must be one of "TEXT", "FLOAT", "DOUBLE", '
                         '"SHORT", "LONG", "DATE", "BLOB", "RASTER", or "GUID".')
    # Call AddField_management with field_length parameter if fieldType is appropriate
    if fieldType in ["TEXT", "BLOB"]:
        AddField_management(fc, field, fieldType, field_length=length)
    # Otherwise call AddField_management without field_length parameter
    else:
        if length is not None:
            userWarning("AddFieldAndCalculate: Argument length is unused for field of type %s." % fieldType)
        AddField_management(fc, field, fieldType)
    CalculateField_management(fc, field, expression, exp_lang)


def cleanUp(listOfItems):
    # type: (List[str]) -> int
    """Passes each item, such as a feature class or table, to deleteExising, which determines whether or not the item
    exists and deletes it if it does. Returns the number of items that were deleted.

    Parameters
    ----------
    listOfItems : list of str
        List of strings of names of items (such as feature classes and/or tables) to delete (if existing)

    Returns
    -------
    int
        The number of items deleted
    """
    deleted_items = 0  # type: int
    for item in listOfItems:
        if deleteExisting(item) is True:
            deleted_items += 1
    return deleted_items

def deleteExisting(item):
    # type: (str) -> bool
    """Deletes an item, such as a feature class or table, if it exists.

    Parameters
    ----------
    item : str
        The name of the item (such as a feature class or table) to delete (if it exists)

    Returns
    -------
    bool
        True if an item was deleted; False if no item was deleted

    """
    from arcpy import Exists, Delete_management
    if Exists(item):
        Delete_management(item)
        return True
    else:
        return False

def getFastCount(lyr):
    # type: (str) -> int
    """Returns the number of records contained in a feature class or table as an integer.

    Parameters
    ----------
    lyr : str
        The name of the feature class or table

    Returns
    -------
    int
        Number of records in lyr

    """
    from arcpy import GetCount_management
    result = GetCount_management(lyr)
    count = int(result.getOutput(0))
    return count

# def ExistsAndHasData(item):
#     result = False
#     from arcpy import Exists
#     if Exists(item):
#         if getFastCount(item) > 0:
#             result = True
#     return result

# def countLayers(folder):
#     from arcpy import ListFeatureClasses, env
#     env.workspace = folder
#     fcs = ListFeatureClasses()
#     count = len(fcs)
#     return count

def ListFieldNames(item):
    # type: (str) -> List[Union[str, unicode]]
    """Gets a list of the fields of an item, such as a feature class or table.

    Parameters
    ----------
    item : str
        Name of the table

    Returns
    -------
    list of str


    """
    #create a list of field names
    from arcpy import ListFields
    fieldList = map(lambda x: x.name, ListFields(item)) # WE REMOVED .upper()
    return fieldList

def fieldExists(fc, fieldName):
    # type: (str, str) -> bool
    """Returns a bool indicating whether or not a field with a given name exists in a feature class or table with a
    given name.

    Parameters
    ----------
    fc : str
        Name of the feature class or table to check
    fieldName : str
        Name of the field to search for in fc

    Returns
    -------
    bool
        True if fc has a field called fieldName, otherwise False

    """
    fields = ListFieldNames(fc)
    if fieldName in fields:
        return True
    else:
        return False

def delete_field_if_exists(fc, field_name):
    # type: (str, str) -> bool
    """Checks a feature class or table for the existance of a field, and, if it exists, deletes it. Returns True if a
    field was found and deleted; returns False if no such field was found.

    Parameters
    ----------
    fc : str
        The name of the feature class or table to search for the field called field_name
    field_name : str
        Name of the field to search for and delete

    Returns
    -------
    bool
        True if a field was found and deleted; False if the field was not found

    """
    if fieldExists(fc, field_name):
        from arcpy import DeleteField_management
        DeleteField_management(fc, field_name)
        return True
    else:
        return False

def indexExists(fc, indexName):
    # type: (str, str) -> bool
    """

    Parameters
    ----------
    fc
    indexName

    Returns
    -------

    """
    indexList = ListIndexNames(fc)
    if indexName in indexList:
        return True
    else:
        return False

# def hasIndex(fc):
#     exists = False
#     indexes = ListIndexNames
#     if indexes != []:
#         exists = True
#     return exists

def ListIndexNames(fc):
    # type: (str) -> List[str]
    """

    Parameters
    ----------
    fc

    Returns
    -------

    """
    from arcpy import ListIndexes
    names = map(lambda x: x.name, ListIndexes(fc))
    return names

def MakeLayer(item, lyrName, wc=""):
    # type: (str, str, str) -> str
    """Makes a layer from a feature class with a given name and optional WHERE clause.

    Parameters
    ----------
    item : str
        Name of the feature class upon which the new layer shall be based
    lyrName : str
        Name of the new layer
    wc : str, optional
        WHERE clause to select a subset of records from item

    Returns
    -------
    str
        The name of the newly-created layer

    """
    from arcpy import Describe, MakeFeatureLayer_management, MakeTableView_management
    #get data type
    dataType = Describe(item).dataType
    #based on data type, create the right kind of layer or table view
    if dataType == "FeatureClass":
        if wc != "":
            MakeFeatureLayer_management(item, lyrName, wc)
        else:
            MakeFeatureLayer_management(item, lyrName)
    else:
        if wc != "":
            MakeTableView_management(item, lyrName, wc)
        else:
            MakeTableView_management(item, lyrName)
    return lyrName


def CalcWithWC(fc, field, python_expression, where_clause, code_block=""):
    """
    Shortcut function to calculate a field for only certain records as selected with a WHERE clause.

    Parameters
    ----------
    fc : str
        Full path to the feature class containing the field to be calculated
    field : str
        Name of the field to be calculated
    python_expression : str
        The Python expression, as a string, to be executed in order to calculate the field
    where_clause : str
        SQL expression, as a string, and omitting everything before WHERE, used to select the records upon which
        a field calulation will be run
    code_block : str, optional
        The Python code block, as a string, to be executed before python_expression
    """
    # type: (str, str, str, str, str) -> None

    from arcpy import MakeFeatureLayer_management, CalculateField_management, Delete_management
    fl_calc = "fl_calc"
    MakeFeatureLayer_management(fc, fl_calc, where_clause)
    CalculateField_management(fl_calc, field, python_expression, "PYTHON_9.3", code_block)
    Delete_management(fl_calc)

def CalcWithWhereClause(fc, field, python_expression, where_clause, code_block=""):
    # type: (str, str, str, str, str) -> None
    """Calls CalcWithWC with same arguments. CalcWithWC: Selects a subset of records of a feature class as defined by a
    WHERE clause, and runs Calculate Field on a selected field with a Python expression and an optional code block."""
    CalcWithWC(fc, field, python_expression, where_clause, code_block)


def writeToText(textFile, stuff):
    # type: (str, Union[str, unicode]) -> None
    """Writes some text to a text file. If the file already exists, append the provided text to the file."""

    if exists(textFile): mode = "a"  # type: str
    else: mode = "w"  # type: str

    try:
        with open(textFile, mode) as f:
            f.writelines(stuff)
    except:
        AddWarning('Function writeToText failed. Provided filename: "%s". Mode: "%s".' % (textFile, mode))

def delim_field_py(field_name):
    # type: (str) -> str
    """Wraps a string in exclamation points for use in ArcGIS Python expressions."""
    return "!%s!" % field_name

def delim_fields_py(field_names):
    # type: (Union[Tuple[str], List[str]]) -> Tuple[str]
    """Wraps in exclamation points each string in a tuple or list for use in ArcGIS Python expressions."""
    return tuple("!%s!" % x for x in field_names)

def __vb_alert_message(title=None, print_as="WARNING"):
    # type: (Optional[str], Optional[str]) -> Optional[unicode]
    """Alerts the user that ArcGIS VB expressions should be avoided due to poetntial compatibility issues.

    Parameters
    ----------
    title : str, optional
        String, such as the name of the calling function, to add at the beginning of the message (followed by ": ")
    print_as : {"WARNING", "MESSAGE", "ERROR"}
        The type of message to print. "ERROR" will raise an exception.

    Returns
    -------
    unicode or None
        The message string or None
    """
    msg = __vb_alert_string
    if title is not None: msg = "%s: %s" % (title, msg)
    if print_as is None: return msg
    elif print_as is "MESSAGE": userMessage(msg)
    elif print_as is "WARNING": userWarning(msg)
    elif print_as is "ERROR":
        from arcpy import AddError
        AddError(msg)
        raise Exception(msg)
    else:
        userWarning(msg)
        userWarning('If the print_as argument of __vb_alert_message is used, its value should be one of "MESSAGE", "WARNING", OR "ERROR"; instead, it was "%s". Defaulting to "WARNING" mode.' % print_as)

def delim_field_vb(field_name, raise_exception=True):
    # type: (str, Union[str, bool]) -> str
    """Wraps a string in square brackets for use in ArcGIS VB expressions. VB in ArcGIS, and therefore this function
    call, should be avoided due to potential compatibility issues."""
    if raise_exception is False:
        __vb_alert_message("delim_field_vb", "WARNING")
    elif raise_exception is "SUPPRESS":
        pass
    else:
        __vb_alert_message("delim_field_vb", "ERROR")
    return "[%s]" % field_name

def delim_fields_vb(field_names, raise_exception=True):
    # type: (Union[Tuple[str], List[str]], Union[bool, str]) -> Tuple[str]
    """Wraps in square brackets each string in a tuple or list for use in ArcGIS VB expressions. VB in ArcGIS, and therefore this function
    call, should be avoided due to potential compatibility issues."""
    if raise_exception is False:
        __vb_alert_message("delim_field_vb", "WARNING")
        return tuple("[%s]" % x for x in field_names)
    elif raise_exception is "SUPPRESS":
        return tuple("[%s]" % x for x in field_names)
    else:
        __vb_alert_message("delim_field_vb", "ERROR")

class FieldInfo:
    """
    Class used to provide a tidy representation of the properties of a field of a table or feature class. It also
    provides a class method to read in field information from a delimited text file.
    """
    def __init__(self, name, type, length, domain):
        self.name = name  # type: str
        self.type = type  # type : str
        self.length = int(length) if length is not "" else ""  # type: Union[int, str]
        self.domain = domain  # type: str

    @classmethod
    def get_from_text(cls, filepath, delimiter="|"):
        # type: (str, str) -> List[FieldInfo]
        """
        Loads field information for a table or feature class from a delimited text file and returns a list of FieldInfo
        objects containing this information, which includes field name, data type, length, and domain.

        Parameters
        ----------
        filepath : str
            The full path to the plaintext file containing the field information
        delimiter : str
            The character(s) used to separate field properties in the text file. Default is a pipe ("|").

        Returns
        -------
        list of FieldInfo
            A list of FieldInfo objects derived from the plaintext file
        """
        with open(filepath, "r") as textfile:
            # TODO: Make, like, readable
            header = textfile.readline().lower().split(delimiter)
            header = [i.strip("\n") for i in header]
            # userMessage(header)
            return [  # Return a list...
                cls(**field_info_dict) for field_info_dict in [  # ...of FieldInfo objects, each constructed from an item in a list of...
                    {  # ...dicts...
                        k: v for k, v in zip(header, row.strip("\n").split(delimiter))  #  ...with keys of column headers (e.g. "NAME") and values from the data...
                    } for row in textfile.readlines()  # ...in each line of the text file.
                ]
            ]  # type: List[FieldInfo]

    @classmethod
    def get_from_feature_class(cls, gdb, feature_class, field=None):
        # type: (str, str, Optional[str]) -> Union[FieldInfo, List[FieldInfo]]
        """
        Loads field information for a table or feature class given the path to or name of a feature class. If the
        `field` parameter is set, a single `FieldInfo` object is returned. Otherwise, a list of `FieldInfo` objects is
        returned.

        Parameters
        ----------
        gdb : str
            The full path to the geodatabase
        feature_class : str
            The name of or a full path to the feature class for which field information should be returned.
        field : str, optional
            The name of the field for which field information should be returned.

        Returns
        -------
        FieldInfo or List[FieldInfo]
            If the `field` parameter is set, a single `FieldInfo` object; otherwise, a list of `FieldInfo` objects
        """
        session = NG911_Session(gdb)
        field_folder = session.fieldsFolderPath
        feature_class = basename(feature_class)
        field_file = join(field_folder, feature_class + ".txt")
        field_infos = cls.get_from_text(field_file)
        if field:
            for fi in field_infos:
                if fi.name == field:
                    return fi
            raise Exception("A FieldInfo object was requested for a field that does not exist: %s.%s" % (feature_class, field))
        else:
            return field_infos

def map_NG911_feature_class(in_table, out_table, conversion_dict, correct_fields=None, field_info_file=None):
    """
    Parameters
    ----------
    in_table : str
        Full path to the non-standards-compliant feature class
    out_table : str
        Full path where the standards-compliant output feature class should be exported
    conversion_dict : dict
        A dict with standard (output) field names as keys and input field names as values
        e.g. { "MSAGComm" : "MSAGCO" }
    correct_fields : list of FieldInfo or None
        A list with the correct field names in the proper order
    field_info_file : str or None
        Full path to a text file containing name, type, length, and domain information for the standard (output) fields

    Returns
    -------
    arcpy.FieldMappings

    """
    from arcpy import ListFields, FieldMappings, FieldMap, AddError
    from os.path import basename

    original_fields = [conversion_dict[key] for key in conversion_dict]
    if correct_fields is None and field_info_file is not None:
        standard_fields = FieldInfo.get_from_text(field_info_file)
    elif correct_fields is not None and field_info_file is None:
        standard_fields = correct_fields
    elif correct_fields is not None and field_info_file is not None:
        standard_fields = correct_fields
        userWarning("correct_fields and field_info_file are both provided. Defaulting to correct_fields and not reading from fields text file.")
    else:
        # correct_fields is None and field_info_file is None
        raise ValueError("correct_fields and field_info_file cannot both be None.")

    if len(original_fields) != len(standard_fields):
        raise ValueError("The number of fields to map in the input feature class \"%s\" does not match the number of fields in the field info file \"%s\"." % (basename(in_table), basename(field_info_file)))

    fms = FieldMappings()
    for out_field in standard_fields:
        in_field = conversion_dict[out_field.name]
        if in_field in [None, "#", ""]:
            continue
        fm = FieldMap()
        try:
            fm.addInputField(in_table, in_field)
        except:
            AddError("Field %s may not exist in input feature class." % in_field)
        fm_outputField = fm.outputField
        fm_outputField.name = out_field.name
        fm_outputField.aliasName = out_field.name
        fm_outputField.type = out_field.type
        fm_outputField.length = int(out_field.length) if out_field.length is not "" else ""
        fm_outputField.domain = out_field.domain if out_field.domain is not "" else ""
        fm.outputField = fm_outputField
        fms.addFieldMap(fm)

    return fms


class DomainInfo:
    """
    Class used to provide a tidy representation of a database domain. It also provides a class method to read in domain
    information from a delimited text file.

    Attributes
    ----------
    domain_name: str
        Name of the domain
    domain_description: str
        Description of the domain
    domain_dict: OrderedDict
        An ordered dictionary of key-value pairs representing code-description pairs from the domain-definition text
        files. These key-value pairs are stored in this ordered dict in the same order they are listed in the domain-
        definition text files.
    """
    def __init__(self, domain_name, domain_description, domain_dict):
        #type: (str, str, OrderedDict[str, str]) -> DomainInfo

        self.domain_name = domain_name  # type: str
        self.domain_description = domain_description  # type: str
        self.domain_dict = domain_dict  # type: OrderedDict[str, str]

    @classmethod
    def get_from_domainfile(cls, filepath, delimiter="|"):
        # type: (str, str) -> DomainInfo
        """
        Loads domain information for a table or feature class from a delimited text file and returns a list of
        DomainInfo objects containing this information, which includes domain name, description, and key-value pairs.

        Parameters
        ----------
        filepath : str
            The full path to the plaintext file containing the domain information
        delimiter : str
            The character(s) used to separate domain properties in the text file. Default is a pipe ("|").

        Returns
        -------
        DomainInfo
            An object containing domain information, including name (domain_name), description (domain_description), and
            key-value pairs (domain_dict)

        """
        from os.path import basename

        domain_name = basename(filepath)[:-12]#.strip("_Domains.txt")

        with open(filepath, "r") as textfile:
            header = textfile.readline().split(delimiter)
            header = [i.strip("\n") for i in header]
            # header[0]: Value
            # header[1]: Domain Description
            domain_description = header[1]
            domain_dict = OrderedDict()
            for line in textfile.readlines():
                line = unicode(line.strip("\n"))
                items = line.split(delimiter)
                domain_dict[items[0]] = items[1]

        return cls(domain_name, domain_description, domain_dict)

    DOMAINS = 0  # TODO: Determine if this line serves any purpose whatsoever