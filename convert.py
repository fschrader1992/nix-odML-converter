import sys
import os
import odml
import nixio as nix


info = {"sections read": 0,
        "sections written": 0,
        "properties read": 0,
        "properties written": 0,
        "skipped empty properties": 0,
        "skipped binary values": 0,
        "skipped none values": 0,
        "type errors": 0}


def print_info():
    print("Conversion info")
    print("{sections read}\t Sections were read\n"
          "{sections written}\t Sections were written\n"
          "{properties read}\t Properties were read\n"
          "{properties written}\t Properties were written\n"
          "{skipped empty properties}\t Properties were skipped because they "
          "contained only None or binary values\n"
          "{skipped binary values}\t Values were skipped because they "
          "were of type 'binary'\n"
          "{skipped none values}\t Values were skipped because they were "
          "empty (None)\n"
          "{type errors}\t Type Errors were encountered\n".format(**info))


def convert_datetime(dt):
    return dt.isoformat()


def convert_value(v, dtype):
    global info
    if dtype == "binary":
        info["skipped binary values"] += 1
        return None
    if v is None:
        info["skipped none values"] += 1
        return None
    if dtype in ("date", "time", "datetime"):
        v = convert_datetime(v)
    return v


def odml_to_nix_recurse(odmlseclist, nixparentsec):
    global info
    for odmlsec in odmlseclist:
        info["sections read"] += 1
        secname = odmlsec.name
        definition = odmlsec.definition
        reference = odmlsec.reference
        repository = odmlsec.repository

        nixsec = nixparentsec.create_section(secname, odmlsec.type, oid=odmlsec.id)
        info["sections written"] += 1
        nixsec.definition = definition
        if reference is not None:
            nixsec["reference"] = reference
        if repository is not None:
            nixsec["repository"] = repository

        for odmlprop in odmlsec.properties:
            info["properties read"] += 1
            propname = odmlprop.name
            definition = odmlprop.definition
            odmlvalue = odmlprop.value
            nixvalues = []
            for v in odmlvalue:
                nixv = convert_value(v, odmlprop.dtype)
                if nixv is not None:
                    nixvalues.append(nixv)

            if not nixvalues:
                info["skipped empty properties"] += 1
                continue
            nixprop = nixsec.create_property(propname, nixvalues, oid=odmlprop.id)
            info["properties written"] += 1
            nixprop.definition = definition
            nixprop.unit = odmlprop.unit
            nixprop.uncertainty = odmlprop.uncertainty
            nixprop.reference = odmlprop.reference
            nixprop.odml_type = nix.property.OdmlType[odmlprop.dtype]
            nixprop.value_origin = odmlprop.value_origin
            nixprop.dependency = odmlprop.dependency
            nixprop.dependency_value = odmlprop.dependency_value

        odml_to_nix_recurse(odmlsec.sections, nixsec)

def write_odml_doc(odmldoc, nixfile):
    nixsec = nixfile.create_section('odML document', 'odML document', oid=odmldoc.id)
    info["sections written"] += 1
    nixsec.author = odmldoc.author
    nixsec.date = odmldoc.date
    nixsec.version = odmldoc.version
    nixsec.repository = odmldoc.repository
    return nixsec


def nixwrite(odml_doc, filename):
    nixfile = nix.File.open(filename, nix.FileMode.Overwrite)

    nix_document_section = write_odml_doc(odml_doc, nixfile)
    odml_to_nix_recurse(odml_doc.sections, nix_document_section)


############### NIX -> ODML #################

def odmlwrite(nix_file, filename):

    odml_doc = get_odml_doc(nix_file)
    nix_to_odml_recurse(nix)

def get_odml_doc(nix_file):

    # identify odml document section in nix file
    doc_section = nix_file.find_sections(lambda x: x.name=='odml document', limit=1)
    if not doc_section:
        raise ValueError('No odML document section present in nix file.')
    elif len(doc_section) > 1:
        raise ValueError('More than one ({}) document section present in nix file.'
                         ''.format(len(doc_section)))
    doc_section = doc_section[0]

    attributes = ['id', 'author', 'version', 'repository', 'date']
    return odml.Document(**{(att, getattr(doc_section, att)) for att in attributes})


def nix_to_odml_recurse(nix_section_list, nix_section):
    for nix_sec in nix_section_list:
        # info["sections read"] += 1
        secname = nix_sec.name
        definition = nix_sec.definition
        reference = nix_sec.reference
        repository = nix_sec.repository

        odml_sec = odml.Section(secname, definition=definition, reference=reference,
                                oid=nix_sec.id, repository=repository)
        # info["sections written"] += 1
        if reference is not None:
            nixsec["reference"] = reference
        if repository is not None:
            nixsec["repository"] = repository

        for odmlprop in odmlsec.properties:
            info["properties read"] += 1
            propname = odmlprop.name
            definition = odmlprop.definition
            odmlvalue = odmlprop.value
            nixvalues = []
            for v in odmlvalue:
                nixv = convert_value(v, odmlprop.dtype)
                if nixv:
                    nixvalues.append(nixv)

            if not nixvalues:
                info["skipped empty properties"] += 1
                continue
            nixprop = nixsec.create_property(propname, nixvalues, oid=odmlprop.id)
            info["properties written"] += 1
            nixprop.definition = definition
            nixprop.unit = odmlprop.unit
            nixprop.uncertainty = odmlprop.uncertainty
            nixprop.reference = odmlprop.reference
            nixprop.dtype = odmlprop.dtype
            nixprop.value_origin = odmlprop.value_origin
            nixprop.dependency = odmlprop.dependency
            nixprop.dependency_value = odmlprop.dependency_value

        odml_to_nix_recurse(odmlsec.sections, nixsec)


def main(filename):
    # Determine input and output format
    file_base, file_ext = os.path.splitext(filename)
    if file_ext in ['.xml', '.odml']:
        output_format = '.nix'
    elif file_ext in ['.nix']:
        output_format = '.xml'
    else:
        raise ValueError('Unknown file format {}'.format(file_ext))

    # Check output file
    outfilename = file_base + output_format
    if os.path.exists(outfilename):
        yesno = input("File {} already exists. "
                      "Overwrite? ".format(outfilename))
        if yesno.lower() not in ("y", "yes"):
            print("Aborted")
            return

    # Load, convert and save to new format
    print("Saving to {} file...".format(output_format), end=" ", flush=True)
    if output_format in ['.nix']:
        odml_doc = odml.load(filename)
        nixwrite(odml_doc, outfilename)
    elif output_format in ['.xml', '.odml']:
        nix_file = nix.File.open(filename, nix.FileMode.ReadOnly)
        odmlwrite(nix_file, outfilename)
    else:
        raise ValueError('Unknown file format {}'.format(output_format))

    print("Done")


if __name__ == "__main__":
    files = sys.argv[1:]
    for f in files:
        main(f)

    print_info()
