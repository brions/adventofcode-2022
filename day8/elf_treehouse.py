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
from enum import Enum

# simple class represting an (x,y) coordinate tuple
class Coordinates:
    def __init__(self, coordinates: tuple):
        self.coordinates = coordinates
    
    def __str__(self) -> str:
        # build a display string for this TallTree
        return f'{self.coordinates}'
    
    def __repr__(self) -> str:
        return str(self.__str__())
    
    def __eq__(self, other: "Coordinates") -> bool:
        if other == None:
            return False
        isEq = self.coordinates[0] == other.coordinates[0] and \
            self.coordinates[1] == other.coordinates[1]
        return isEq
    
    def __ne__(self, other: "Coordinates") -> bool:
        if other == None:
            return True
        isEq = self.coordinates[0] != other.coordinates[0] or \
            self.coordinates[1] != other.coordinates[1]
        return isEq
        
    def __hash__(self):
        return self.coordinates.__hash__()
    
    def __getitem__(self, item) -> int:
        return self.coordinates[item]
    
    def compareCoord0(self, other: int):
        return self.coordinates[0] - other
                
    def compareCoord1(self, other: int):
        return self.coordinates[1] - other
    
    # return true of the other coordinate is adjacent to this one in any direction
    def isAdjacent(self, other: "Coordinates") -> bool:
        # if the other is the same coordinates, then they're "adjacent"
        if other == self:
            return True
        if other[0] == self[0]+1 or other[0] == self[0]-1:
            return True
        if other[1] == self[1]+1 or other[1] == self[1]-1:
            return True
        
        return False
        

## DEBUG
# if Coordinates((0, 1)) == Coordinates((0, 1)):
#     print('Yay equality!')
# else:
#     print('Boo! LOGIC!')
## DEBUG

# A Python class that represents an individual Tree
class TallTree:
    def __init__(self, height: int, coordinates: Coordinates):
        self.height = height
        self.coordinates = coordinates
    
    def __str__(self) -> str:
        # build a display string for this TallTree
        return f'{self.coordinates} {self.height}'
    
    def __repr__(self) -> str:
        return str(self.__str__())
    
    def __eq__(self, obj: "TallTree"):
        if obj == None:
            return False
        isEq = self.height == obj.height
        isEq = isEq and (self.coordinates == obj.coordinates)
        return isEq
    
    def __getitem__(self, item) -> int:
        return self.coordinates[item]
        
    def __hash__(self):
        hash = self.height.__hash__()
        hash += self.coordinates.__hash__()
        return hash.__hash__()

def compareTreeByCoordinate0(tree1: TallTree, tree2: TallTree) -> int:
    return tree1.coordinates.compareCoord0(tree2.coordinates[0])    
    
def compareTreeByCoordinate1(tree1: TallTree, tree2: TallTree) -> int:
    return tree1.coordinates.compareCoord1(tree2.coordinates[1])    
    
# try to sort a set of trees by coordinate dimension into a list
def sortSet(treeSet: set, sortCoord: int) -> list:
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

## MOAR debugging    
# if TallTree((0, 1), 5) == TallTree((0, 1), 5):
#     print('yay equality again!')
# else:
#     print('sadge')
    
# testSet = set()
# testSet.add(TallTree((0, 1), 5))
# testSet.add(TallTree((0, 1), 5))
# print(f'testSet size: {len(testSet)}\n{testSet}')
## you know...

## Part 1 ##
fh = open('input.txt', 'r')

forest = list()

# sort any set of trees
def prettyPrintSet(treeSet, msg: str):
    orderedTrees = sortSet(treeSet, 0)
    treeline = "\n".join(map(str, orderedTrees))
    print(f'{msg}: \n{treeline}')


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
#print(f'forest is:\n{forest}')

# this will hold the same trees 90deg from their original positions, so each row == column of the orignal forest
rotatedForest = [[] for i in range(len(forest[0]))]

# rotate the forest
for line in forest:
    colIdx = 0
    for height in line:
        rotatedForest[colIdx].append(height)
        colIdx += 1

# print rotate forest
#print(f'rotated forest: {rotatedForest}')

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
    tallestTreeRowList.append(sortSet(tallestTreesSoFar, 1))
    

