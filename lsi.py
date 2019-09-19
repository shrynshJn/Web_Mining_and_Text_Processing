import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import  numpy.linalg as linAlgs
import numpy as np 
import math 
from svd import SVD

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

query = [word.lower() for word in input("Enter query string: ").split(' ') if word not in stop_words]
words_list.union(set(query))

words_list = list(words_list)
words_list.sort()
term_freq = []
query_freq = []

for word in words_list:
    doc_freq = []
    for i in range(len(docs)):
        doc_freq.append(docs[i].count(word))
    term_freq.append(doc_freq)
    query_freq.append(query.count(word))

U, S, V = SVD(term_freq) # use the SVD function created in svd.py
# dimension approximation
# for k - dimension approximation change 2 to k
# for 2 - dimension approximation
k = 2
Uk = U[:, 0:k] # first two coloumns of U and all rows
Sk = S[0:k, 0:k] # sub matrix with first two columns and rows
Vk = V[:, 0:k] # first two columns of V and all rows each row is the vector of doc(i)
SkI = linAlgs.inv(Sk)
Q = np.array(query_freq)
Q = np.dot(Q.transpose(), Uk)
Q = np.dot(Q, SkI)
print(Q)
print(Vk)