# Hey, Look at the stuff you can edit here!             

# These are what you want the variables to be called (For the example, U and V arent used)
vars = ["X", "Y", "Z", "W", "U", "V"] 


# This is the truth table output! As an example I've loaded all 7-segments of the seven segment display into the array
# 2 Represents Dont Care condition (Program reads 2 as either a 0 or 1, whichever is more efficient with the groupings)
# You can also following Dont-Cares empty (i.e. 01001 will become 01001222)
outStr = ["1011011111101011",   # A                 A
          "1111100111100100",   # B                ---
          "1101111111110100",   # C             F |   | B
          "1011011011011110",   # D                --- <-- G
          "1010001010111111",   # E             E |   | C
          "1000111011111011",   # F                ---
          "0011111011110111"]   # G                 D







## FUNCTIONAL, BUT PAINFULLY RUSHED PSEUDO-GARBAGE ##
## (AKA: Don't look unless you're a masochist)

import math

# Define global schtuffs
outDict = dict()
outIndex = 0
groupings = dict()

# Woah, look at Mr. Big function over here
def getEquation(index):
    numBits = math.ceil(math.log2(len(outStr[index])))  # Calcs number of bits
    nearestPowOf2 = 2**numBits                          # Gets closest larger/= power of 2 (round up 1 bit)
    outLs = [int(i) for i in outStr[index]]             # Creates list of outputs from input

    for i in range(len(outStr[index]), nearestPowOf2):  # Add Dont Cares to lengthen outputs to an int pow of 2
        outLs.append(2)                 

    # Converts binary list to a dict string 
    # (stuffs gotta be a list bc/ I need to modify bits arbitrarily)
    def dictStrFromVals(vals):
        dictStr = ""
        for i in vals:
            dictStr += str(i) 
        return dictStr

    # Neat lil' recursive function to generate the Truth Table when given a set of bits
    global outDict
    global outIndex
    outDict = dict()
    outIndex = 0

    def recursiveDict(bit, bitVals):
        # Base Condition, recursion has reached past the last bit
        if bit == numBits:
            # Use varaibles as global
            global outDict
            global outIndex
            # Convert pass-in list to dict key
            outDict[dictStrFromVals(bitVals)] = outLs[outIndex]
            # Increment index (synchronizes pulling from the output list and storing with corresponding keys)
            outIndex += 1
            return

        # Recursion is actually super good at modelling arbitrary-length bit counting
        for i in range(2):
            bitVals[bit] = i
            recursiveDict(bit + 1, bitVals)

    # Call le function, print le result ( + Cool print info  ) for le debugging
    recursiveDict(0, [0]*numBits)
    print("Truth Table "+str(index)+": "+str(outDict))

    # This is where groupings will be stored (Dict is just used for holding size of grouping, useful for sorting)
    global groupings
    groupings = dict()

    # Recursively creates groupings
    # Human readability, Schumuman schmeadability!
    def recursiveGroup(varVals):
        numLoops = 0    # Count loops (Java-Brain mode)
        allTrue = True  # Whether the grouping defined by pass-in is all true
        
        # Loop through the vars
        for i in range(len(varVals)):
            newArr = varVals.copy()     # Copy the array because stuff is about to get all modify-ey
            if newArr[i] != 2: continue # If bit is already set (Not Dont-Care) dont change it
            numLoops += 1               # Increment loops (will remain 0 if all bits have been modified)
            
            for x in range(2):                  # Recurse twice, once with the DC bit set to 0, and another when its set to 1
                newArr[i] = x                   # This'll exhaust every grouping (Probably)
                if not recursiveGroup(newArr):  # What if we kissed in the 3rd recursion layer of the equation generator? :flustered:... Haha jk... Unless..?
                    allTrue = False             # If recursive result is false, this grouping does not provide an accurate result
                    
        if numLoops == 0:                               # This is what happens when a grouping consists of 1 combination
            return outDict[dictStrFromVals(newArr)] > 0 # For minterms, just check if the output is 1 (i.e. not 0, i.ee. true, i.eee. not false)

        # Calculate number of combinations covered by grouping
        numGrouped = 1
        if allTrue:
            for i in varVals:
                if i == 2:          # If a bit is DC, grouping is double the size
                    numGrouped *= 2 # Manual exponent moment
            global groupings
            groupings[dictStrFromVals(varVals)] = numGrouped # Set dict val of the succesful grouping (this will catch really shit-tier groups too)
        
        # finally return *something*
        return allTrue

    recursiveGroup([2 for i in range(numBits)])

    sortedGroups = []
    nonOverlappingGroups = []

    # SORTING PASS (Sort by Decreasing Grouped bits, i.e. Decreasing shitness of grouping)
    for i in sorted(groupings, key=groupings.get, reverse=True):
        sortedGroups.append(i)

    # Removes binary combinations which can be represented by DCs
    def aIsRepresentedInB(aSet, bSet):
        for n in range(len(aSet)-1, -1, -1):    # Loop in reverse, start at LSB and move to MSB
            if bSet[n] == "2": continue         # If bit B is a DC, then the corresponding bit A *MUST* be a subset
            if aSet[n] != bSet[n]:              # If there is a difference in the bits, then B does not fully contain A
                return False
        return True # Otherwise... Well.. Otherwise!

    # Assume every group is not fully contained until proven otherwise (you could make a legal system out of this)
    for x in sortedGroups:
        contained = False
        for y in nonOverlappingGroups:  
            if aIsRepresentedInB(x, y):  # Damn, proven contained
                contained = True
        if not contained:
            nonOverlappingGroups.append(x) # If group is not fully contained, append it to the final groups list

    # Writes an Equation now, im tired, no more comments, sorry :/
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
    return equation

# I lied lmao, print all the equations
eqs = [getEquation(i) for i in range(len(outStr))]

[print("Equation "+str(e)+": "+eqs[e]) for e in range(len(eqs))]

#      Hold it right htere bub.
#  This is a restricted access zone.
#
#               (- -)
#              -^-|-^-
#                 |
#                / \