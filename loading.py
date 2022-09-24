# SPDX-License-Identifier: Apache-2.0

import json
import os

from datatypes import SPDXLicense, LDBLicense

def loadSPDXLicenseList(licensesFilename, exceptionsFilename):
    spdxLicenses = {}

    try:
        with open(licensesFilename, 'r') as f:
            js = json.load(f)
            lics = js.get("licenses", [])
            for lic in lics:
                l = SPDXLicense()
                # record all-lowercase ID to mirror scancode-licensedb
                origID = lic.get("licenseId", None)
                l._id = origID.lower()
                l._origID = origID
                l._name = lic.get("name", None)
                if not l._id:
                    print(f"Error: missing licenseId for {l._name}")
                    continue
                spdxLicenses[l._id] = l

    except json.decoder.JSONDecodeError as e:
        print(f"Error loading or parsing {licensesFilename}: {str(e)}")
        return {}

    try:
        with open(exceptionsFilename, 'r') as f:
            js = json.load(f)
            excs = js.get("exceptions", [])
            for exc in excs:
                e = SPDXLicense()
                e._id = exc.get("licenseExceptionId", None)
                e._name = exc.get("name", None)
                if not e._id:
                    print(f"Error: missing licenseExceptionId for {e._name}")
                    continue
                spdxLicenses[e._id] = e

            return spdxLicenses

    except json.decoder.JSONDecodeError as e:
        print(f"Error loading or parsing {exceptionsFilename}: {str(e)}")
        return {}

def loadLDBLicenseList(ldbDocsDir):
    ldbLicenses = {}

    ignoreFiles = [
        "CNAME",
        "help",
        "index",
        "static",
    ]

    # catalog which licenses we've got based on filenames
    allfiles = os.listdir(ldbDocsDir)
    filekeys = sorted(list(set([os.path.splitext(x)[0] for x in allfiles])))
    lickeys = [x for x in filekeys if x not in ignoreFiles]

    # walk through files and gather info
    for lkey in lickeys:
        lic = LDBLicense()
        lic._key = lkey

        ltextfile = os.path.join(ldbDocsDir, lkey + ".LICENSE")
        try:
            with open(ltextfile, "r") as f:
                lic._text = f.read().strip()
        except OSError as e:
            print(f"Error loading or reading {ltextfile}: {str(e)}")
            return {}

        ljsonfile = os.path.join(ldbDocsDir, lkey + ".json")
        try:
            with open (ljsonfile, "r") as f:
                js = json.load(f)
                # check that the "key" value matches the filename
                found_key = js.get("key", "")
                if not found_key:
                    print(f"Error: no 'key' found in {ljsonfile}")
                    continue
                if found_key != lkey:
                    print(f"Error: {ljsonfile} 'key' {found_key} did not match filename key {lkey}")
                    continue
                # looks good, read other values
                lic._name = js.get("name", "")
                lic._category = js.get("category", "")
                lic._text_urls = js.get("text_urls", [])
                lic._spdx_license_key = js.get("spdx_license_key", "")
                lic._osi_license_key = js.get("osi_license_key", "")

                ldbLicenses[lic._key] = lic

        except OSError as e:
            print(f"Error loading or reading {ljsonfile}: {str(e)}")
            return {}

    return ldbLicenses

