# This is the module for extracting keywords and 'smartword'
import re
from collections import Counter

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

def smartWords(doc):
    words = re.findall(r'\w+', open('05629128.txt').read().lower())
    for line in doc:
    #TFIDF code