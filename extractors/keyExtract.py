# This is the module for extracting keywords and 'smartword'
import re
from collections import Counter

#TODO: Change hardcoded filename to passed argument
def keyWords(doc):
    searchfile = open("05629128.txt", "r")
    for line in searchfile:    
        if "words-" in line: 
            print line
            #keylist = line.split("; ",";","-")
            #keylist = re.findall(regex,line)
            keylist = re.split("\W+",line)
            print keylist
        if "Terms-" in line: print line

#TODO: Change hardcoded filename to passed argument
def smartWords(doc):
    words = re.findall(r'\w+', open('05629128.txt').read().lower())
    #for line in doc:
    #TFIDF code

from rake import Rake
def getRakeKeywords(doc):
    r = Rake('SmartStoplist.txt')
    candidates = r.run(open(doc).read().replace('\n',' '))
    return candidates[:10]
#Tested as follows:
#keyExtract.getRakeKeywords('../convertor/converted-text/00528686.txt')
