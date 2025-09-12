"""
Specialized exception and error classes for NG911.
"""

from time import strftime

class NG911Exception (Exception):
    """Base class for NG911 exceptions (not data-related errors) that should halt execution."""
    def __init__(self):
        pass

class NG911DataIssue:
    """Base class for NG911 data-related issues (not execution-halting exceptions)."""

    class NG911DataIssueSeverity:
        ERROR = "Error"
        NOTICE = "Notice"

    def __init__(self):
        self.date = strftime("%Y/%m/%d")

class NG911FieldValueError (NG911DataError):
    """NG911 error class for errors relating to field values in tables/feature classes."""

    def __init__(self, code, description, severity, check, layer, field, feature, str_params=None):
        NG911DataError.__init__(self)
        self.code = code
        self._description = description
        self.severity = severity
        self.check = check
        self.layer = layer
        self.field = field
        self.feature = feature
        self.str_params = str_params

    @property
    def description(self):
        if self.str_params:
            return self._description % self.str_params
        else:
            return self._description

    @property
    def message(self):
        return "%s %s: %s" % (self.severity, self.code, self.description)

    @classmethod
    def f1_parity_null_error(cls, layer, field, feature):
        return cls(
            code="F1",
            description="Could not execute parity check due to null values.",
            severity="ERROR",
            check="Check Parity",
            layer=layer,
            field=field,
            feature=feature
        )

    @classmethod
    def f2_address_range_null_error(cls, layer, field, feature):
        return cls("F2", "One or more address ranges are null.", "ERROR", "Check Parity", layer, field, feature)

    @classmethod
    def f3_rclside_n_error(cls, layer, field, feature):
        return cls("F3", "RCLSide set to N, but RCLMatch has a valid NGSEGID. RCLSide should be either R or L.", "ERROR", "Check Address Point GEOMSAG", layer, field, feature)

    @classmethod
    def f4_duplicate_geomsag_error(cls, layer, field, feature, str_params):
        return cls("F4", "Point duplicates GEOMSAG with RCLMatch record %s on %s side.", "ERROR", "Check Address Point GEOMSAG")

class NG911TemplateError (NG911DataError):
    """NG911 error class for errors relating to the template."""

    code = None
    description = None
    category = None
    severity = None
    check = None

    def __init__(self):
        NG911DataError.__init__(self)