#prettyPrintSet(tallestTreeRowList, 'tallest trees in each row')

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
    tallestTreeColList.append(sortSet(tallestTreesSoFar, 0))

# treeline = "\n".join(map(str, tallestTreeColList))
# print(f'tallest trees in each column: \n{treeline}')
#prettyPrintSet(tallestTreeColList, 'tallest trees in each column')

# Find the visible trees in each row by starting from the tallest left most and finding the next
# tallest leftmost tree, and so on until we reach the edge.  Then repeat from the rightmost tallest
# tree to the rightmost edge. The set of unique trees visible from both runs == visible trees for 
# the row

# this set holds the superset of all visible tree sets calculated below
allVisibleTrees = set()

rowIdx = 0
forestRightEdge = len(forest[0])-1
for row in forest:
    if rowIdx == 0 or rowIdx == forestRightEdge:
        # for the first row, and the last row, add all trees and continue
        allVisibleTrees.update(row)
        rowIdx += 1
        continue
        
    visibleTreesInRow = set()

    # get the leftmost tallest tree coordinates
    tallTreeRowList = tallestTreeRowList[rowIdx]
    startingTree = tallTreeRowList[0]
    visibleTreesInRow.add(startingTree)
    
    nextHeight = startingTree.height - 1
    nextHeightTree = None

    # find everything visible to the left of tallest leftmost tree
    leftmostVisibleTree = None
    while(nextHeight > 0):
        for tree in reversed(row[0:startingTree[1]]):
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                leftmostVisibleTree = tree
        if leftmostVisibleTree:
            visibleTreesInRow.add(leftmostVisibleTree)
            startingTree = leftmostVisibleTree

        # exit if we've hit the left edge
        if leftmostVisibleTree and leftmostVisibleTree[1] == 0:
            break

        nextHeight -= 1

    # get the rightmost tallest tree coordinates    
    startingTree = tallTreeRowList[len(tallTreeRowList)-1]
    visibleTreesInRow.add(startingTree)
    
    nextHeight = startingTree.height - 1
    nextHeightTree = None

    # find everything to the right of tallest rightmost tree
    while(nextHeight > 0):
        for tree in row[startingTree[1] + 1:]:
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                nextHeightTree = tree
        if nextHeightTree:
            visibleTreesInRow.add(nextHeightTree)
            startingTree = nextHeightTree

        # exit if we've hit the right edge
        if nextHeightTree and nextHeightTree[1] == forestRightEdge:
            break

        nextHeight -= 1

    allVisibleTrees.update(visibleTreesInRow)
    rowIdx += 1

#print(f'found {len(allVisibleTrees)} in forest rows')
#prettyPrintSet(allVisibleTrees, 'found row trees')

# Find the visible trees in each column by starting from the tallest leftmost tree and finding the next
# tallest leftmost tree, and so on until we read the edge.  Then repeat from the rightmost tallest
# tree to the rightmost edge. The set of unique trees visible from both runs == visible trees for 
# the column

colIdx = 0
rotatedForestRightEdge = len(rotatedForest[0])-1
for row in rotatedForest:
    if colIdx == 0 or colIdx == rotatedForestRightEdge:
        # for the first row (column), or the last row (column), add all trees and continue
        allVisibleTrees.update(row)
        colIdx += 1
        continue
        
    visibleTreesInCol = set()
    
    # get the leftmost tallest tree coordinates to start
    tallTreeColList = tallestTreeColList[colIdx]
    startingTree = tallTreeColList[0]
    visibleTreesInCol.add(startingTree)
    
    nextHeight = startingTree.height - 1
    nextHeightTree = None
    
    # NOTE: don't forget to rotate the coordinates in the rotated forest!
    while(nextHeight > 0):
        for tree in reversed(row[0:startingTree[0]]):
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                nextHeightTree = tree
        if nextHeightTree:
            visibleTreesInCol.add(nextHeightTree)
            startingTree = nextHeightTree

        # exit if we've hit the left edge
        if nextHeightTree and nextHeightTree[0] == 0:
            break

        nextHeight -= 1
    
    # get the rightmost tallest tree coordinates
    startingTree = tallTreeColList[len(tallTreeColList)-1]
    visibleTreesInCol.add(startingTree)

    nextHeight = startingTree.height - 1
    nextHeightTree = None

    # find everything to the right of tallest rightmost tree
    while(nextHeight > 0):
        for tree in row[startingTree[0] + 1:]:
            if tree.height < nextHeight:
                continue
            elif tree.height == nextHeight:
                nextHeightTree = tree
        if nextHeightTree:
            visibleTreesInCol.add(nextHeightTree)
            startingTree = nextHeightTree

        # exit if we've hit the right edge
        if nextHeightTree and nextHeightTree[1] == rotatedForestRightEdge:
            break

        nextHeight -= 1

    allVisibleTrees.update(visibleTreesInCol)
    colIdx += 1

