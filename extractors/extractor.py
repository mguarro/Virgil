# This is the module for extracting various attributes from the XML:
# Title / Abstract / Conclusion / Results / Discussion / Keywords

from xml.dom.minidom import parse
from os import path
import re

class PDF:
    def __init__(self, pdfname):
        basepath = path.join("..", "convertor", "converted-xml", pdfname)
        print basepath
        self.titles = getAttribute(basepath, "titles", "title")
        print self.titles
#        self.abstract = getAttribute(pdfname, )

# This function returns all instances of a certain attribute as a string list
# given the name of a PDF, the ID of the XML file, and the name of the
# attribute's XML element
def getAttribute(basepath, xmlID, xmlElement):
    filepath = basepath + "-" + xmlID + ".xml";
    try:
        dom = parse(filepath);
    except Exception:
        print "Failed to find " + xmlID + " in " + filepath
    titles = []
    for node in dom.getElementsByTagName(xmlElement):
        for child in node.childNodes:
            childxml = child.toxml();
            titles.append(childxml)
    return titles

pdf1 = PDF("05571262")
