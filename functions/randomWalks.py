from os import path
import sys
# need to append the current directory here explicitly, 
# so that we can include this script in our notebook, but also include the importDataset here
sys.path.append( path.dirname( path.abspath(__file__) )  ) 


from  importData import importDataset

import numpy as np

import collections

import random


def getBasis( myString : "iterable") -> "list":

    basisElements = set()
    for val in myString: basisElements.add(val)

    basis = sorted(list(basisElements))

    return basis


def dummyIterator( myIterable ):
    for x in myIterable: yield x

def getCharacterFrequency( stringList :"list(string)",
    flexIterator : "a function mapping iterable on iterable" = dummyIterator ) -> "list(np.array)":

    # we presume all character show up in the first string

    autoBasis = set()

    counterList = []

    for seqString in stringList:
        counter = collections.Counter(  flexIterator(seqString))

        totanNumberOfCharacters = np.sum(np.array(list(counter.values())))

        for key in counter.keys():
            counter[key] = float(counter[key])/totanNumberOfCharacters
            autoBasis.add(key)

        counterList.append(counter)

    for counter in counterList:
        for basisElement in autoBasis:
            if basisElement not in counter: 
                #print("missing basis")
                counter[basisElement] = 0

    sortedBasis = sorted(list(autoBasis))

    outputList = []
    for counter in counterList:
        outputList.append( [counter[base] for base in sortedBasis]  )


    return np.asarray(outputList), sortedBasis

def calculateTransitionFrequencies( stringList :"list(string)", tupleLength = 2) -> "list(np.array)":
    
    def yieldNeighbors( aString ):
        for index in range(0, len(aString) - (tupleLength-1)):
            yield aString[index : index+tupleLength]

    transitionProbabilityList, basis = getCharacterFrequency( stringList , flexIterator = yieldNeighbors ) 

    return transitionProbabilityList, basis


def getTransitionProbabilities(transFreq : "np.array", transBase :  "list", 
                              letterFreq : "np.array", letterBase : "list" ):


    
    letter_index_mapting = { letter:index for index, letter in enumerate(letterBase) }


    startingLetterProbabilities = np.zeros(np.shape(transFreq))

    for index, transition in enumerate(transBase): 

        startingLetterProbabilities[:,index] = letterFreq[:,letter_index_mapting[transition[0]]]



    transitionProbabilities = transFreq/startingLetterProbabilities


    return transitionProbabilities




def calculateAverageTransitionProbabilitiesBasedOnClusterLabel(clusterLabel, transtionProbability):

    if isinstance(clusterLabel,list):         clusterLabel         = np.asarray(clusterLabel)
    if isinstance(transtionProbability,list): transtionProbability = np.asarray(transtionProbability)

    clusterLabel = clusterLabel[0:10]
    transtionProbability = transtionProbability[0:10]

    clusterLabelUnique = sorted( list( set(clusterLabel) ))


    meanList = []
    stdList = []


    for label in clusterLabelUnique:

        # select rows in our transtionProbability that match with the given label
        selector = clusterLabel == label 

        meanList.append( np.mean(transtionProbability[selector], axis=0 ) )
        stdList.append(  np.std( transtionProbability[selector], axis=0 ) )


    return clusterLabelUnique, meanList, stdList


if __name__ == '__main__':
    # tests of methods go here

    stringList = importDataset("../sequences.txt")

    basis = getBasis( stringList[0] )

    letterFrequencies, sortedBasis =  getCharacterFrequency( stringList )


    transitionProbs, base = calculateTransitionFrequencies( stringList )

    getTransitionProbabilities(transitionProbs, base, letterFrequencies, sortedBasis)


    transitionProbsTest, baseTest = calculateTransitionFrequencies( ["abc"] )


    assert (transitionProbsTest == np.asarray( [[0.5,0.5]])).all()
    assert baseTest == ["ab", "bc"]


    fakeLabels = [random.randint(0,2) for counter in range(0,len(transitionProbs)) ]

    clusterLabelUnique, meanList, stdList = calculateAverageTransitionProbabilitiesBasedOnClusterLabel(fakeLabels, transitionProbs)
    

    print("All good!")


    #import pdb; pdb.set_trace() # import the debugger and instruct it to stop here

