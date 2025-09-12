from warnings import warn
from arcpy import AddMessage, AddWarning
try:
    from typing import Optional, Union
except:
    pass

TOOLKIT_VERSION = "0.6.1"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Alert user if the print statements in userMessage and userWarning have been disabled. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print_to_console_and_arcpy_messages = False
print_debug_messages = False

if not print_to_console_and_arcpy_messages:
    try:
        print("PROGRAMMER NOTICE: The print() calls in userMessage and userWarning are disabled.")
        AddMessage("PROGRAMMER NOTICE: The print() calls in userMessage and userWarning are disabled.")
    except:
        pass

def userMessage(msg, debug_only=False):
    # type: (Union[str, unicode], Optional[bool]) -> None
    """
    Convenience function to print a message to the Python console and/or the tool interface in Arc. Its exact behavior
    depends upon the values of the module-level variables `print_to_console_and_arcpy_messages` and
    `print_debug_messages`.

    If `print_to_console_and_arcpy_messages` is True, output from this function will be output both in the Python
    console as well as through an arcpy message (and therefore in the Arc tool, if applicable). If it is `False`, `msg`
    will only be output through an arcpy message (and therefore in the Arc tool, if applicable).

    Parameters
    ----------
    msg : str or unicode
        The string to be printed as a message. Note that this should not be used for messages describing problems. Non-
        fatal problems should be brought forth as warnings (such as by the `userWarning` funciton in this module), and
        fatal problems should be brought forth as arcpy errors and/or by raising a Python exception.
    debug_only : bool
        If this parameter is True, the message will be printed if the module-level variable `print_debug_messages` is
        is also True. If this parameter is False, the message will be printed as normal. As a shortcut, `debugMessage`
        can be used to automatically invoke this function with this parameter set to False.
    """
    # Display a message via the tool's messages and/or the Python console
    if debug_only is True and print_debug_messages is False:
        return
    elif debug_only is True and print_debug_messages is True:
        msg = "DEBUG: %s" % msg
    try:
        # Try to add a tool message
        AddMessage(msg)
    except:
        # If adding a tool message fails, print the message to Python console instead
        print(msg)
    else:
        # If adding a tool message succeeds and print_to_console_and_arcpy_messages is True, print to Python console
        if print_to_console_and_arcpy_messages: print(msg)


def debugMessage(msg):
    """
    Equivalent to `userMessage(msg, True)`.

    Parameters
    ----------
    msg : str or unicode
        The text content of the message.
    """
    userMessage(msg, True)


def userWarning(msg):
    """
    Much like sending a message (see `userMessage` documentation in this module), but sends it as a warning, which
    causes the Arc tool to display a yellow triangle containing an exclamation point upon completion and also (if
    `print_to_console_and_arcpy_messages` is `True`) generates a Python warning which is printed to the console.

    Parameters
    ----------
    msg : str or unicode
        The text content of the warning
    """
    # Display a WARNING via the tool's messages and/or the Python console
    try:
        # Try to add a tool warning
        AddWarning(msg)
    except:
        # If adding a tool warning fails, print the warning to Python console instead
        warn(msg)
    else:
        # If adding a tool warning succeeds and print_to_console_and_arcpy_messages is True, print to Python console
        if print_to_console_and_arcpy_messages: warn(msg)

userMessage("Oklahoma NG911 GIS Toolkit - Version %s" % TOOLKIT_VERSION)