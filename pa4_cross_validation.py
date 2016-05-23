__author__ = 'Holliday'

import bayesBest, random, os
import numpy as np


execfile("bayesBest.py")
bc = bayesBest.Bayes_Classifier()

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


## AVERAGE TOGETHER 10 10-FOLD CROSS VALIDATIONS

# Bayes
rp = np.mean(np.array([.97727, .97206, .97978, .97996, .97718, .97044, .97817, .97996, .97790, .97385]))
rn = np.mean(np.array([.73931, .77367, .72687, .73784, .73894, .75832, .74296, .72066, .73163, .76271]))
pp = np.mean(np.array([.93888, .94629, .93629, .93871, .93879, .94274, .93974, .93493, .93722, .94391]))
pn = np.mean(np.array([.89232, .87510, .90199, .90412, .89188, .86633, .89673, .90206, .89410, .88091]))
fp = np.mean(np.array([.95769, .95900, .95854, .95889, .95760, .95639, .95857, .95692, .95713, .95865]))
fn = np.mean(np.array([.80864, .82127, .80502, .81256, .80824, .80873, .81264, .80122, .80475, .81756]))

# Bayes Best
RP = np.mean(np.array([.97441, .972943327239, .969652650823, .974040219378, 0.974040219378, 0.974405850091, 0.972943327239, .975868372943, 0.972212065814, .975868372943]))
RN = np.mean(np.array([.92505, .92029250457, .929067641682, 0.921389396709, 0.928336380256, 0.921389396709, 0.920658135283, 0.924314442413, 0.926142595978, 0.915539305302]))
PP = np.mean(np.array([.93019, .925887265136, .933474128828, 0.926931106472, 0.933099824869, 0.926956521739, 0.926209537069, 0.929641239986, 0.931022408964, 0.921934369603]))
PN = np.mean(np.array([.97495, .973317865429, .970217640321, 0.974477958237, 0.974664107486, 0.974854932302, 0.973328179358, 0.976438779452, 0.972734254992, 0.976218323587]))
FP = np.mean(np.array([.95178, .94883223391, .951219512195, 0.949901943305, 0.95313059034, 0.95008912656, 0.949001426534, 0.952194077774, 0.951171525666, 0.948134991119]))
FN = np.mean(np.array([.94934, .946062770156, .949196862159, 0.947190377749, 0.950936329588, 0.947368421053, 0.946260804209, 0.94966190834, 0.948866828994, 0.944905660377]))

print "BAYES", pp, rp, fp, pn, rn, fn
print "BAYES BEST", PP, RP, FP, PN, RN, FN



