# This is the module for extracting keywords and 'smartword'
import re
from collections import Counter

# This fuction returns the keyword list contained in a document 
def keyWords(self):
    searchfile = open(self, "r")
    for line in searchfile:    
        if "words-" in line: 
            keylist = re.split("\W+",line)
            #print keylist
            return keylist
        if "Terms-" in line: print line
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