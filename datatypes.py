# SPDX-License-Identifier: Apache-2.0

class SPDXLicense:
    # License details obtained from license-list-data/licenses.json
    # and from license-list-data/exceptions.json
    # _id includes license IDs as well as exception IDs

    def __init__(self):
        super (SPDXLicense, self).__init__()

        self._id = ""
        self._origID = ""
        self._name = ""

class LDBLicense:
    # License details regarding scancode-licensedb licenses

    def __init__(self):
        super(LDBLicense, self).__init__()

        # loaded from scancode-licensedb/docs
        self._key = ""
        self._name = ""
        self._text = ""
        self._category = ""
        self._text_urls = []
        self._spdx_license_key = ""
        self._osi_license_key = ""

        # analyzed later
        self._is_spdx = False
        self._is_exception = False
        self._is_osi = False
        self._spdx_chosen_id = ""
        self._text_processed = ""
