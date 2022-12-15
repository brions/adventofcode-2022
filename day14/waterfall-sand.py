from helpers import Coordinates, openFile, runFile, parseAndLoad, debug, getLogLevel, LogLevel
from io import TextIOWrapper

sandSource = Coordinates(500, 0)
pileOsand = set()
abyss = 0

# debugging
rockMatrix: list
minX = 500
maxX = 500
minY = 0
maxY = 0


class Segment:
    def __init__(self, c1: Coordinates, c2: Coordinates) -> None:
        self.left = c1
        self.right = c2
        
    def __eq__(self, __o: object) -> bool:
        return self.left == __o.left and self.right == __o.right
    
    def __hash__(self) -> int:
        return (self.left, self.right).__hash__()
    
    def intersects(self, coord: Coordinates) -> bool:
        minX = min(self.left['x'], self.right['x'])
        maxX = max(self.left['x'], self.right['x'])
        if (coord['x'] >= minX and coord['x'] <= maxX) and \
           (coord['y'] == self.left['y'] or coord['y'] == self.right['y']):
            return True
        return False


class RockLine:
    def __init__(self, coordinates: list) -> None:
        self.coordinates = coordinates
        self.segments = set()
        
        # build the sets from the coordinates
        previousCoord = None
        for coordinate in coordinates:
            if previousCoord is not None:
                self.segments.add(Segment(previousCoord, coordinate))
            previousCoord = coordinate
    
    def __str__(self) -> str:
        coordinateString = " -> ".join(list(map(lambda coord: coord.__str__(),
                                                self.coordinates)))
        return f'<{coordinateString}>'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def adjacentBelow(self, coord: Coordinates) -> bool:
        """Determine whether or not this RockLine is adjacent below the given
        coordinate. This could be directly below or at a diagonal

        Args:
            coord (Coordinates): the coordinate to check

        Returns:
            bool: True if the Rockline is immediately adjacent to the
            coordinate; False otherwise
        """
        for segment in self.segments:
            if segment.intersects(Coordinates(coord['x'], coord['y']+1)):
                return True

        return False
    
    def getCoordinates(self) -> list:
        return self.coordinates

    
#####
# Main logic
###

def dropSand(rocklines: list) -> Coordinates:
    """Simulates the drop of a single grain of sand from the source against a 
    list of RockLines and determine where its final resting coordinte is

    Args:
        rockRidges (list): list of RockLines to test for intersection with
        the path of the falling sand.

    Returns:
        Coordinates: final resting coordinates of the piece of sand. If
        sand falls into the abyss, return None
    """
    global pileOsand, abyss, rockMatrix

    grainPos = sandSource
    landed = False
    
    while not landed:
        testGrain = Coordinates(grainPos['x'], grainPos['y']+1)
        
        # check for the abyss
        if testGrain['y'] >= int(abyss+1):
            # we've fallen into it ... aaaaaaaaaaaaaaaaaahhhhhhhhhhhhhhh
            debug('oh no! the abyss!!')
            break
        
        if pileOsand:
            if testGrain in pileOsand:
                # there is sand directly below, check down-left
                if Coordinates(testGrain['x']-1, testGrain['y']) in pileOsand:
                    # there is sand below and to the left, check down-right
                    if Coordinates(testGrain['x']+1, testGrain['y']) in pileOsand:
                        # there is sand below and to the right too....dang it
                        landed = True
                    else:
                        testGrain['x'] = testGrain['x'] + 1
                else:
                    testGrain['x'] = testGrain['x'] - 1

        if not landed:
            if len(rockMatrix) > testGrain['y'] and rockMatrix[testGrain['y']]:
                for x in rockMatrix[testGrain['y']]:
                    if x == testGrain['x']:
                        # we hit a rock, check down-left
                        if rockMatrix[testGrain['y']] == testGrain['x']-1:
                            # we hit a rock again, check down-right
                            if len(testGrain) < testGrain['y'] + 1:
                                # nothing left to test against, but we didn't land
                                break
                            if rockMatrix[testGrain['y']+1] == testGrain['x']+1:
                                # more rock...we're stuck here
                                landed = True
                                break
                            else:
                                testGrain['x'] = testGrain['x'] + 1
                                break
                        else:
                            testGrain['x'] = testGrain['x'] - 1
                            break
        
        if not landed:
            # if we've gotten here, we've hit nothing - update the grainPos
            grainPos = testGrain

    debug(f'landed? {landed}')
    if not landed:
        return None
    debug(f'next grainPos: {grainPos}')
    return grainPos


def printCavern() -> None:
    global rockMatrix, pileOsand, minX, minY, maxX, maxY
    
    if getLogLevel() < LogLevel.DEBUG:
        return

    # generate the "image"
    # a '.' for every point in the coordinate plane that isn't in
    # 'rockMatrix' or 'pileOSand'
    for y in range(minY, maxY):
        for x in range(minX-1, maxX+1):
            point = Coordinates(x, y+1)
            if point in pileOsand:
                print('o', end='')
            elif x in rockMatrix[y]:
                print('#', end='')
            else:
                print('.', end='')
        print('')

    print('----')


def part1(file: TextIOWrapper):
    global sandSource, abyss, rockMatrix
    
    # debugging
    global minX, maxX, minY, maxY
    
    rockRidges = list()
    
    for line in list(map(lambda next: next.strip(), file.readlines())):
        lineCoords = list()
        
        coordinatePairs = line.split(' -> ')
        for x, y in list(map(lambda pair: pair.split(','), coordinatePairs)):
            lineCoords.append(Coordinates(int(x), int(y)))
            if int(y) > int(abyss):
                abyss = int(y)
            
            # debugging
            if int(x) < minX:
                minX = int(x)
            elif int(x) > maxX:
                maxX = int(x)
            elif int(y) > maxY:
                maxY = int(y)
            
        rockRidges.append(RockLine(lineCoords))
    debug(f'rock ridges: {rockRidges}')
    
    # build a matrix of y=0 -> y=maxY
    # for every coordinate of the rocklines add the X coordinate to the appropriate
    # y row (filling in all x coords that make up a segment)
    rockMatrix = [set() for x in range(maxY)]
    for line in rockRidges:
        start: Coordinates = None
        end: Coordinates = None
        for point in line.coordinates:
            if start is None:
                start = point
                rockMatrix[start['y']-1].add(start['x'])
                continue
            end = point
            
            if start['x'] == end['x']:
                # build a vertical line of points ['y'] long
                length = abs(start['y'] - end['y']) + 1
                m = min(start['y'], end['y'])
                x = max(start['y'], end['y'])
                for i in range(m, m+length):
                    rockMatrix[i-1].add(start['x'])
            elif start['y'] == end['y']:
                # build a horizontal line of points ['x'] long
                length = abs(start['x'] - end['x']) + 1
                m = min(start['x'], end['x'])
                x = max(start['x'], end['x'])
                for i in range(m, m+length):
                    rockMatrix[start['y']-1].add(i)
            # last end is the next start
            start = end
    
    sandLanding = dropSand(rockRidges)
    while (sandLanding is not None):
        pileOsand.add(sandLanding)
        debug(printCavern())
        sandLanding = dropSand(rockRidges)
        # debug(f'pileOsand: {pileOsand}')

    print(f'Total sand collected: {len(pileOsand)}')

def part2(file: TextIOWrapper):
    pass


# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel = parseAndLoad()
file = openFile(inputfile)
partsMap = {"1": part1, "2": part2}
runFile(parts, partsMap, file)
