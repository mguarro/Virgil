# This is the module for extracting keywords and 'smartword'
import re
import nltk
from collections import Counter
import rake
import operator
from rake import Rake
from os import path

cur_dir = path.dirname(__file__)
# This function returns the keyword list contained in a document 
def keyWords(self):
    searchfile = open(self, "r")
    for line in searchfile:    
        if "words-" in line: 
            keylist = re.split("\W+",line)
            keylist.pop(0)
            keylist.pop()
            return keylist
        if "Terms-" in line: 
            keylist = re.split("\W+",line)
            keylist.pop(0)
            keylist.pop()
            return keylist

# This function returns a list of words with their associated frequency
# in the following format: ('word', frequency)
def smartWords(self):
    stop1 = open(path.join('extractors/static', 'FoxStoplist.txt'), "r")
    stop2 = open(path.join('extractors/static', 'SmartStoplist.txt'), "r")
    words = re.findall(r'\w+', open(self).read().lower())
    print len(words)
    ref1 = re.findall(r'\w+', stop1.read().lower())
    ref3 = re.findall(r'\w+', stop2.read().lower())
    stopwords = nltk.corpus.stopwords.words('english') + ref1 + ref3
    stopwordsfree_words = [word for word in words if word not in stopwords and len(word) >= 5 and len(word) <= 10] 
    return Counter(stopwordsfree_words).most_common(15) 

def getRakeKeywords(doc):
    r = Rake(path.join('', cur_dir+'/SmartStoplist.txt'))
    candidates = r.run(open(doc).read().replace('\n',' '))
    return candidates[:300]


