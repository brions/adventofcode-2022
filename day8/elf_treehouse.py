## Day 8 - Hiding the Tree House
# given a grid map of tree heights, find the number of trees visible from outside the grid
# taller trees (9) obscure shorter trees (0); consider only row and column visbility
##

# for a row:
#  1. find the tallest tree from the left - record its column
#  2. find the tallest tree from the right - record its column
#
# for a column:
#  1. find the tallest tree from the top - record its row
#  2. find the tallest tree from the bottom - record its row
#
# Solution == sum of all the tallest trees that are unique coordinates

from functools import total_ordering, cmp_to_key

# simple class represting an (x,y) coordinate tuple
class Coordinates:
    def __init__(self, coordinates: tuple):
        self.coordinates = coordinates
    
    def __str__(self) -> str:
        # build a display string for this TallTree
        return f'{self.coordinates}'
    
    def __repr__(self) -> str:
        return str(self.__str__())
    
    def __eq__(self, obj: "Coordinates"):
        if obj == None:
            return False
        isEq = isEq and (self.coordinates == self.coordinates)
        return isEq
        
    def __hash__(self):
        return self.coordinates.__hash__()
    
    def __getitem__(self, item):
        return self.coordinates[item]
    
    def compareCoord0(self, other: int):
        return self.coordinates[0] - other
                
    def compareCoord1(self, other: int):
        return self.coordinates[1] - other

# A Python class that represents an individual Tree
@total_ordering
class TallTree:
    def __init__(self, height: int, coordinates: Coordinates):
        self.height = height
        self.coordinates = coordinates
    
    def __str__(self) -> str:
        # build a display string for this TallTree
        return f'{self.coordinates} {self.height}'
    
    def __repr__(self) -> str:
        return str(self.__str__())
    
    def __lt__(self, obj: "TallTree"):
        if obj == None:
            return False

    def __gt__(self, obj: "TallTree"):
        if obj == None:
            return False
    
    def __eq__(self, obj: "TallTree"):
        if obj == None:
            return False
        isEq = self.height == obj.height
        isEq = isEq and (self.coordinates == self.coordinates)
        return isEq
        
    def __hash__(self):
        hash = self.height.__hash__()
        hash += self.coordinates.__hash__()
        return hash.__hash__()

def compareTreeByCoordinate0(tree1: TallTree, tree2: TallTree) -> int:
    return tree1.coordinates.compareCoord0(tree2.coordinates[0])    
    
def compareTreeByCoordinate1(tree1: TallTree, tree2: TallTree) -> int:
    return tree1.coordinates.compareCoord1(tree2.coordinates[1])    
    
# try to sort a set of trees by coordinate dimension into a list
def sortBy(treeSet: set, sortCoord: int) -> list:
    sortedList = None
    if sortCoord == 0:
        sortedList = sorted(treeSet, key=cmp_to_key(compareTreeByCoordinate0))
    else:
        sortedList = sorted(treeSet, key=cmp_to_key(compareTreeByCoordinate1))
        
    # for tree in treeSet:
    #     if not sortedList:
    #         sortedList = list([tree])
    #     else:
    #         for elem in sortedList:
    #             idx = 0
    #             if sortCoord == 0:
    #                 if elem.coordinates.compareCoord0(tree.coordinates[0]) < 0:
    #                     sortedList.insert(idx, tree)
    #                 else:
    #                     sortedList.insert(idx + 1, tree)
    #             else:
    #                 if elem.coordinates.compareCoord1(tree.coordinates[1]) < 0:
    #                     sortedList.insert(idx + 1, tree)
    #                 else:
    #                     sortedList.insert(idx, tree)
    #             idx += 1
    return sortedList

## Part 1 ##
fh = open('input-sample.txt', 'r')

forest = list()

def buildTreeLine(line: str, rowIndex: int) -> list:
    row = list()
    columnIndex = 0
    for height in line:        
        row.append(TallTree(int(height), Coordinates((rowIndex, columnIndex))))
        columnIndex += 1
    return row

rowIndex = 0
# read in each line at a time and populate a matrix (n*x array) of trees
for line in list(map(lambda l: l.strip(), fh.readlines())):
    forest.append(buildTreeLine(line, rowIndex))
    rowIndex += 1
    
# print out the forest
print(f'forest is:\n{forest}')

# this will hold the same trees 90deg from their original positions, so each row == column of the orignal forest
rotatedForest = [[] for i in range(len(forest[0]))]

# rotate the forest
for line in forest:
    colIdx = 0
    for height in line:
        rotatedForest[colIdx].append(height)
        colIdx += 1

# print rotate forest
print(f'rotated forest: {rotatedForest}')

# hold the unique set of tallest tree(s) in each row and each column
tallestTreeRowList = list()
tallestTreeColList = list()

