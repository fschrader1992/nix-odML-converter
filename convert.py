import sys
import os
from collections import Iterable
import odml
import nixio as nix


# NOTES:
#   - If a Section has a 'reference' create a property called reference
#   - If a Property has a 'reference' put the reference in the Property's
#   values

def write_recurse(odmlseclist, nixparentsec):
    for odmlsec in odmlseclist:
        secname = odmlsec.name
        type_ = odmlsec.type
        definition = odmlsec.definition
        reference = odmlsec.reference
        repository = odmlsec.repository

        nixsec = nixparentsec.create_section(secname, type_)
        nixsec.definition = definition
        if reference is not None:
            nixsec["reference"] = reference
        if repository is not None:
            nixsec["repository"] = repository

        for odmlprop in odmlsec.properties:
            propname = odmlprop.name
            definition = odmlprop.definition
            odmlvalue = odmlprop.value
            # dtype = value.dtype
            if isinstance(odmlvalue, Iterable):
                nixvalues = []
                for v in odmlvalue:
                    nixv = nix.Value(v.data)
                    nixv.unit = v.unit
                    nixv.uncertainty = v.uncertainty
                    nixv.reference = v.reference
                    nixvalues.append(nixv)
            else:
                nixv = nix.Value(odmlvalue.data)
                nixv.unit = odmlvalue.unit
                nixv.uncertainty = odmlvalue.uncertainty
                nixv.reference = odmlvalue.reference
                nixvalues = [nixv]

            nixprop = nixsec.create_property(propname, nixvalues)
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
