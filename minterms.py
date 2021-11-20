import math

vars = ["X", "Y", "Z", "W", "V", "U"]
outStr = "1011011111101011"

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

groupings = dict()

# Recursively creates groupings
def recursiveGroup(varVals):
    numLoops = 0
    allTrue = True
    for i in range(len(varVals)):
        newArr = varVals.copy()
        if newArr[i] != 2:
            continue
        numLoops += 1
        for x in range(2):
            newArr[i] = x
            if not recursiveGroup(newArr):
                allTrue = False
    if numLoops == 0:
        dictStr = ""
        for i in newArr:
            dictStr += str(i) 
        return outDict[dictStr] > 0

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

recursiveGroup([2 for i in range(numBits)])

sortedGroups = []
nonOverlappingGroups = []
# SORTING PASS (Sort by Decreasing Grouped bits)
for i in sorted(groupings, key=groupings.get, reverse=True):
    sortedGroups.append(i)
    
print("ALL GROUPINGS: " + str(sortedGroups))

def aIsRepresentedInB(aSet, bSet):
    
    bSubset = True
    for n in range(len(aSet)-1, -1, -1):
        if bSet[n] == "2":
            continue
        if aSet[n] != bSet[n]:
            bSubset = False
    return bSubset

for x in sortedGroups:
    contained = False
    for y in nonOverlappingGroups:
        if aIsRepresentedInB(x, y):
            contained = True
    if not contained:
        nonOverlappingGroups.append(x)
        
print("SUPERSET-ONLY GROUPINGS: " + str(nonOverlappingGroups))

equation = ""
for i in range(len(nonOverlappingGroups)):
    for n in range(len(nonOverlappingGroups[i])):
        if nonOverlappingGroups[i][n] == "2":
            continue
        if nonOverlappingGroups[i][n] == "1":
            equation += str(vars[n]) 
        else:
            equation += str(vars[n])+"'"
    if i < len(nonOverlappingGroups)-1:
        equation += " + "
print("EQUATION: " + equation)
