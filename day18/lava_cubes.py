from helpers import Coordinates3D, parseAndLoad, runLines, readLines, debug
from queue import Queue

###
# Objects
#####


###
# Globals
#####
lavaSet = set()
waterSet = set()
totalFaces:int
maxDimensions: list
minDimension = -1
nextQueue: Queue

###
# Main execution
#####

        
def reset(lines):
    global lavaSet, totalFaces, maxDimensions, nextQueue
    totalFaces = 0
    maxDimensions = [0 for pos in range(3)]
    waterSet.clear()
    lavaSet.clear()
    nextQueue = Queue()
    
    for line in list(map(lambda ln: ln.strip(), lines)):
        coords = line.split(',')
        cube = Coordinates3D(int(coords[0]), int(coords[1]), int(coords[2]))
        lavaSet.add(cube)
        if cube['x'] > maxDimensions[0]:
            maxDimensions[0] = cube['x']
        if cube['y'] > maxDimensions[1]:
            maxDimensions[1] = cube['y']
        if cube['z'] > maxDimensions[2]:
            maxDimensions[2] = cube['z']
    
    # expand the maxDimensions by 1 in every direction so we can successfully flood fill
    # the external space (there is always at least 1 adjacent external cube)
    maxDimensions[0] += 1
    maxDimensions[1] += 1
    maxDimensions[2] += 1
    debug(f'lavaSet: {len(lavaSet)}')
    
    
def part1(lines, args):
    reset(lines)


def checkPoint(point: Coordinates3D):
    """Creates 6 test points from this point and checks all of their coordinate values
    against the bounds adding points within bounds into the work queue.

    Args:
        point (Coordinates3D): origin test point
    """
    global nextQueue, lavaSet, totalFaces

    xpos = Coordinates3D(point['x'] + 1, point['y'], point['z'])
    xneg = Coordinates3D(point['x'] - 1, point['y'], point['z'])
    ypos = Coordinates3D(point['x'], point['y'] + 1, point['z'])
    yneg = Coordinates3D(point['x'], point['y'] - 1, point['z'])
    zpos = Coordinates3D(point['x'], point['y'], point['z'] - 1)
    zneg = Coordinates3D(point['x'], point['y'], point['z'] + 1)

    for p in [xpos, xneg, ypos, yneg, zpos, zneg]:
        if p['x'] >= minDimension and p['y'] >= minDimension and p['z'] >= minDimension and \
           p['x'] <= maxDimensions[0] and p['y'] <= maxDimensions[1] and \
           p['z'] <= maxDimensions[2]:
            if p not in lavaSet:
                nextQueue.put(p)
            else:
                totalFaces += 1
        

def checkX(point: Coordinates3D):
    global nextQueue, lavaSet, totalFaces

    pointEdge = Coordinates3D(point['x'] + 1, point['y'], point['z'])
    if point['x'] >= minDimension and point['x'] + 1 < maxDimensions[0] + 1:
        if pointEdge not in lavaSet:
            nextQueue.put(pointEdge)
        else:
            totalFaces += 1
    pointEdge = Coordinates3D(point['x'] - 1, point['y'], point['z'])
    if point['x'] - 1 >= minDimension and point['x'] < maxDimensions[0] + 1:
        if pointEdge not in lavaSet:
            nextQueue.put(pointEdge)
        else:
            totalFaces += 1    


def checkY(point: Coordinates3D):
    global nextQueue, lavaSet, totalFaces

    pointEdge = Coordinates3D(point['x'], point['y'] + 1, point['z'])
    if pointEdge['y'] >= minDimension and pointEdge['y'] < maxDimensions[0] + 1:
        if pointEdge not in lavaSet:
            nextQueue.put(pointEdge)
        else:
            totalFaces += 1
    pointEdge = Coordinates3D(point['x'], point['y'] - 1, point['z'])
    if pointEdge['y'] >= minDimension and pointEdge['y'] < maxDimensions[0] + 1:
        if pointEdge not in lavaSet:
            nextQueue.put(pointEdge)
        else:
            totalFaces += 1    


def checkZ(point: Coordinates3D):
    global nextQueue, lavaSet, totalFaces

    pointEdge = Coordinates3D(point['x'], point['y'], point['z'] - 1)
    if point['z'] >= minDimension and point['z'] < maxDimensions[0] + 1:
        if pointEdge not in lavaSet:
            nextQueue.put(pointEdge)
        else:
            totalFaces += 1
    pointEdge = Coordinates3D(point['x'], point['y'], point['z'] + 1)
    if point['z'] >= minDimension and point['z'] < maxDimensions[0]:
        if pointEdge not in lavaSet:
            nextQueue.put(pointEdge)
        else:
            totalFaces += 1    


def part2(lines, args):
    global lavaSet, totalFaces
    reset(lines)
    
    debugCounter = 0
    
    # now that we've read in the entire lava rock and discovered the max dimensions
    # build the 3D volumetric space and start a flood fill on the edge of that space
    # that is not part of the lava rock
    origin = Coordinates3D(-1,-1,-1)

    # test all the points around the origin first, add any that aren't lava points to
    # the queue for futher testing, count all the ones that are lava points as a face
    checkPoint(origin)
    
    while not nextQueue.empty():
        debugCounter += 1
        # pop the queue
        # check all adjacent points to see if they're in the cubeSet
        # if so, add 1 to totalFaces and drop that point
        # otherwise add the point (within bounds) to the queue
        test = nextQueue.get()
        if test in waterSet:
            # we've already tested this, skip
            continue
        # add this to the waterSet
        waterSet.add(test)
        
        # test all the points around this test point, add any that aren't lava points to
        # the queue for futher testing
        checkPoint(test)
            
        if debugCounter % 100 == 0:
            # done loading cubes and comparing them
            debug(f'Total cubes: {len(lavaSet)}')
            debug(f'Total exposed lava faces: {totalFaces}')

    # done loading cubes and comparing them
    print(f'Total cubes: {(maxDimensions[0]-minDimension) * (maxDimensions[1]-minDimension) * (maxDimensions[2]-minDimension)}')
    print(f'Total lava cubes: {len(lavaSet)}')
    print(f'Total water cubes: {len(waterSet)}')
    print(f'Total exposed lava faces: {totalFaces}')

# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel, args = parseAndLoad()
lines = readLines(inputfile)
partsMap = {"1": part1, "2": part2}
runLines(parts, partsMap, lines, args)