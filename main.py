# SPDX-License-Identifier: Apache-2.0

import sys

from loading import loadSPDXLicenseList, loadLDBLicenseList
from analysis import analyzeLDBLics
from templates import makeTemplates

def main():
    # load license lists
    spdxLicenses = loadSPDXLicenseList("../license-list-data/json/licenses.json", "../license-list-data/json/exceptions.json")
    if not spdxLicenses:
        print("Exiting before analyzing licenses.")
        sys.exit(1)

    ldbLicenses = loadLDBLicenseList("../scancode-licensedb/docs")
    if not ldbLicenses:
        print("Exiting before analyzing licenses.")
        sys.exit(1)

    # analyze Scancode LicenseDB licenses
    processedLDBLicenses = analyzeLDBLics(ldbLicenses, spdxLicenses)
    if not processedLDBLicenses:
        print("Exiting before creating templates.")
        sys.exit(1)

    # create templates
    retval = makeTemplates(processedLDBLicenses)
    if not retval:
        print("Exiting with error during template creation.")
        sys.exit(1)

    print("Done.")

if __name__ == "__main__":
    main()
