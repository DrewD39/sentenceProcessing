# written by drewdavi

import pdb
import sys
import numpy as np
import re
import math
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder

class periodFeats:
    def __init__(self):
        lWord = ""
        rWord = ""
        lenL = False
        lCap = False
        rCap = False
        dToLPeriod = 0
        dToRPeriod = 0
        lIsFloat = False


trainData = open(sys.argv[1], "r")

lines = trainData.readlines()
words = []

for l in range(len(lines)):
    words.append( lines[l].split()[1] )


classLabels = [] # EOS or NEOS for each word that contains a period
periods = []

for i in range(len(words)):
    
    # if this word contains a period
    if "." in words[i]:
        if lines[i].split()[2] == "EOS":
            classLabels.append(1)
        else:
            classLabels.append(0)
        
        p = periodFeats()

        p.lWord = re.sub(r'[^\w\s]','', words[i])
        if i < len(words)-1:
            p.rWord = re.sub(r'[^\w\s]','', words[ i+1 ])
        else:
            p.rWord = ""

        p.lenL = len( p.lWord ) < 3

        if len(p.lWord) > 0: p.lCap = p.lWord[0].isupper()
        else: p.lCap = False
        if len(p.rWord) > 0: p.rCap = p.rWord[0].isupper()
        else: p.rCap = False

        j = i-1
        dToL = 1
        while j >= 0:
            if "." in words[j]:
                break
            dToL = dToL+1
            j = j-1

        p.dToLPeriod = dToL

        j = i+1
        dToR = 0
        while j < len(words):
            dToR = dToR+1
            if "." in words[j]:
                break
            j = j+1
    
        p.dToRPeriod = dToR

        j = i+1

        try:
            float(p.lWord)
            p.lIsFloat = True
        except:
            p.lIsFloat = False

        periods.append(p)



periodNum = -1
featVect = []

for o in periods:
    periodNum += 1
    featVect.append([])
    featVect[periodNum].append( o.lWord )
    featVect[periodNum].append( o.rWord )
    featVect[periodNum].append( o.lenL )
    featVect[periodNum].append( o.lCap )
    featVect[periodNum].append( o.rCap )
    featVect[periodNum].append( o.dToLPeriod )
    featVect[periodNum].append( o.dToRPeriod )
    featVect[periodNum].append( o.lIsFloat )



#
# begin processing of test data
#

testData = open(sys.argv[2], "r")

testLines = testData.readlines()

testClassLabels = []
testWords = []

for l in range(len(testLines)):
    testWords.append(testLines[l].split()[1])

periods = []

for i in range(len(testWords)):

    # if this word contains a period
    if "." in testWords[i]:
        
        if testLines[i].split()[2] == "EOS":
            testClassLabels.append(1)
        else:
            testClassLabels.append(0)

        p = periodFeats()

        p.lWord = re.sub(r'[^\w\s]','', testWords[i])
        if i < len(testWords)-1:
            p.rWord = re.sub(r'[^\w\s]','', testWords[ i+1 ])
        else:
            p.rWord = ""

        p.lenL = len( p.lWord ) < 3

        if len(p.lWord) > 0: p.lCap = p.lWord[0].isupper()
        else: p.lCap = False
        if len(p.rWord) > 0: p.rCap = p.rWord[0].isupper()
        else: p.rCap = False

        j = i-1
        dToL = 1
        while j >= 0:
            if "." in testWords[j]:
                break
            dToL = dToL+1
            j = j-1

        p.dToLPeriod = dToL

        j = i+1
        dToR = 0
        while j < len(testWords):
            dToR = dToR+1
            if "." in testWords[j]:
                break
            j = j+1
    
        p.dToRPeriod = dToR

        j = i+1


        try:
            float(p.lWord)
            p.lIsFloat = True
        except:
            p.lIsFloat = False

        periods.append(p)


periodNum = -1
testFeatVect = []

for o in periods:
    periodNum += 1
    testFeatVect.append([])
    testFeatVect[periodNum].append( o.lWord )
    testFeatVect[periodNum].append( o.rWord )
    testFeatVect[periodNum].append( o.lenL )
    testFeatVect[periodNum].append( o.lCap )
    testFeatVect[periodNum].append( o.rCap )
    testFeatVect[periodNum].append( o.dToLPeriod )
    testFeatVect[periodNum].append( o.dToRPeriod )
    testFeatVect[periodNum].append( o.lIsFloat )


enc = OneHotEncoder()
#enc.fit( np.concatenate(np.asarray(featVect), np.asarray(testFeatVect)))
enc.fit(featVect + testFeatVect)

encodedFeatVect = enc.transform(featVect)

clf = DecisionTreeClassifier(criterion="entropy")
clf.fit(encodedFeatVect, classLabels)

encodedTestFeatVect = enc.transform(testFeatVect)
testPredictions = clf.predict(encodedTestFeatVect)

p = 0
n = 0
tp = 0
tn = 0

for i in range(len(testPredictions)):
    if testPredictions[i] == testClassLabels[i]:
        if testPredictions[i] == 1:
            p += 1
            tp += 1
        else:
            n += 1
            tn += 1
    else:
        if testClassLabels[i] == 1:
            p += 1
        else:
            n += 1

print("accuracy: " + str( round(100*(tp+tn)/(p+n),2) ) + "%")


inF = open(sys.argv[2],"r")
outF = open("SBD.test.out","w")

inLines = inF.readlines()

predNum = 0

for i in range(len(inLines)):
    cols = inLines[i].split()
    if "." in cols[1]:
        if testPredictions[predNum] == 1: temp = "EOS"
        else: temp = "NEOS"
        s = cols[0] + " " + cols[1] + " " + temp + "\n"
        predNum += 1
        outF.write(s)
