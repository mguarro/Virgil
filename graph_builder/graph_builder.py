import numpy as np
from scipy.optimize import minimize
import pickle
import os
from tinydb import TinyDB, Query
import matplotlib.pyplot as plt
import json

cur_dir = os.path.dirname(__file__)
db_loc = cur_dir+"/../database_builder/master-db.json"
sim_mat_loc = cur_dir+"/../database_builder/similarity_matrix.pkl"
graph_loc = cur_dir+"/graph.json"

#global variables
kr = 1
kac = 1
sim_mat = 1
index_dict = 1
xyd_p = 1
N = 1

#compute gradient of cost
def gradCost(vec):
    x = vec[:N]
    y = vec[N:]

    d2m2 = np.zeros((N,N)) #1 over distance squared squared
    for i in range(N):
        for j in range(i):
            t1 = x[i] - x[j]
            t2 = y[i] - y[j]
            t3 = t1**2 + t2**2
            t4 = 1/(t3**2)
            d2m2[i,j] = t4
            d2m2[j,i] = t4

            
    dx = np.zeros(N)
    dy = np.zeros(N)

    for a in range(N):
        dx[a] = 2*kac*x[a]+2*xyd_p*(x[a]-y[a])
        dy[a] = 2*kac*y[a]-2*xyd_p*(x[a]-y[a])
        for i in range(N):
            if a!=i:
                dx[a] = dx[a]+sim_mat[a,i]*2*(x[a]-x[i])-2*kr*(x[a]-x[i])*d2m2[a,i]
                dy[a] = dy[a]+sim_mat[a,i]*2*(y[a]-y[i])-2*kr*(y[a]-y[i])*d2m2[a,i]

    grad = np.append(dx,dy)
    return grad
            
            
    

#cost of current arrangement on nodes
def arrCost(vec):
    #vec arranged as [x1:xn y1:yn]
    x = vec[:N]
    y = vec[N:]

    cost = 0;
    for i in range(N):
        a = x[i]**2 + y[i]**2
        cost = cost+kac*a
        cost = cost + xyd_p*((x[i]-y[i])**2)
        for j in range(i):
            t1 = x[i] - x[j]
            t2 = y[i] - y[j]
            t3 = t1**2 + t2**2
            t4 = 1/t3
            cost = cost + kr*t4 + sim_mat[i,j]*t3
            
    return cost

def scaleSimMat(sim_mat_set,mat_scale):
    global sim_mat
    sim_mat = sim_mat_set*mat_scale
    return None
 

def computeNodeLocations(kr_set,kac_set,mat_scale,xyd_p_set):
    #set global variables
    global kr
    global kac
    global N
    global index_dict
    global xyd_p
    xyd_p = xyd_p_set
    kr = kr_set
    kac = kac_set

    #load similarity matrix and index, set globals
    mat_file = open(sim_mat_loc,'rb')
    mat_list = pickle.load(mat_file)
    index_dict = mat_list[0]
##    print mat_list[1]
    scaleSimMat(mat_list[1],mat_scale)
    N = np.size(sim_mat,axis = 0)

    #do minimization
##    res = minimize(rosen, x0, method='BFGS', jac=rosen_der,
##...                options={'disp': True})
   # np.random.seed(seed=0)
    x0 = np.random.rand(2*N)
##    res = minimize(arrCost,x0,method = 'Nelder-Mead', options={'disp':True,'maxfev':100000,'maxiter':100000})

    res = minimize(arrCost, x0, method= 'BFGS',jac = gradCost, options={'disp': True})
    return res

#some test code
##r = computeNodeLocations(1,1,100,10)
##print N
##vec = r.x
##x = vec[:N]
##y = vec[N:]
##print x
##print y
##plt.plot(x,y,'o')
##plt.show()

def nodeLocationsJSON(kr_set,kac_set,mat_scale,xyd_p_set):
    res = computeNodeLocations(kr_set,kac_set,mat_scale,xyd_p_set)
    vec = res.x
    x = vec[:N]
    y = vec[N:]
    toJSON=[]
    for index,line in enumerate(index_dict):
        toJSON.append({"doi": line,
                  "x_axis": x[index],
                  "y_axis": y[index]})
    with open(graph_loc, 'w+') as fp:
        json.dump(toJSON, fp, skipkeys=True)

        
        
        

nodeLocationsJSON(1,1,1,1)





    
