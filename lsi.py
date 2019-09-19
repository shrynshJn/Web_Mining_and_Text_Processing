import numpy as np 
import  numpy.linalg as linAlgs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math

stop_words = set(stopwords.words('english')) # define a set of stopwords
punctuations = set([',', '.', '`', ':', '?', ';'])
stop_words = stop_words.union(punctuations) # all the words and character we want to filter out


doc_file = [] # list that will store all the documents, each item is a document
words_docs = [] # list that will convert a document in doc in doc_file to a list of words it has every item is a list of words
docs = [] # list will store the words in a document after stopword removal, each item is a list of words in doc(i) after stopword removal
for i in range(10):
    f = open("docs2/doc{}.txt".format(i), 'r')
    doc_file.append(f.read())
    words_docs.append(word_tokenize(doc_file[i]))
    docs.append([word.lower() for word in words_docs[i] if word not in stop_words])

words_list = set() # will store all the words in our document collection, bag of words after stopword removal
for i in range(10):
    words_list = words_list.union(set(docs[i])) 

query = [term.lower() for term in input("Enter query string: ").split(' ')]
words_list = words_list.union(set(query))

term_freq = []
query_freq = []
for word in words_list:
    word_freq = []
    for i in range(10):
        word_freq.append(docs[i].count(word))
    term_freq.append(word_freq)
    query_freq.append(query.count(word))

A = np.array(term_freq)
aT = A.transpose()
aTA = np.dot(aT, A)
W, V = linAlgs.eig(aTA)
print(W)
S = []
for i in range(len(W)):
    row = [0]*10
    row[i] = W[i]
    S.append(row)

S = np.array(S)
vT = V.transpose()
AV = np.dot(A, V)

sI = linAlgs.inv(S)
U = np.dot(AV, sI)

U2 = U[:, :-1]
S2 = S[:-1, :-1]

s2I = linAlgs.inv(S2)
V2 = V[:,:-1]
v2T = V2.transpose()

query_freq = np.array(query_freq)
query_freq = np.dot(query_freq.transpose(), U2)
query_freq = np.dot(query_freq, s2I)

print(query_freq)
print(v2T)