# search each row of the forest for the tallest tree(s) and add them to the treeRowSet
for row in forest:
    maxHeight = 0
    tallestTreesSoFar = set()
    for tree in row:
        if tree.height > maxHeight:
            tallestTreesSoFar.clear()
            maxHeight = tree.height
            tallestTreesSoFar.add(tree)
        elif tree.height == maxHeight:
            tallestTreesSoFar.add(tree)
    tallestTreeRowList.append(sortBy(tallestTreesSoFar, 1))
    

treeline = "\n".join(map(str, tallestTreeRowList))
print(f'tallest trees in each row: \n{treeline}')

# search each column of the forest
for row in rotatedForest:
    maxHeight = 0
    tallestTreesSoFar = set()
    for tree in row:
        if tree.height > maxHeight:
            tallestTreesSoFar.clear()
            maxHeight = tree.height
            tallestTreesSoFar.add(tree)
        elif tree.height == maxHeight:
            tallestTreesSoFar.add(tree)
    tallestTreeColList.append(sortBy(tallestTreesSoFar, 0))

treeline = "\n".join(map(str, tallestTreeColList))
print(f'tallest trees in each column: \n{treeline}')

# Find the visible trees in each row by starting from the tallest left most and finding the next
# tallest leftmost tree, and so on until we read the edge.  Then repeat from the rightmost tallest
# tree to the rightmost edge. The set of unique trees visible from both runs == visible trees for 
# the row

# this set holds the superset of all visible tree sets calculated below
allVisibleTrees = set()

rowIdx = 0
for row in forest:
    if rowIdx == 0 or rowIdx == len(forest[0]):
        # for the first row, and the last row, add all trees
        allVisibleTrees.update(row)
        
    visibleTreesInRow = set()

    # get the leftmost tallest tree coordinates
    tallTreeRowList = tallestTreeRowList[rowIdx]
    tallestTree = tallTreeRowList[0]
    visibleTreesInRow.add(tallestTree)
    
    nextHeight = tallestTree.height - 1
    nextHeightTree = None

    # find everything to the left of tallest leftmost tree
    while(nextHeight > 0):
        for tree in reversed(row[0:tallestTree.coordinates[1]]):
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                nextHeightTree = tree
        if nextHeightTree:
            visibleTreesInRow.add(nextHeightTree)
        nextHeight -= 1

    # get the rightmost tallest tree coordinates    
    tallestTree = tallTreeRowList[len(tallTreeRowList)-1]
    visibleTreesInRow.add(tallestTree)

    nextHeight = tallestTree.height - 1
    nextHeightTree = None

    # find everything to the right of tallest rightmost tree
    while(nextHeight > 0):
        for tree in row[tallestTree.coordinates[1] + 1:]:
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                nextHeightTree = tree
        if nextHeightTree:
            visibleTreesInRow.add(nextHeightTree)
        nextHeight -= 1

    allVisibleTrees.update(visibleTreesInRow)
    rowIdx += 1

print(f'found {len(allVisibleTrees)} in forest rows')

# Find the visible trees in each column by starting from the tallest leftmost tree and finding the next
# tallest leftmost tree, and so on until we read the edge.  Then repeat from the rightmost tallest
# tree to the rightmost edge. The set of unique trees visible from both runs == visible trees for 
# the column

colIdx = 0
for row in rotatedForest:
    if colIdx == 0 or colIdx == len(rotatedForest[0]):
        # for the first row (column), and the last row (column), add all trees
        allVisibleTrees.update(row)
        
    visibleTreesInCol = set()
    
    # get the leftmost tallest tree coordinates
    tallTreeColList = tallestTreeColList[colIdx]
    tallestTree = tallTreeColList[0]
    visibleTreesInCol.add(tallestTree)
    
    nextHeight = tallestTree.height - 1
    nextHeightTree = None
    
    while(nextHeight > 0):
        for tree in reversed(row[0:tallestTree.coordinates[0]]):
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                nextHeightTree = tree
        if nextHeightTree:
            visibleTreesInCol.add(nextHeightTree)
        nextHeight -= 1
    
    # get the rightmost tallest tree coordinates
    tallestTree = tallTreeColList[len(tallTreeColList)-1]
    visibleTreesInCol.add(tallestTree)

    nextHeight = tallestTree.height - 1
    nextHeightTree = None

    # find everything to the right of tallest rightmost tree
    while(nextHeight > 0):
        for tree in row[tallestTree.coordinates[1] + 1:]:
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                nextHeightTree = tree
        if nextHeightTree:
            visibleTreesInCol.add(nextHeightTree)
        nextHeight -= 1

    allVisibleTrees.update(visibleTreesInCol)
    colIdx += 1

print(f'total visible trees: {len(allVisibleTrees)}')
treelist = "\n".join(map(str, sortBy(allVisibleTrees, 0)))
print(f'allVisibleTrees: \n{treelist}')