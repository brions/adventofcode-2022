## Day 9 - the rope bridge
# Given a series hypothetical movements of a knotted rope head, determine the path taken
# by the extremely short knotted rope tail that can never be more than one space (cardinal or
# diagonal) away from the head.  Overlapping is ok and considered "adjacent".
##

##################
# Definitions Start Here
########################

from enum import Enum
import itertools

# simple class represting an (x,y) coordinate pair
class Coordinates:
    def __init__(self, xpos: int, ypos: int):
        self.x = xpos
        self.y = ypos
    
    def __str__(self) -> str:
        # build a display string for this TallTree
        return f'({self.x},{self.y})'
    
    def __repr__(self) -> str:
        return str(self.__str__())
    
    def __eq__(self, other: "Coordinates") -> bool:
        if other == None:
            return False
        return (self.x, self.y) == (other.x, other.y)
    
    def __ne__(self, other: "Coordinates") -> bool:
        if other == None:
            return True
        return (self.x, self.y) != (other.x, other.y)
        
    def __hash__(self):
        return (self.x, self.y).__hash__()
    
    def __getitem__(self, item) -> int:
        if item == 0 or item == 'x':
            value = self.x
        elif item == 1 or item == 'y':
            value = self.y
        else:
            raise IndexError(f'{item} is not a valid index')
        return value
    
    def __setitem__(self, item, value: int) -> None:
        if item == 0 or item == 'x':
            self.x = value
        elif item == 1 or item == 'y':
            self.y = value
        else:
            raise IndexError(f'{item} is not a valid index')
    
    def compareX(self, other: "Coordinates"):
        return self.x - other.x
                
    def compareY(self, other: "Coordinates"):
        return self.y - other.y
    
    # return true of the other coordinate is adjacent to this one in any direction
    def isAdjacent(self, other: "Coordinates") -> bool:
        # if the other is the same coordinates, then they're "adjacent"
        if other == self:
            return True
        if other == Coordinates(self['x'], self['y']+1) or other == Coordinates(self['x'], self['y']-1):
            return True
        if other == Coordinates(self['x']+1, self['y']) or other == Coordinates(self['x']-1, self['y']):
            return True
        
        return False

class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

###
# Globals
###

knots: list
ropeHead = Coordinates(0,0)
tailVistedCoordinates: set

## debugging vars
debug = False
totalTailMoves = 0
totalHeadMoves = 0
diagonalTailMoves = 0

maxX=0
minX=0
maxY=0
minY=0
## debugging vars

tailVistedCoordinates = set()

def isDiagaonallyAdjacent(head: Coordinates, tail: Coordinates) -> bool:
    ur = Coordinates(tail['x']+1, tail['y']+1)
    ul = Coordinates(tail['x']-1, tail['y']+1)
    dr = Coordinates(tail['x']+1, tail['y']-1)
    dl = Coordinates(tail['x']-1, tail['y']-1)
    return head == ur or head == ul or head == dr or head == dl
    

# translate a knot one position in a given Direction
def moveOne(knot: Coordinates, direction: Direction):
    #### DEBUG
    global debug
    global maxX
    global minX
    global maxY
    global minY
    #### DEBUG
    
    if Direction(direction) == Direction.UP:
        knot['y'] = knot['y'] + 1
        ## DEBUGGING ##
        if debug:
            if maxY < knot['y']:
                maxY = knot['y']
    elif Direction(direction) == Direction.DOWN:
        knot['y'] = knot['y'] - 1
        ## DEBUGGING ##
        if debug:
            if minY > knot['y']:
                minY = knot['y']
    elif Direction(direction) == Direction.LEFT:
        knot['x'] = knot['x'] - 1
        ## DEBUGGING ##
        if debug:
            if minX > knot['x']:
                minX = knot['x']
    elif Direction(direction) == Direction.RIGHT:
        knot['x'] = knot['x'] + 1
        ## DEBUGGING ##
        if debug:
            if maxX < knot['x']:
                maxX = knot['x']
    else:
        raise TypeError(f'Unknown direction {direction}')
    
def isTail(knot: Coordinates) -> bool:
    global knots
    return knot == knots[len(knots)-1]

