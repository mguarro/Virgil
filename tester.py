# This is a test script to check for keyword extraction and distance computation 
# of two keyword vectors. The script uses two texts as input, extracts their keywords 
# as vectors, normalizes the vectors, calculates the 'distance' between the two vectors,
# and prints the resultant vector.
# 
# Written for Virgil by Marcello Guarro

import sys
import os.path
import distance.keyExtract as keyExt
import distance.distance as dist
from pprint import pprint

test1 = "merkel.txt"
test2 = "merkel2.txt"

rakeList1 = keyExt.getRakeKeywords(test1)
rakeList2 = keyExt.getRakeKeywords(test2)

vect1 = dist.normVectorGen(rakeList1)
vect2 = dist.normVectorGen(rakeList2)

pprint(dist.vectorMult(vect1,vect2))

