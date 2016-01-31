import sys
import os.path
import keyExtract
import pickle
import numpy as np
from tinydb import TinyDB, Query

cur_dir = os.path.dirname(__file__)
db_loc = cur_dir+"/../database_builder/master-db.json"
text_dir = cur_dir +"/../database_builder/text/"
vector_dir = cur_dir+"/../database_builder/vectors/"
sim_matrix = cur_dir+"/../database_builder/similarity_matrix.pkl"

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

def init_similarity_matrix(firstDOI):
    index_dict = {firstDOI: 0}
    
    return

#figure out name of pdf from db entry, grab text for that pdf, compute vector, save vector in vectors folder
def compute_vector_for_DOI(DOI):
    db = TinyDB(db_loc)
    paper = Query()
    this_paper_dict = db.search(paper.ownDOI == DOI)[0] #returns entry as dictionary
    name = this_paper_dict['filename']
    ##here we call marcellos code
    vector = keyExtract.getRakeKeywords(text_dir+name+'.txt')
    out_path = vector_dir + name+'.pkl'
    output = open(out_path,'wb')
    pickle.dump(vector,output)

#test code for compute_vector_for_DOI
#compute_vector_for_DOI("http://dx.doi.org/10.1109/icsc.2010.19")

    #add a new column and row to similiarity matrix for the new DOI (the vector should already have been computed)
def update_similarity_matrix(newDOI):
    db = TinyDB(db_loc)
    paper = Query()
    this_paper_dict = db.search(paper.ownDOI == newDOI)[0] #returns entry as dictionary
    name = this_paper_dict['filename']
    vector_path = vector_dir + name+'.pkl'
    vec_file = open(vector_path, 'rb')
    newVector = pickle.load(vec_file)
    #now load the matrix
    mat_file = open(sim_matrix,'rb')
    mat_list = pickle.load(mat_file)
    mat = mat_list[0];
    index_dict = mat_list[0];
    
    return


update_similarity_matrix("http://dx.doi.org/10.1109/icsc.2010.19")
