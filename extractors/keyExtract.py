# This is the module for extracting keywords and 'smartword'
import re
import nltk
from collections import Counter
from rake import Rake
from os import path

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
    stop1 = open(path.join('static', 'FoxStoplist.txt'), "r")
    stop2 = open(path.join('static', 'SmartStoplist.txt'), "r")
    #dic = open(path.join('static', 'VirgilStoplist.txt'), "r")
    words = re.findall(r'\w+', open(self).read().lower())
    ref1 = re.findall(r'\w+', stop1.read().lower())
    #ref2 = re.findall(r'\w+', dic.read().lower())
    ref3 = re.findall(r'\w+', stop2.read().lower())
    #pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
    #print Counter(words).most_common()[:-60+100:-1]
    #stopwords = nltk.corpus.stopwords.words('english') + ref1 + ref2 + ref3

    stopwords = nltk.corpus.stopwords.words('english') + ref1 + ref3
    #wordList = [i for i in words.split() if i not in stop]
    stopwordsfree_words = [word for word in words if word not in stopwords and len(word) >= 5 and len(word) <= 10]
    #wordList = Counter(words).most_common()[:-60+100:-1]
    #stopList = open(,"r")
    #for word in wordList

        #smartWordList =
    #return Counter(wordList).most_common()[:-60+100:-1] 
    return Counter(stopwordsfree_words).most_common(15) 


def getRakeKeywords(doc):
    r = Rake(path.join('static', 'SmartStoplist.txt'))
    candidates = r.run(open(doc).read().replace('\n',' '))
    return candidates[:10]

#Tested as follows:
#keyExtract.getRakeKeywords('../convertor/converted-text/00528686.txt')

