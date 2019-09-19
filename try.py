import numpy as np
import numpy.linalg as LA
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity as CoSim

stop_words = set(stopwords.words('english'))
import math
d1 = "Shipment of gold damaged in a fire"
d2 = "Delivery of silver arrived in a silver truck"
d3 = "Shipment of gold arrived in a truck"
q = "gold silver truck"

Q = q.split()
q = []
for t in Q:
    t = t.lower()
    q.append(t)
    
D1 = d1.split()
D2 = d2.split()
D3 = d3.split()
d1 = []
d2 = []
d3 = []
vocab = []
for t in D1:
    t = t.lower()
    d1.append(t)
    if(t not in vocab): #and t not in stop_words):
        vocab.append(t)
for t in D2:
    t = t.lower()
    d2.append(t)
    if(t not in vocab): # and t not in stop_words):
        vocab.append(t)
for t in D3:
    t = t.lower()
    d3.append(t)
    if(t not in vocab): # and t not in stop_words):
        vocab.append(t)
vocab.sort()
#print(vocab)
A = []
Q = []
for i in vocab:
    temp = []
    temp.append(d1.count(i))
    temp.append(d2.count(i))
    temp.append(d3.count(i))
    A.append(temp)
    Q.append(q.count(i))

A = np.array(A)
#print(A)
AT = A.transpose()
#print(AT)
ATA = np.dot(AT,A)
#print(ATA)
W,V = LA.eig(ATA)
#print(W)
#print(V)

S= []
for i in range(0,len(W)):
    temp = [0, 0, 0]
    temp[i] = math.sqrt(W[i])
    S.append(temp)
S = np.array(S)

VT = V.transpose()
AV = np.dot(A,V)

Si = LA.inv(S)
U = np.dot(AV,Si)

U2 = U[:,:-1]

S2 = S[:-1,:-1]

S2i = LA.inv(S2)
V2 = V[:,:-1]
V2T = V2.transpose()

Q = np.array(Q)
Q = np.dot(Q.transpose(),U2)
Q = np.dot(Q,S2i)
print(Q)
print(V2T)
print(CoSim([Q,V2T[:,0]]))
print(CoSim([Q,V2T[:,1]]))
print(CoSim([Q,V2T[:,2]]))