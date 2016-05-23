__author__ = 'Holliday'

import bayes, random, os

execfile("bayes.py")
bc = bayes.Bayes_Classifier()

random.shuffle(bc.positiveFiles)
random.shuffle(bc.negativeFiles)

size1 = bc.positiveCount / 10
size2 = bc.negativeCount / 10
groups = []
group1 = bc.positiveFiles[:size1] + bc.negativeFiles[:size2]
groups.append(group1)
group2 = bc.positiveFiles[size1:2*size1] + bc.negativeFiles[size2:2*size2]
groups.append(group2)
group3 = bc.positiveFiles[2*size1:3*size1] + bc.negativeFiles[2*size2:3*size2]
groups.append(group3)
group4 = bc.positiveFiles[3*size1:4*size1] + bc.negativeFiles[3*size2:4*size2]
groups.append(group4)
group5 = bc.positiveFiles[4*size1:5*size1] + bc.negativeFiles[4*size2:5*size2]
groups.append(group5)
group6 = bc.positiveFiles[5*size1:6*size1] + bc.negativeFiles[5*size2:6*size2]
groups.append(group6)
group7 = bc.positiveFiles[6*size1:7*size1] + bc.negativeFiles[6*size2:7*size2]
groups.append(group7)
group8 = bc.positiveFiles[7*size1:8*size1] + bc.negativeFiles[7*size2:8*size2]
groups.append(group8)
group9 = bc.positiveFiles[8*size1:9*size1] + bc.negativeFiles[8*size2:9*size2]
groups.append(group9)
group10 = bc.positiveFiles[9*size1:10*size1] + bc.negativeFiles[9*size2:10*size2]
groups.append(group10)

# classified as positive and was positive
classPosT = 0
# classified as positive but was negative
classPosF = 0
# classified as negative and was negative
classNegT = 0
# classified as negative but was positive
classNegF = 0

for i in range(0, 10):
	print i
	bc.positiveDict = {}
	bc.negativeDict = {}
	bc.positiveFiles = bc.positiveFiles[:i*size1] + bc.positiveFiles[(i+1)*size1:]
	bc.negativeFiles = bc.negativeFiles[:i*size2] + bc.negativeFiles[(i+1)*size2:]
	bc.train(True)
	for f in groups[i]:
	    text = bc.loadFile("movies_reviews/" + f)
	    classified = bc.classify(text, False)
	    if f[7] == '1' and classified == "negative":
	    	classNegT += 1
	    if f[7] == '1' and classified == "positive":
	    	classPosF += 1
	    if f[7] == '5' and classified == "negative":
	    	classNegF += 1
	    if f[7] == '5' and classified == "positive":
	    	classPosT += 1
recallP = classPosT / float(bc.positiveCount)
recallN = classNegT / float(bc.negativeCount)
precisionP = classPosT / float(classPosT + classPosF)
precisionN = classNegT / float(classNegT + classNegF)
fMeasureP = 2 * recallP * precisionP / float(precisionP + recallP)
fMeasureN = 2 * recallN * precisionN / float(precisionN + recallN)

print "RecallP: ", recallP
print "RecallN: ", recallN
print "PrecisionP: ", precisionP
print "PrecisionN: ", precisionN
print "FmeasureP: ", fMeasureP
print "FmeasureN: ", fMeasureN







