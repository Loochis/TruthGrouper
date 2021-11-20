import math

vars = ["X", "Y", "Z", "W", "V", "U"]
outStr = "0000000011111111"

numBits = math.ceil(math.log2(len(outStr)))
nearestPowOf2 = 2**numBits
outLs = [int(i) for i in outStr]
# Add Dont Cares to lengthen outputs to an int pow of 2
for i in range(len(outStr), nearestPowOf2):
    outLs.append(2)

outDict = dict()
outIndex = 0

def recursiveDict(bit, bitVals):
    if bit == numBits:
        dictStr = ""
        for i in bitVals:
            dictStr += str(i) 
        global outDict
        global outIndex
        outDict[dictStr] = outLs[outIndex]
        outIndex += 1
        return

    for i in range(2):
        bitVals[bit] = i
        recursiveDict(bit + 1, bitVals)

recursiveDict(0, [0]*numBits)
print(outDict)

groupings = dict()

def recursiveGroup(varVals):
    numLoops = 0
    newArr = varVals.copy()
    allTrue = True
    print(newArr)
    for i in range(len(varVals)):
        if varVals[i] != 2:
            continue
        numLoops += 1
        for x in range(2):
            newArr[i] = x
            if not recursiveGroup(newArr):
                allTrue = False

    numGrouped = 1
    if allTrue:
        for i in varVals:
            if i == 2:
                numGrouped *= 2
        global groupings
        dictStr = ""
        for i in varVals:
            dictStr += str(i) 
        groupings[dictStr] = numGrouped
    return allTrue

print(recursiveGroup([2 for i in range(numBits)]))
print(groupings)
