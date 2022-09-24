# SPDX-License-Identifier: Apache-2.0

from jinja2 import Environment, FileSystemLoader

LISTVERSIONADDED = "3.20"

def makeTemplates(ldbLicenses):
    # set up Jinja2 environment
    env = Environment(
        loader = FileSystemLoader("spdxtemplates/"),
        autoescape = False,
    )

    licTemplate = env.get_template("license.xml")

    # FIXME === testing ===
    lic = ldbLicenses.get("3com-microcode", None)
    renderLicense(licTemplate, lic)
    print(lic._text)
    return True

def renderLicense(licTemplate, lic):
   print(licTemplate.render(lic=lic, listVersionAdded=LISTVERSIONADDED))