#prettyPrintSet(allVisibleTrees, 'allVisibleTrees')
print(f'total visible trees: {len(allVisibleTrees)}')


## Part 2
# Scenic score = distance * 4 directions from any given tree
# distance = count of trees from starting to edge or height >= starting tree.height
##

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# calculate how many trees can be seen from the baseTree of the forest in the given direction
def lineOfSight(baseTree: TallTree, forest: list, direction: Direction) -> int:
    visibleDistance = 0
    maxHeight = baseTree.height
    
    if direction == Direction.UP:
        targetCol = baseTree[1]
        # run through all the trees from the starting row back to the first in this column
        for pos in reversed(range(baseTree[0])):
            nextTree = forest[pos][targetCol]
            if nextTree == baseTree:
                continue
            
            if nextTree.height <= maxHeight:
                visibleDistance += 1
                if (nextTree.height == maxHeight):
                    # count the same height, but then we're done
                    break
            else:
                visibleDistance +=1
                # once we can't see anymore - we're done.
                break
    elif direction == Direction.DOWN:
        targetCol = baseTree[1]
        # run through all the trees from the starting row to the last in this column
        for pos in range(baseTree[0], len(forest)):
            nextTree = forest[pos][targetCol]
            if nextTree == baseTree:
                continue
            
            if nextTree.height <= maxHeight:
                visibleDistance += 1
                if (nextTree.height == maxHeight):
                    # count the same height, but then we're done
                    break
            else:
                visibleDistance +=1
                # once we can't see anymore - we're done.
                break
    elif direction == Direction.LEFT:
        targetRow = baseTree[0]
        # run through all the trees from the starting column back to zero in this row
        for pos in reversed(range(baseTree[1])):
            nextTree = forest[targetRow][pos]
            if nextTree == baseTree:
                continue
            
            if nextTree.height <= maxHeight:
                visibleDistance += 1
                if (nextTree.height == maxHeight):
                    # count the same height, but then we're done
                    break
            else:
                visibleDistance +=1
                # once we can't see anymore - we're done.
                break
    elif direction == Direction.RIGHT:
        targetRow = baseTree[0]
        # run through all the trees from the starting column to the last in this row
        for pos in range(baseTree[1], len(forest[targetRow])):
            nextTree = forest[targetRow][pos]
            if nextTree == baseTree:
                continue
            
            if nextTree.height <= maxHeight:
                visibleDistance += 1
                if (nextTree.height == maxHeight):
                    # count the same height, but then we're done
                    break
            else:
                visibleDistance +=1
                # once we can't see anymore - we're done.
                break
    
    return visibleDistance
    

# map of tree -> score
scenicScoreMap = dict()

startingCoordinates: Coordinates
startingHeight: int
for treeline in forest:
    for tree in treeline:
        scenicScore: int
        startingCoordinates = tree.coordinates
        startingHeight = tree.height
        
        scenicScore = lineOfSight(tree, forest, Direction.LEFT)
        scenicScore = scenicScore * lineOfSight(tree, forest, Direction.RIGHT)
        scenicScore = scenicScore * lineOfSight(tree, forest, Direction.UP)
        scenicScore = scenicScore * lineOfSight(tree, forest, Direction.DOWN)
        
        scenicScoreMap[tree] = scenicScore
    
# now that we have all the scores, find the highest
highest = [None,0]
for tree, score in scenicScoreMap.items():
    if score > highest[1]:
        highest = [tree, score]

#print(f'DEBUG: scenicScoreMap: {scenicScoreMap}')
print(f'Highest scenic score is tree {highest[0]} with a score of {highest[1]}')