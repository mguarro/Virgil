import sys
import os.path
import extractors.keyExtract as keyExt
import distance.distance as dist
from pprint import pprint

#import RAKE

#test = "05629128.txt"
test1 = "merkel.txt"
test2 = "merkel2.txt"

#print keyExtract.keyWords(test)
#print keyExtract.smartWords(test)
#pprint(keyExtract.smartWords(test))
#pprint(keyExtract.getRakeKeywords(test))
rakeList1 = keyExt.getRakeKeywords(test1)
rakeList2 = keyExt.getRakeKeywords(test2)

vect1 = dist.normVectorGen(rakeList1)
vect2 = dist.normVectorGen(rakeList2)

pprint(dist.vectorMult(vect1,vect2))

