import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from sklearn import model_selection

stop_words = set(stopwords.words('english'))
puncs = set(punctuation)

stop_words = stop_words.union(punctuation)
doc_file = [] # list that will store all the documents, each item is a document
words_docs = [] # list that will convert a document in doc in doc_file to a list of words it has every item is a list of words
docs = [] # list will store the words in a document after stopword removal, each item is a list of words in doc(i) after stopword removal
for i in range(10):
    f = open("docs/doc{}.txt".format(i), 'r')
    doc_file.append(f.read())
    words_docs.append(word_tokenize(doc_file[i]))
    docs.append([word.lower() for word in words_docs[i] if word not in stop_words])

words_list = set() # will store all the words in our document collection, bag of words after stopword removal
for i in range(10):
    words_list = words_list.union(set(docs[i])) 

data = dict()
for word in words_list:
    data[word] = []
    for doc in docs:
        if word in doc:
            data[word].append(doc.count(word))
        else:
            data[word].append(0)
dFrame = pd.DataFrame(data)

labels = [1, 0, 1, 1, 1, 0, 0, 1, 1, 0]

dFrame.insert(284, "Class", labels, True)

X = dFrame.iloc[:, 1:284]
Y = dFrame.iloc[:, 284]


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=90)

#applying decision tree

clf = DecisionTreeClassifier()
clf = clf.fit(X_train, Y_train)
Y_pred = clf.predict(X_test)
print("Decision Tree", "Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))

# applying naive bayes

gnb = GaussianNB()
gnb.fit(X_train, Y_train)
Y_pred = gnb.predict(X_test)
print("Naive Bayes", "Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))


clf = SVC(kernel='linear')
clf.fit(X_train, Y_train)
Y_pred = clf.predict(X_test)
print("Support Vector Machine", "Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))


array = dFrame.values
seed = 7
kFold = model_selection.KFold(random_state=seed)
estimators = []
estimators.append(('decisiontree', DecisionTreeClassifier()))
estimators.append(('svc', SVC()))
estimators.append(('naivebayes', GaussianNB()))

ensemble = VotingClassifier(estimators)
results = model_selection.cross_val_score(ensemble, X_train, Y_train, cv = kFold)
print(results.mean())
clf1 = DecisionTreeClassifier(random_state=1)
clf2 = SVC()
clf3 = GaussianNB()
labels = ['Decision Tree', 'SVM', 'Naive Bayes']
for clf, label in zip([clf1, clf2, clf3], labels):
    scores = model_selection.cross_val_score(clf, X_train, Y_train, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]"%(scores.mean(), scores.std(), label))

