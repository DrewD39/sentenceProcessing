# writte by drewdavi

from __future__ import division
import sys
import string
import math
import pdb


# returns true if all characters are punctuation
def onlyPuncChars(s):
    return all(i in string.punctuation for i in s)


# out of all bigrams, how often do the words appear in their respective places
# reference the 2x2 grid in the slides
def X2(bigrams, biCount, unigrams, uniCount):

    firstWords = {}
    secWords = {}

    chiSquareVals = []


    # get the X2 val for each bigram
    for B in bigrams.keys():

        X2Sum = 0

        B0, B1 = B.split()

        #count0 = unigrams[B0]
        #count1 = unigrams[B1]
        #countNOT0 = biCount - unigrams[B0]
        #countNOT1 = biCount - unigrams[B1]

        if B0 in firstWords and B1 in secWords:
            count0 = firstWords[B0]
            count1 = secWords[B1]
            countNOT0 = biCount - count0
            countNOT1 = biCount - count1
        else:
            count0 = 0
            count1 = 0
            countNOT0 = 0
            countNOT1 = 0

            for b in bigrams.keys():
                b0, b1 = b.split()

                if b0 == B0:
                    count0 += bigrams[b]
                if b1 == B1:
                    count1 += bigrams[b]
                if b0 != B0:
                    countNOT0 += bigrams[b]
                if b1 != B1:
                    countNOT1 += bigrams[b]

            firstWords[B0] = count0
            secWords[B1] = count1

        s = B0 + " " + B1

        # 0, 0 - b0 = s0, b1 = s1
        E = count0 / biCount * count1 / biCount * biCount
        O = bigrams[ s ]

        num = math.pow( O - E, 2 )
        den = E
        res = num / den
        X2Sum += res

#        print(X2Sum)

        #chiSquareVals.append( (sum_ij,b) )

        # 0, 1 - b0 = s0, b1 != s1    
        E = count0 / biCount * countNOT1 / biCount * biCount

        O = count0 - bigrams[s] # number of bigrams where b0 = s0 and b1 != s

        num = math.pow( O - E, 2 )
        den = E
        res = num / den
        X2Sum += res

#        print(X2Sum)
        #     1, 0 - b0 != s0, b1 = s1
        E = countNOT0 / biCount * count1 / biCount * biCount

        O = count1 - bigrams[s] # number of bigrams where b0 = s0 and b1 != s

        num = math.pow( O - E, 2 )
        den = E
        res = num / den
        X2Sum += res

#        print(X2Sum)
        # 1, 1 - b0 != s0, b1 != s1
        E = countNOT0 / biCount * countNOT1 / biCount * biCount

        O = biCount - count0 - count1 + bigrams[s] # number of bigrams where b0 != s0 and b1 != s1

        num = math.pow( O - E, 2 )
        den = E
        res = num / den
        X2Sum += res

#        print(X2Sum)

        chisquared = X2Sum

        chiSquareVals.append( (chisquared,B) )


    # sort with largest chi-squared vals first
    chiSquareVals.sort(reverse=True)

    for k in range(20):
        print( str(chiSquareVals[k][1]) + " " + str(chiSquareVals[k][0]) )




def PMI(bigraphs, biCount, unigrams, uniCount):

    PMIVals = []

    for B in bigraphs.keys():
        B0, B1 = B.split()
        P_12 = bigrams[B] / biCount
        P_1 = unigrams[B0] / uniCount
        P_2 = unigrams[B1] / uniCount

        PMI = math.log(P_12 / (P_1*P_2))
        PMIVals.append( (PMI,B) )

    PMIVals.sort(reverse=True)

    for k in range(20):
        print( str(PMIVals[k][1]) + " " + str(PMIVals[k][0]) )


#    firstWords = {}
#    secWords = {}
#
#    for B in bigraphs.keys():
#
#        P_12 = bigraphs(B)
#
#        B0, B1 = B.split()
#        if B0 in firstWords and B1 in secWords:
#
#            P_1 = firstWords[B0]/biCount
#            P_2 = secWords[B1]/biCount
#
#        else:
#            count0 = 0
#            count1 = 0
#            for b in bigrams.keys():
#                b0, b1 = b.split()
#                if b0 == B0:
#                    count0 += bigrams[b]
#                if b1 == B1:
#                    count1 += bigrams[b]
#            firstWords[B0] = count0
#            secWords[B1] = count1



inFile = open(sys.argv[1], "r")
lines = inFile.readlines()

unigrams = {}
bigrams = {}

for l in lines:
    words = l.split() # split on whiotespace
    q = -1
    while q < len(words)-1:
        q += 1

        # if this word is only punctuation, get rid of it
        # then move on to next letter, which will now be at pos i
        if onlyPuncChars(words[q]):
            del words[q]
            q -= 1
            continue

        # if this word not already in unigram set, add it
        if words[q] not in unigrams:
            unigrams[words[q]] = 1
        # else increment it
        else:
            unigrams[words[q]] = unigrams[words[q]]+1

        # if a bigram can be made
        if q > 0:
            bi = words[q-1] + " " + words[q]
            if bi not in bigrams:
                bigrams[bi] = 1
            else:
                bigrams[bi] = bigrams[bi]+1

uniCount = 0
for u in unigrams.keys():
    uniCount += unigrams[u]


biCount = 0 # total number of (non-unique) bigrams
for b in bigrams.keys():
    if bigrams[b] < 5:
        del bigrams[b]
    else:
        biCount += bigrams[b]


# at this point you have a map that shows all unigrams and bigrams with
# values that correspond to their counts
# (bigrams that occour less than 5 times are ignored)


if sys.argv[2] == "chi-square":
    X2(bigrams, biCount, unigrams, uniCount)
elif sys.argv[2] == "PMI":
    PMI(bigrams, biCount, unigrams, uniCount)
else:
    print("INVALID INPUT ARGS")


