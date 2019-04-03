# odML ↔️ NIX metadata conversion tool

This tool reads in [odML](https://g-node.github.io/python-odml/) / 
[NIX](https://g-node.github.io/nix/) files and writes the metadata structure to newly 
created NIX / odML files. When run as a script from the command line, it prints 
information regarding the number of Sections and Properties that were read, written, 
or skipped for various reasons.

For more information on the odML and NIX data formats, please check the sections below.


## Dependencies

* Python 2.7 or 3.5+
* Python packages:
    * odml
    * nixio (>=1.5.0b1)

These dependency packages can be manually installed via the python package manager `pip`:

`pip install odml nixio==1.5.0b3` 

or by manually installing the nix-odML-converter from the repository root:

`python setup.py install`


## Building from source

    git clone https://github.com/G-Node/nix-odML-converter.git
    cd nix-odML-converter
    python setup.py install

## Usage

After installing the package, you can use the `convert.py` script found in the
directory 'nix-odML-converter/nixodmlconverter' that acts as a command line tool.

You can use it to a) import the content of an existing odML file into a NIX file or
b) to export the odML content of a NIX file into a new odML file. 

### Import of odML into a NIX file

From the command line use the `convert.py` script to import the contents of an existing
odML file into a NIX file:

    python nix-odML-convert/nixodmlconverter/convert.py odmlfile.xml nixfile.nix  

The odML file has to be provided in XML format. 

### Export odML from a NIX file

From the command line use the `convert.py` script to export the contents of an existing 
NIX file to a new odML file:

    python nix-odML-convert/nixodmlconverter/convert.py nixfile.nix newodmlfile.xml

### Usage notes

For compatibility with the NIX metadata format, which differs slightly from the 
odML format, the following modifications occur when converting from odML to NIX:

- If a Section has a `reference` create a property called `reference`
- If a Property has a `reference` put the reference in the Property's values
- Values of type `URL`, `person`, and `text` are treated as strings
- Values of type `datetime`, `date`, and `time` are converted to string representations
- Values of type `binary` are discarded
