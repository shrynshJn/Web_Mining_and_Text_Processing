from random import seed
from random import randrange
from csv import reader
from math import sqrt

def loadCSV(fn):
	dataset = []
	f = open(fn, "r")
	csvReader = reader(f)
	for row in csvReader:
		if not row:
			continue
		dataset.append(row)
	return dataset

def str2float(dataset, col):
	for row in dataset:
		row[col] = float(row[col].strip())

def str2index(dataset, col):
	classValues = [row[col] for row in dataset]
	unique = set(classValues)
	lookup = dict()
	for i, val in enumerate(unique):
		lookup[val] = i
	for row in dataset:
		row[col] = lookup[row[col]]
	return lookup

def crossValidation(dataset, n_folds):
	datasetSplit = []
	datasetCopy = list(dataset)
	foldSize = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = []
		while (len(fold) < foldSize):
			index = randrange(len(datasetCopy))
			fold.append(datasetCopy.pop(index))
		datasetSplit.append(fold)
	return datasetSplit

def accuracyMetric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		correct += 1 if actual[i] == predicted[i] else 0
	return (correct / len(actual) ) * 100.0

def evaluateAlgorithm(dataset, alg, n_folds, *args):
	folds = crossValidation(dataset, n_folds)
	scores = []
	for fold in folds:
		trainSet = list(folds)
		trainSet.remove(fold)
		trainSet = sum(trainSet, [])
		testSet = []
		for row in fold:
			rowCopy = list(row)
			testSet.append(rowCopy)
			rowCopy[-1] = None
		predicted = alg(trainSet, testSet, *args)
		actual = [row[-1] for row in fold]
		accuracy = accuracyMetric(actual, predicted)
		scores.append(accuracy)
	return scores

def testSplit(index, value, dataset):
	left, right = [], []
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right

def giniIndex(groups, classes):
	nInstances = float(sum([len(group) for group in groups]))
	gini = 0.0
	for group in groups:
		size = float(len(group))
		if size == 0:
			continue
		score = 0.0
		for classVal in classes:
			p = [row[-1] for row in group].count(classVal) / size
			score += p*p
		gini += (1.0 - score) * (size / nInstances)
	return gini

def getSplit(dataset, nFeatures):
	classVal = list(set(row[-1] for row in dataset))
	bIndex, bVal, bScore, bGroups = 999, 999, 999, None
	features = []
	while len(features) < nFeatures:
		index = randrange(len(dataset[0]) - 1)
		if index not in features:
			features.append(index)
	for index in features:
		for row in dataset:
			groups = testSplit(index, row[index], dataset)
			gini = giniIndex(groups, classVal)
			if (gini < bScore):
				bIndex, bValue, bScore, bGroups = index, row[index], gini, groups
	return {'index': bIndex, 'value':bValue, 'groups':bGroups}

def toTerminal(group):
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)

def split(node, maxDepth, minSize, nFeatures, depth):
	left, right = node['groups']
	del(node['groups'])
	if not left or not right:
		node['left'] = node['right'] = toTerminal(left + right)
		return
	if depth >= maxDepth:
		node['left'], node['right'] = toTerminal(left), toTerminal(right)
		return
	if (len(left) <= minSize):
		node['left'] = toTerminal(left)
	else:
		node['left'] = getSplit(left, nFeatures)
		split(node['left'], maxDepth, minSize, nFeatures, depth+1)
	
	if (len(right) <= minSize):
		node['right'] = toTerminal(right)
	else:
		node['right'] = getSplit(right, nFeatures)
		split(node['right'], maxDepth, minSize, nFeatures, depth+1)

def buildTrees(train, maxDepth, minSize, nFeatures):
	root = getSplit(train, nFeatures)
	split(root, maxDepth, minSize, nFeatures, 1)
	return root

def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']

def subSample(dataset, ratio):
	sample = []
	nSample = round(len(dataset)*ratio)
	while (len(sample) < nSample):
		index = randrange(len(dataset))
		sample.append(dataset[index])
	return sample

def baggingPredict(trees, row):
	predictions = [predict(tree, row) for tree in trees]
	return max(set(predictions), key = predictions.count)

def random_forest(train, test, maxDepth, minSize, sampleSize, nTrees, nFeatures):
	trees = []
	for i in range(nTrees):
		sample = subSample(train, sampleSize)
		tree = buildTrees(sample, maxDepth, minSize, nFeatures)
		trees.append(tree)
	predictions = [baggingPredict(trees, row) for row in test]
	return (predictions)

seed(2)
filename = 'sonar.all-data.csv'
dataset = loadCSV(filename)
for i in range(0, len(dataset[0]) - 1):
	str2float(dataset, i)
str2index(dataset, len(dataset[0]) - 1)
nFolds = 5
maxDepth = 10
minSize = 1
sampleSize = 1.0
nFeatures = int(sqrt(len(dataset[0]) - 1))
for nTrees in [1, 5, 10]:
	scores = evaluateAlgorithm(dataset, random_forest, nFolds, maxDepth, minSize, sampleSize, nTrees, nFeatures)
	print("Trees: ", nTrees)
	print("Scores: ", scores)
	print("Mean Accuracy: %.3f%%" % (sum(scores)/float(len(scores))))

