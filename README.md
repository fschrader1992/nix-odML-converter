# odML ↔️ NIX metadata conversion tool

This tool reads in odML / NIX files and writes the metadata structure to newly created NIX / odML files.
When run as a script from the command line, it prints information regarding the number of Sections and Properties that were read, written, or skipped for various reasons.

For compatibility with the NIX metadata format, which differs slightly from the odML format, the following modifications occur when converting from odML to NIX:
- If a Section has a `reference` create a property called `reference`
- If a Property has a `reference` put the reference in the Property's
    values
- Values of type `URL`, `person`, and `text` are treated as strings
- Values of type `datetime`, `date`, and `time` are converted to string
    representations
- Values of type `binary` are discarded
