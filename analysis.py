# SPDX-License-Identifier: Apache-2.0

def analyzeLDBLics(ldbLicenses, spdxLicenses):
    processedLDBLicenses = {}

    for lic in ldbLicenses.values():
        if lic._spdx_license_key.startswith("LicenseRef-"):
            # FIXME validate that it actually is not yet on SPDX list
            lic._is_spdx = False
            if "exception" in lic._spdx_license_key.lower():
                lic._is_exception = True
            # FIXME assuming not is OSI for now, need to check
            lic._spdx_chosen_id = lic._spdx_license_key.removeprefix("LicenseRef-scancode-")

            # process text to replace line breaks with <p> tags
            lic._text_processed = lic._text.replace("\n\n", "\n</p>\n<p>\n")
            lic._text_processed = lic._text_processed.replace("\n", "\n\t\t\t")

            # add to processed list
            processedLDBLicenses[lic._key] = lic

    return processedLDBLicenses
