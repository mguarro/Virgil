import sys
import os.path
import keyExtract
import pickle
import numpy as np
from tinydb import TinyDB, Query

#in order for your shit not to break, you must follow the following order of operations upon receiving a new pdf:
#1: call process_and_add_one(path_to_pdf)
#2: call distance_add_new_DOI(DOI) from this module
#
#also, if it is the first paper you are adding, you must call:
#init_similarity_matrix(firstDOI) after doing step 1

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

def vector_mult_and_add(keylist1,keylist2):
    sum = 0
    for i in keylist1:
        for j in keylist2:
            if i[0] == j[0]:
                sum = sum+i[1]*j[1]

#initialize similarity matrix after you process the first DOI
def init_similarity_matrix(firstDOI):
    index_dict = {firstDOI: 0}
    mat = np.ones(1)
    mat_list = [index_dict,mat]
    output = open(sim_matrix,'wb')
    pickle.dump(mat_list,output)
    return None

#figure out name of pdf from db entry, grab text for that pdf, compute vector, save vector in vectors folder
def compute_vector_for_DOI(DOI):
    db = TinyDB(db_loc)
    paper = Query()
    this_paper_dict = db.search(paper.ownDOI == DOI)[0] #returns entry as dictionary
    name = this_paper_dict['filename']
    ##here we call marcellos code
    vector = keyExtract.getRakeKeywords(text_dir+name+'.txt')
    vectore = normVectorGen(vector)
    out_path = vector_dir + name+'.pkl'
    output = open(out_path,'wb')
    pickle.dump(vector,output)

#test code for compute_vector_for_DOI
#compute_vector_for_DOI("http://dx.doi.org/10.1109/icsc.2010.19")

    #add a new column and row to similiarity matrix for the new DOI (the vector should already have been computed)
def update_similarity_matrix(newDOI):
    if(os.path.isfile(sim_matrix)):    
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
        index_dict = mat_list[0];
        mat = mat_list[1];
        if newDOI in index_dict:
            return False
        
        sizemat =   np.size(mat)
        print sizemat
        if sizemat == 1:
            num_ent = 1
        else:
            num_ent = sizemat[0]
            
        index_dict[newDOI] = num_ent

        #extend the matrix to appropriate size
        mat = np.vstack((mat,np.zeros((1,num_ent))))
        mat = np.hstack((mat,np.zeros((num_ent+1,1))))
        print mat
        
        #get all the entries of the db
        all_DOIs = db.all()
        for line in all_DOIs:
            print vector_path
            name = line['filename']
            vector_path = vector_dir+name+'.pkl'
            print vector_path
            vec_file = open(vector_path,'rb')
            vec = pickle.load(vec_file)
            closeness = vector_mult_and_add(newVector,vec)
            newInd = index_dict[newDOI]
            oldInd = index_dict[line['ownDOI']]
            mat[newInd][oldInd] = closeness;
            mat[oldInd][newInd] = closeness;
        
        output = open(sim_matrix,'wb')
        pickle.dump(mat_list,output)   
        return None
    else:
        init_similarity_matrix(newDOI)
        return None

def distance_add_new_DOI(DOI):
    compute_vector_for_DOI(DOI)
    update_similarity_matrix(DOI)

##distance_add_new_DOI("http://dx.doi.org/10.1109/wivec.2013.6698240")
##distance_add_new_DOI("http://dx.doi.org/10.1109/icsc.2010.19")

##compute_vector_for_DOI("http://dx.doi.org/10.1109/wivec.2013.6698240")
##update_similarity_matrix("http://dx.doi.org/10.1109/wivec.2013.6698240")
##
##compute_vector_for_DOI("http://dx.doi.org/10.1109/icsc.2010.19")
##update_similarity_matrix("http://dx.doi.org/10.1109/icsc.2010.19")
##
##compute_vector_for_DOI("http://dx.doi.org/10.1109/wmute.2010.24")
##update_similarity_matrix("http://dx.doi.org/10.1109/icsc.2010.19")
