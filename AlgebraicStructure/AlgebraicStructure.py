def main(args):
    if len(args) == 0:
        print("Not enough arguments")
        return
    try:
        identifyAlgebraicStructure(args[0])
    except ValueError as err:
        print(err.args)
    except IOError as err:
        print(err.args)

# note: elements' indexing starts from 0
def identifyAlgebraicStructure(path):
    table = parseToCayleyTable(path)
    
    if not checkClosure(table):
        print("Nothing")
        return
    
    if not checkAssociativity(table):
        print("Magma")
        return

    (hasIdentity, e) = checkIdentity(table)
    
    if not hasIdentity:
        print("Semigroup")
        return

    inv = checkInvertibility(table, e)
    comm = checkCommutativity(table)

    if inv and comm:
        print("Abelian group")
    elif inv:
        print("Group")
    elif comm:
        print("Commutative monoid")
    else:
        print("Monoid")

def checkClosure(table):
    elemCount = len(table)

    for x in range(elemCount):
        for y in range(elemCount):
            # if not an element of the set
            if table[x][y] >= elemCount:
                return False
    return True

def checkAssociativity(table):
    elemCount = len(table)

    # for each element
    for a in range(elemCount):
        # check table of (x*a)*y and x*(a*y)
        for x in range(elemCount):
            for y in range(elemCount):
                # if not an element of the set
                if table[table[x][a]][y] != table[x][table[a][y]]:
                    return False
    return True

def checkIdentity(table):
    elemCount = len(table)

    # there must exist such e
    for e in range(elemCount):
        # that for each y : e*y = y*e = y
        isIdentity = True
        for y in range(elemCount):
            isIdentity = isIdentity and table[e][y] == y and table[y][e] == y
        # if all are equal
        if (isIdentity):
            # return answer and identity
            return (True, e)

    # such x doesn't exist
    return (False, -1)

def checkInvertibility(table, e):
    elemCount = len(table)

    # for each x
    for x in range(elemCount):
        # try to find such y that x*y = y*x = e
        hasInv = False
        for y in range(elemCount):
            hasInv = hasInv or (table[x][y] == e and table[y][x] == e)
        # if doesn't have
        if not hasInv:
            return False
    # every x has inversed
    return True

def checkCommutativity(table):
    elemCount = len(table);

    # check if table is symmentric
    for x in range(1,elemCount):
        for y in range(0,x-1):
            if table[x][y] != table[y][x]:
                return False
    return True

# parse text file to table
def parseToCayleyTable(path):
    table = []
    tempRow = []
    tempString = ""
    prevColumnCount = -1

    text = open(path, "r").read()
    print(text)

    # add '\n' at the end (for easy parsing)
    if text[len(text) - 1] != '\n':
        text += '\n'

    # foreach char in the file
    for c in text:
        if c >= '0' and c <= '9':
            # if a number, add to string
            tempString += c
        else:
            # else convert current string to int
            tempRow.append(int(tempString))
            tempString = ""
        if c == '\n':
            # if end of line
            # append row to table
            table.append(tempRow)
            # check if row count are same with previous
            if len(tempRow) == prevColumnCount or prevColumnCount == -1:
                prevColumnCount = len(tempRow)
                tempRow = []
            else:
                raise ValueError("Row lengths are different")
    # if row count != column count
    if len(table) !=  prevColumnCount:
        raise ValueError("Table must be square")
    return table

if __name__ == '__main__':
    path = raw_input("Enter path: ")
    try:
        identifyAlgebraicStructure(path)
    except ValueError as err:
        print(err.args)
    except IOError as err:
        print(err.args)