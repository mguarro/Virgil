import sys
import os.path
#import keyExtract


def normVectorGen(keyList):
    normSum = 0
    normKeyList = []

    for i in keyList:
        normSum = normSum + i[1]

    for i in keyList:
        normKeyList.append((i[0],i[1] / normSum))

    return normKeyList

def vectorMult(normKeyList1,normKeyList2):
    vectorResult = []

    for i in normKeyList1:
        for j in normKeyList2:
            if i[0] == j[0]:
                vectorResult.append((i[0],i[1]*j[1]))

    return vectorResult