# check whether or not the nextKnot is adjacent or diagonal to leadKnot, and move appropriately
# if the nextKnot is the tail, update the tailVisitedCoordinates
def moveKnot(leadKnot: Coordinates, nextKnot: Coordinates, direction: Direction):
    global diagonalTailMoves
    global totalTailMoves
    
    # calculate where nextKnot moves based on where the leadKnot is
    if not nextKnot.isAdjacent(leadKnot) and not isDiagaonallyAdjacent(leadKnot, nextKnot):
        # determine which way to move T - direction or diagonal?
        # and then translate T
        if nextKnot['x'] == leadKnot['x'] or nextKnot['y'] == leadKnot['y']:
            # just move in the closer direction one space
            if nextKnot.compareX(leadKnot) == 0:
                moveOne(nextKnot, Direction.UP) if nextKnot.compareY(leadKnot) < 0 else \
                    moveOne(nextKnot, Direction.DOWN)
            else:
                moveOne(nextKnot, Direction.LEFT) if nextKnot.compareX(leadKnot) > 0 else \
                    moveOne(nextKnot, Direction.RIGHT)

            if (isTail(nextKnot)):
                totalTailMoves += 1
        else:
            # find which diagonal is adjacent to the new rope head
            ur = Coordinates(nextKnot['x']+1, nextKnot['y']+1)
            ul = Coordinates(nextKnot['x']-1, nextKnot['y']+1)
            dr = Coordinates(nextKnot['x']+1, nextKnot['y']-1)
            dl = Coordinates(nextKnot['x']-1, nextKnot['y']-1)
            if ur.isAdjacent(leadKnot) or isDiagaonallyAdjacent(leadKnot, ur):
                nextKnot['x'] = ur['x']
                nextKnot['y'] = ur['y']
                if (isTail(nextKnot)):
                    diagonalTailMoves += 1
                    totalTailMoves += 1
            elif ul.isAdjacent(leadKnot) or isDiagaonallyAdjacent(leadKnot, ul):
                nextKnot['x'] = ul['x']
                nextKnot['y'] = ul['y']
                if (isTail(nextKnot)):
                    diagonalTailMoves += 1
                    totalTailMoves += 1
            elif dr.isAdjacent(leadKnot) or isDiagaonallyAdjacent(leadKnot, dr):
                nextKnot['x'] = dr['x']
                nextKnot['y'] = dr['y']
                if (isTail(nextKnot)):
                    diagonalTailMoves += 1
                    totalTailMoves += 1
            elif dl.isAdjacent(leadKnot) or isDiagaonallyAdjacent(leadKnot, dl):
                nextKnot['x'] = dl['x']
                nextKnot['y'] = dl['y']
                if (isTail(nextKnot)):
                    diagonalTailMoves += 1
                    totalTailMoves += 1
            else:
                raise RuntimeError(f'nextKnot is in an unexpected location. nextKnot={nextKnot}, leadKnot={leadKnot}')
        
    if (isTail(nextKnot)):
        # add T coordinates
        tailVistedCoordinates.add(Coordinates(nextKnot['x'], nextKnot['y']))

# function to translate the Head/Tail of the rope given a "movement" instruction
def moveRope(instruction: str):
    global debug
    global ropeHead
    global totalHeadMoves
    global knots
        
    direction, distance = instruction.split()
    
    ## DEBUG ##
    #prettyPrintRope(ropeHead, knots)
    ## DEBUG ##

    # loop 'distance' times without caring about the index
    for _ in itertools.repeat(None, int(distance)):
        # move H 1 space in direction
        moveOne(ropeHead, direction)
        totalHeadMoves += 1
                
        nextHead = Coordinates(ropeHead['x'], ropeHead['y'])
        for idx in range(len(knots)):
            moveKnot(nextHead, knots[idx], direction)
            nextHead = knots[idx]
            
        ## DEBUG ##
        if debug:
            prettyPrintRope(ropeHead, knots)
        ## DEBUG ##
        
def prettyPrintRope(ropeHead: Coordinates, rope: list, tailCovered:list = None) -> None:
    global minX
    global maxX
    global minY
    global maxY
    
    # find the min/max X and Y positions
    if ropeHead:
        if ropeHead['x'] < minX:
            minX = ropeHead['x']
        if ropeHead['x'] > maxX:
            maxX = ropeHead['x']
        if ropeHead['y'] < minY:
            minY = ropeHead['y']
        if ropeHead['y'] > maxY:
            maxY = ropeHead['y']
    else:
        mixX = minY = maxX = maxY = 0
    
    if rope:
        ropeMap = dict()
        knotNum = 1
        for knot in rope:
            ropeMap[knot] = knotNum
            if knot['x'] < minX:
                minX = knot['x']
            if knot['x'] > maxX:
                maxX = knot['x']
            if knot['y'] < minY:
                minY = knot['y']
            if knot['y'] > maxY:
                maxY = knot['y']
            knotNum += 1
        ropeMap[ropeHead] = 'H' if ropeHead else None
        
    if tailCovered:
        for point in tailCovered:
            if point['x'] < minX:
                minX = point['x']
            if point['x'] > maxX:
                maxX = point['x']
            if point['y'] < minY:
                minY = point['y']
            if point['y'] > maxY:
                maxY = point['y']
    
    coordinates = set()
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            coordinates.add(Coordinates(x,y))
            
    # now draw the picture
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            if 'ropeMap' in locals() and Coordinates(x,y) in ropeMap:
                print(f'{ropeMap[Coordinates(x,y)]}', end='')
            elif tailCovered and Coordinates(x,y) in tailCovered:
                print('#', end='')
            elif Coordinates(x,y) == Coordinates(0,0):
                print('s', end='')
            else:
                print('.', end='')            
        print('\n', end='')
    print('')

