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

words_list = set() # will store all the words in our document collection, bag of words after stopword removal
for i in range(10):
    words_list = words_list.union(set(docs[i])) 

inverted_index = dict() # will store the inverted index for each word in our words_list
# each word will have a list of 3-tuples
# the 3-tuple will be (document_id, frequency of word in document_id, [index of the word in document])
for word in words_list:
    index = [] # index for 'word'
    for i in range(10):
        if (word in docs[i]):
            # the word is in the document
            # calculate frequency and indices of 'word' in docs(i)
            freq = docs[i].count(word)
            indices = [index for index in range(len(docs[i])) if docs[i][index] == word] # go throught the current document and find store the index at which word = word
            doc_id = i
            index.append((doc_id, freq, indices))
    inverted_index[word] = index

# print the inverted index now
for word in inverted_index:
    print(word, ":", inverted_index[word])
