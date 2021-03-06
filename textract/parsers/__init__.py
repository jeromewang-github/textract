import os
import importlib

from .. import exceptions


def process(filename, **kwargs):
    """This is the core function used for parsing. It routes the filename
    to the appropriate parser and returns the result.
    """

    # make sure the filename exists
    if not os.path.exists(filename):
        raise exceptions.MissingFileError(filename)

    # get the filename extension, which is something like .docx for
    # example, and import the module dynamically using importlib. This
    # is a relative import so the name of the package is necessary
    root, ext = os.path.splitext(filename)
    ext = ext.lower()

    # to avoid conflicts with packages that are installed globally
    # (e.g. python's json module), all extension parser modules have
    # the _parser extension
    module = ext + '_parser'
    try:
        filetype_module = importlib.import_module(module, 'textract.parsers')
    except ImportError, e:
        raise exceptions.ExtensionNotSupported(ext)

    return filetype_module.extract(filename, **kwargs)
