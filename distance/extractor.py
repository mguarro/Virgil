# This is the module for extracting various attributes from the XML:
# Titles / Abstract / Conclusion / Results / Discussion / Keywords

from xml.dom.minidom import parse
from os import path
import sys
import codecs
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

abconst = "Abstract"

class PDF:
    def __init__(self, pdfName):
        basepath = path.join("..", "convertor", "converted-xml", pdfName)
        print basepath
        titlesDOM = getDOM(basepath, "titles")
        self.titles = getTitles(titlesDOM)
        regionsDOM = getDOM(basepath, "regions")
        self.abstract = getAbstract(regionsDOM)
    def __str__(self):
        string = ""
        if self.titles == None:
            string += "No title identified\n"
        else:
            if len(self.titles) == 1:
                string += self.titles[0] + "\n"
            else:
                for i in range(len(titles)):
                    string += "Title " + (i+1) + ": " + titles[i] + "\n"
        if self.abstract == None:
            string += "No abstract identified\n"
        else:
            string += self.abstract + "\n"
        return string

# gets the DOM of an XML file
def getDOM(basepath, xmlID):
    filepath = xmlPath(basepath, xmlID)
    try:
        dom = parse(filepath)
    except Exception:
#        print "There is no file at " + filepath
        return None
    return dom

# gets titles from a DOM
def getTitles(dom):
    if dom == None:
        return None
    titles = []
    for node in dom.getElementsByTagName("title"):
        for child in node.childNodes:
            childxml = child.toxml();
            titles.append(childxml)
    return titles

# gets an abstract from a DOM
def getAbstract(dom):
    if dom == None:
        return None
    for node in dom.getElementsByTagName("region"):
        for child in node.childNodes:
            childxml = child.toxml()
            childwords = childxml.split(" ")
            if not isTitleCase(childwords) and len(childwords) >= 1:
                if startsWithAbconst(childxml):
                    childxml = trimAbstract(childxml)
                    return childxml;
    return None

# gets a conclusion from a DOM
def getConclusion(dom):
    if dom == None:
        return None
    # I'm working on the conclusion extractor now

# trims "Abstract - " and similar from the beginning of an abstract
def trimAbstract(abstract):
    if not startsWithAbconst(abstract):
        return None
    abstract = abstract[len(abconst):len(abstract)]
    for i in range(len(abstract)):
        if isalpha(abstract[i]):
            abstract = abstract[i:len(abstract)]
            return abstract

# helper function that checks to see whether a given string
# has "Abstract" at the beginning
def startsWithAbconst(abstract):
    if abstract[0:len(abconst)] == abconst:
        return True
    return False

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
# in title case (gives false negatives but not false positives)
def isTitleCase(words):
    for word in words:
        if len(word) >= 4:
            if word[0].islower():
                return False
    return True

# helper function that creates a path from a basepath and an xmlID
def xmlPath(basepath, xmlID):
    return basepath + "-" + xmlID + ".xml"

pdfs = ["05571262", "05290726", "07001093"]

for p in pdfs:
    thispdf = PDF(p)
    print thispdf
