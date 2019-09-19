# objective: find matrix U, S, V for given A such that A = U*S*trans(V)
import numpy as np 
import numpy.linalg as lingAlgs
from math import sqrt

def SVD(A):
    A = np.array(A)
    transA = A.transpose()
    transAA = np.dot(transA, A) # transA * A
    eig, V = lingAlgs.eig(transAA)
    S = []
    for i in range(len(eig)):
        s_row = [0]*len(A[0])
        s_row[i] = sqrt(eig[i])
        S.append(s_row)
    
    S = np.array(S)
    SI = lingAlgs.inv(S)
    AV = np.dot(A, V)
    U = np.dot(AV, SI)
    return U,S,V
