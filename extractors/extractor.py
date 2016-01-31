# This is the module for extracting various attributes from the XML:
# Titles / Abstract / Conclusion / Results / Discussion / Keywords

from xml.dom.minidom import parse
from os import path

abconst = "Abstract"

class PDF:
    def __init__(self, pdfName):
        basepath = path.join("..", "convertor", "converted-xml", pdfName)
        print basepath
        titlesDOM = getDOM(basepath, "titles")
        self.titles = getTitles(titlesDOM)
        regionsDOM = getDOM(basepath, "regions")
        self.abstract = getAbstract(regionsDOM)

# gets the DOM of an XML file
def getDOM(basepath, xmlID):
    filepath = xmlPath(basepath, xmlID)
    try:
        dom = parse(filepath)
    except Exception:
        print "Failed to find " + xmlID + " in " + filepath
    return dom

# gets titles from a DOM
def getTitles(dom):
    titles = []
    for node in dom.getElementsByTagName("title"):
        for child in node.childNodes:
            childxml = child.toxml();
            titles.append(childxml)
    return titles

# gets an abstract from a DOM
def getAbstract(dom):
    for node in dom.getElementsByTagName("region"):
        for child in node.childNodes:
            childxml = child.toxml()
            childwords = childxml.split(" ")
            if not isTitleCase(childwords) and len(childwords) >= 1:
                if childwords[0] == abconst:
                    childxml = trimAbstract(childxml)
                    return childxml;
    return "No abstract identified"

# trims "Abstract - " and similar from the beginning of an abstract
def trimAbstract(abstract):
    if abstract[0:len(abconst)] != abconst:
        print "Miscall of trimAbstract:"
        print abstract
    abstract = abstract[len(abconst):len(abstract)]
    for i in range(len(abstract)):
        if isalpha(abstract[i]):
            abstract = abstract[i:len(abstract)]
            return abstract

# helper function that checks to see whether a given character
# is an English-alphabet letter
def isalpha(char):
    if len(char) != 1:
        print "Miscall of isalpha:"
        print char
    if char.islower():
        return True
    elif char.isupper():
        return True
    else:
        return False

# helper function that checks to see whether a given phrase is likely to be
# title case (gives false negatives but not false positives)
def isTitleCase(words):
    for word in words:
        if len(word) >= 4:
            if word[0].islower():
                return False
    return True

# helper function that creates a path from a basepath and an xmlID
def xmlPath(basepath, xmlID):
    return basepath + "-" + xmlID + ".xml"

pdfs = {"05571262", "05290726"}

for p in pdfs:
    thispdf = PDF(p)
    print thispdf.titles
    print thispdf.abstract
