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
    excTemplate = env.get_template("exception.xml")

    # FIXME === testing ===
    lic = ldbLicenses.get("3com-microcode", None)
    renderLicense(licTemplate, excTemplate, lic)
    return True

def renderLicense(licTemplate, excTemplate, lic):
    if lic._is_exception:
        tmpl = excTemplate
        xmlFilename = os.path.join("xml", "exceptions", lic._spdx_chosen_id+".xml")
    else:
        tmpl = licTemplate
        xmlFilename = os.path.join("xml", lic._spdx_chosen_id+".xml")

    testTextFilename = os.path.join("text", lic._spdx_chosen_id+".txt")

    try:
        with open(xmlFilename, "w") as f:
            f.write(tmpl.render(lic=lic, listVersionAdded=LISTVERSIONADDED))
    except OSError as e:
        print("Error writing {xmlFilename}: {str(e)}")
        return False

    try:
        with open(testTextFilename, "w") as f:
            f.write(lic._text)
    except OSError as e:
        print("Error writing {testTextFilename}: {str(e)}")
        return False

    return True

