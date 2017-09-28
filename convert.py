import sys
import os
from collections import Iterable
import odml
import nixio as nix


# NOTES:
#   - If a Section has a 'reference' create a property called reference
#   - If a Property has a 'reference' put the reference in the Property's
#   values
#   - Values of type 'URL', 'person', and 'text' are treated as strings
#   - Values of type 'datetime', 'date', and 'time' are converted to string
#   representations
#   - Values of type 'binary' are discarded


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


def write_recurse(odmlseclist, nixparentsec):
    global info
    for odmlsec in odmlseclist:
        info["sections read"] += 1
        secname = odmlsec.name
        type_ = odmlsec.type
        definition = odmlsec.definition
        reference = odmlsec.reference
        repository = odmlsec.repository

        nixsec = nixparentsec.create_section(secname, type_)
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
            if isinstance(odmlvalue, Iterable):
                nixvalues = []
                for v in odmlvalue:
                    if v.dtype == "binary":
                        info["skipped binary values"] += 1
                        continue
                    if v.data is None:
                        info["skipped none values"] += 1
                        continue
                    try:
                        nixv = nix.Value(v.data)
                    except TypeError as exc:
                        print("Unsuported data type: {}".format(type(v.data)))
                        info["type errors"] += 1
                        continue
                    nixv.unit = v.unit
                    nixv.uncertainty = v.uncertainty
                    nixv.reference = v.reference
                    nixvalues.append(nixv)
            else:
                if odmlvalue.dtype == "binary":
                    info["skipped binary values"] += 1
                    info["skipped empty properties"] += 1
                    continue
                if odmlvalue.data is None:
                    info["skipped none values"] += 1
                    info["skipped empty properties"] += 1
                    continue
                try:
                    nixv = nix.Value(odmlvalue.data)
                except TypeError as exc:
                    print("Unsuported data type: {}".format(
                        type(odmlvalue.data)
                    ))
                    info["type errors"] += 1
                    continue
                nixv.unit = odmlvalue.unit
                nixv.uncertainty = odmlvalue.uncertainty
                nixv.reference = odmlvalue.reference
                nixvalues = [nixv]

            if not nixvalues:
                info["skipped empty properties"] += 1
            nixprop = nixsec.create_property(propname, nixvalues)
            info["properties written"] += 1
            nixprop.definition = definition

        write_recurse(odmlsec.sections, nixsec)


def nixwrite(metadata, filename):
    nixfile = nix.File.open(filename, nix.FileMode.Overwrite, backend="h5py")
    write_recurse(metadata.sections, nixfile)


def main(filename):
    metadata = odml.load(filename)
    outfilename = os.path.basename(filename)
    outfilename = outfilename.replace("xml", "nix").replace("odml", "nix")

    if os.path.exists(outfilename):
        yesno = input("File {} already exists. "
                      "Overwrite? ".format(outfilename))
        if yesno.lower() not in ("y", "yes"):
            print("Aborted")
            return
    print("Saving to NIX file...", end=" ", flush=True)
    nixwrite(metadata, outfilename)
    print("Done")


if __name__ == "__main__":
    files = sys.argv[1:]
    for f in files:
        main(f)

    print_info()