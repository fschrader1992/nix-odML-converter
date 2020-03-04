# Changelog

Used to document all changes from previous releases and collect changes until the next release.

# Version 0.0.7
- Update imports from odml where the package structure has changed with version 1.4.4.

# Version 0.0.6
- Moved `info.json` to the `nixodmlconverter` folder to enable import of the package version number.
- Removed `FORMAT_VERSION` from `info.json` since that is odML file format specific and should be defined in the odML python package only.

# Version 0.0.5

## Updates
- The setup script now installs the converter as a command line script called `nixodmlconverter`.
- Major README and docstring updates.
- enables the export of any metadata section from NIX. See #17 for details.

## Fixes
- user input is now available with Python 2 as well.
- odML `Property.values` can now be imported into NIX if they contain non-ascii characters.
- in a odml->nix conversion the 'omega' symbol is sanitized to 'Ohm' if it is used in a `Property.unit`. Otherwise nixpy breaks when using Python 2.
- removes the usage of the deprecated odml attribute `Property.value` and refactors the command line output for the user.
