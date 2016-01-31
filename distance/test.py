import sys
import os.path
import keyExtract
from pprint import pprint

#import RAKE

test = "05629128.txt"
#test = "merkel.txt"
print keyExtract.keyWords(test)
#print keyExtract.smartWords(test)
pprint(keyExtract.smartWords(test))
#pprint(keyExtract.getRakeKeywords(test))
rakeList = keyExtract.getRakeKeywords(test)

normSum = 0

for i in rakeList:
    normSum = normSum + i[1]

newList = []

for i in rakeList:
    newList.append((i[0],i[1] / normSum))
    #print i[1]

nSum = 0

for i in newList:
    nSum = nSum + i[1]

print nSum


#print rakeList[1][1]

import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
 sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

# Info:
# cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
# __file__ fails if script is called in different ways on Windows
# __file__ fails if someone does os.chdir() before
# sys.argv[0] also fails because it doesn't not always contains the path

#import RAKE.rake
