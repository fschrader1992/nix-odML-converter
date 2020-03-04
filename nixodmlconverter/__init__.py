import warnings

from sys import version_info as _python_version

from .info import VERSION

if _python_version.major < 3 or _python_version.major == 3 and _python_version.minor < 6:
    msg = "The '%s' package is not tested with your Python version. " % __name__
    msg += "Please consider upgrading to the latest Python distribution."
    warnings.warn(msg)

__version__ = VERSION
