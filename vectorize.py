import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english')) # define a set of stopwords
punctuations = set([',', '.', '`', ':', '?', ';'])
stop_words = stop_words.union(punctuations) # all the words and character we want to filter out

doc_file = [] # list that will store all the documents, each item is a document
words_docs = [] # list that will convert a document in doc in doc_file to a list of words it has every item is a list of words
docs = [] # list will store the words in a document after stopword removal, each item is a list of words in doc(i) after stopword removal
for i in range(10):
    f = open("docs/doc{}.txt".format(i), 'r')
    doc_file.append(f.read())
    words_docs.append(word_tokenize(doc_file[i]))
    docs.append([word for word in words_docs[i] if word not in stop_words])

# docs(i) is the document with stopword removed and each word at it's index

words_list = set() # a set of all words in all our documents, bag of words
for i in range(10):
    words_list = words_list.union(set(docs[i])) 

# now words_list has the bag of words for our current documents

term_vector = dict() # this will store the vector for each word in words_list
for word in words_list:
    term_vector[word] = [int(word in docs[i]) for i in range(10)] 
# term_vector has a vector for each word, with 10 values (0,1,1,0,1,1,1,0,0,0)
# meaning the word is in docs at index 1,2,4,5,6

for k in term_vector:
    print(k,":", term_vector[k])