
import numpy as np
def importDataset(fileName : "string") -> "list(string)" :

    # read the file and get it's content
    file = open(fileName, 'r')
    content = file.read()
    file.close()

    # return a list of the relevant strings, by splitting at the newline
    return content.split("\n")

def transformStringBase( stringList :"list(string)", mappingDict :"dict" = None) -> "list":
    
    # my default mapping maps a,b,c on the complect plane 120° apart
    # this way the (absolute) distance between any two different charactors is 
    # indepdent of the involved charcters
    # unlike in a mappting like  mappingDict ={"a": 1, "b": 2, "c": 3}
    if mappingDict is None: 

        mappingDict ={"a":np.exp( 0/3 * 1j* 2*np.pi ), 
                      "b":np.exp( 1/3 * 1j* 2*np.pi ), 
                      "c":np.exp( 2/3 * 1j* 2*np.pi )}

    outputList = []

    for aString in stringList:
        # do 'get(character,character)' to be robust against dicts with missind characters
        transformedString = [ mappingDict.get(character,character) for character in aString]
        outputList.append(transformedString)    

    return outputList


if __name__ == '__main__':
    # tests of methods go here

    stringList = importDataset("../sequences.txt")

    assert len(stringList) == 5000
    assert len(stringList[0]) == 240

    A = np.exp( 0/3 * 1j* 2*np.pi )
    B = np.exp( 1/3 * 1j* 2*np.pi )
    C = np.exp( 2/3 * 1j* 2*np.pi )

    testString = transformStringBase(["abc"])[0]
    assert  np.sum(testString - np.array([A,B,C]) ) ==0

    assert abs(testString[0] - testString[1]) - abs(testString[0] - testString[2]) < 1E-15
    assert abs(testString[0] - testString[1]) - abs(testString[1] - testString[2]) < 1E-15
    assert abs(testString[0] - testString[2]) - abs(testString[1] - testString[2]) < 1E-15
    
    print("All good!")


    #import pdb; pdb.set_trace() # import the debugger and instruct it to stop here

