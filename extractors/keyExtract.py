# This is the module for extracting keywords and 'smartword'
import re
from collections import Counter
from rake import Rake

# This fuction returns the keyword list contained in a document 
def keyWords(self):
    searchfile = open(self, "r")
    for line in searchfile:    
        if "words-" in line: 
            keylist = re.split("\W+",line)
            #print keylist
            return keylist
        if "Terms-" in line: 
            #print line
            keylist = re.split("\W+",line)
            #print keylist
            return keylist

# This fuction returns a list of words with their associated frequency
# in the following format: ('word', frequency)
def smartWords(self):
    searchfile = open(self, "r")
    words = re.findall(r'\w+', open(self).read().lower())
    #print Counter(words).most_common()[:-60+100:-1] 
    return Counter(words).most_common()[:-60+100:-1] 


def getRakeKeywords(doc):
    r = rake.Rake('SmartStoplist.txt')
    candidates = r.run(open(doc).read().replace('\n',' '))
    return candidates[:10]

#Tested as follows:
#keyExtract.getRakeKeywords('../convertor/converted-text/00528686.txt')

