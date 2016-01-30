# This is the module for extracting titles
from xml.dom.minidom import parse
from os import path

# This function returns all titles as a string list
# given the name of a PDF that's been processed into XML
def getTitles(pdfname):
    filename = pdfname + "-titles.xml";
    pdfpath = path.join("..", "convertor", "converted-xml", filename)
    dom = parse(pdfpath);
    titles = []
    for node in dom.getElementsByTagName('title'):
        for child in node.childNodes:
            childxml = child.toxml();
            titles.append(childxml)
            print childxml
    return titles

returnedtitles = getTitles("05571262");
