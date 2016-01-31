import sys
import os.path
import keyExtract

db_loc = "../database_builder/master-db/master-db.json"
text_dir = "../database_builder/text/"
vector_dir = "../database_builder/vectors/"

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


#figure out name of pdf from db entry, grab text for that pdf, compute vector, save vector in vectors folder
def compute_vector_for_DOI(DOI):
    db = TinyDB(db_loc)
    paper = Query()
    this_paper_dict = db.search(paper.ownDOI == DOI)[0] #returns entry as dictionary
    name = this_paper_dict['filename']
    ##here we call marcellos code
    vector = keyExtract.getRakeKeywords(text_dir+name+'.txt')
    print type(vector)

#test code for compute_vector_for_DOI

    #add a new column and row to similiarity matrix for the new DOI (the vector should already have been computed)
def update_similarity_matrix(newDOI):
    

    
    
    
    

#add a new column and row to similiarity matrix for the new DOI (the vector should already have been computed)
def update_similarity_matrix(newDOI):
    