##################
# Logic Start Here
########################

## Part 1
def part1() -> None:
    global debug
    global knots
    global totalHeadMoves
    global totalTailMoves
    global tailVistedCoordinates
    global diagonalTailMoves
    
    knotCount = 2
    knots = [Coordinates(0,0) for x in range(knotCount-1)]

    ## DEBUG
    if debug:
        instructionCount = 0
    ## DEBUG 

    # run through all the moves, translating the head(H) and tail(T) of the rope and adding T-visited
    # coordinates to tailVisitedCoordinates
    for move in moves:
        if debug:
            instructionCount += 1
            print(f'--------\n{move}')
        moveRope(move)

    print(f'Tail visited {len(tailVistedCoordinates)} unique coordinates')
    if debug:
        print(f'instructionCount: {instructionCount}\ntotalHeadMoves: {totalHeadMoves}\ntotalTailMoves: {totalTailMoves}\ndiagonalTailMoves: {diagonalTailMoves}')

    if debug:
        # plot the grid and tail traveled
        prettyPrintRope(None, None, tailVistedCoordinates)
    # for y in range(minY, maxY+1):
    #     for x in range(minX, maxX+1):
    #         if Coordinates(x,y) in tailVistedCoordinates:
    #             print('#', end='')
    #         else:
    #             print('.', end='')
            
    #         if x == maxX:
    #             print('')

## Part 2

def part2() -> None:
    global knots
    global ropeHead
    global maxX
    global maxY
    global minX
    global minY
    global totalHeadMoves
    global totalTailMoves
    global tailVistedCoordinates
    global diagonalTailMoves
        
    ## reset globals
    knotCount = 10
    knots = [Coordinates(0,0) for x in range(knotCount-1)]
    ropeHead = Coordinates(0,0)
    tailVistedCoordinates = set()
    totalHeadMoves = 0
    totalTailMoves = 0
    diagonalTailMoves = 0
    maxX=0
    maxY=0
    minX=0
    minY=0
    instructionCount=0

    try:
        for move in moves:
            if debug:
                instructionCount += 1
                print(f'--------\n{move}')
            moveRope(move)
    except Exception as e:
        print(f'Caught error: {e}')
        
    print(f'Tail visited {len(tailVistedCoordinates)} unique coordinates')
    if debug:
        print(f'instructionCount: {instructionCount}\ntotalHeadMoves: {totalHeadMoves}\ntotalTailMoves: {totalTailMoves}\ndiagonalTailMoves: {diagonalTailMoves}')

    # plot the grid and tail traveled
    if debug:
        prettyPrintRope(None, None, tailVistedCoordinates)
    # for y in range(minY, maxY+1):
    #     for x in range(minX, maxX+1):
    #         if Coordinates(x,y) in tailVistedCoordinates:
    #             print('#', end='')
    #         else:
    #             print('.', end='')
            
    #         if x == maxX:
    #             print('')

#### main execution area ####
import getopt
import sys

opts, args = getopt.getopt(sys.argv[1:], 'dp:f:', ["debug", "part=", "file="])

availableParts = {'1': part1, '2': part2}

executeParts = []
inputFile = 'input.txt'

for opt, value in opts:
    if opt == '-p' or opt == '--part':
        executeParts.append(value)
    elif opt == 'f' or opt == '--file':
        inputFile = value
    elif opt == 'd' or opt == '--debug':
        debug = True
        
# read input to get set of hypothetical moves
fh = open(inputFile, 'r')
moves = list(map(lambda l: l.strip(), fh.readlines()))

for part in executeParts:
    if part in availableParts:
        availableParts[part]()

