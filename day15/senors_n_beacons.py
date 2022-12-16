from helpers import *
from enum import Enum
import re

class MapPoint(Enum):
    SENSOR = 'S'
    BEACON = 'B'
    COVERAGE = '#'
    BLANK = '.'

#####
# constants
#######
COORDINATES_PATTERN = re.compile('^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$')


#####
# globals
#######
sensors = set()
# dictionary of sensor coordinates -> (closest beacon, sensor range)
sensorMap = dict()
beacons = set()
# coverage is a dictionary of: y coord -> set of x coords
coverage = dict()
maxValues = {'x': 0, 'y': 0}
minValues = {'x': 0, 'y': 0}


def distanceTo(point1: Coordinates, point2: Coordinates):
    return abs(point1['x'] - point2['x']) + abs(point1['y'] - point2['y'])


def isCovered(point: Coordinates) -> bool:
    # check to see if it's in range of every sensor, not just closest
    for sensor in sensors:
        if sensorMap[sensor][1] >= distanceTo(point, sensor):
            return True
    # sensorPos, distToSensor = closestTo(point, sensors)
    # if sensorPos and distToSensor:
    #     # get the range of this sensor and see if the point is within range
    #     sensorRange = sensorMap[sensorPos][1]
    #     return sensorRange >= distToSensor
    # else:
    return False

def renderRow(row: int) -> str:
    rendered = list()
    for x in range(minValues['x'], maxValues['x']+1):
        point = Coordinates(x, row)
        if point in sensors:
            rendered.append('S')
        elif point in beacons:
            rendered.append('B')
        elif isCovered(point):
            rendered.append('#')
        else:
            rendered.append('.')
    return "".join(rendered)

def drawMap() -> None:
    for y in range(minValues['y'], maxValues['y']+1):
        rowStr = renderRow(y)
        # for x in range(minValues['x'], maxValues['x']+1):
        #     point = Coordinates(x, y)
        #     if point in sensors:
        #         print('S', end='')
        #     elif point in beacons:
        #         print('B', end='')
        #     elif point in coverage:
        #         print('#', end='')
        #     else:
        #         print('.', end='')
        print(f'{y: ^3} {rowStr}')
        
def updateMinMax(index, newMin, newMax) -> None:
        minValues[index] = newMin if newMin < minValues[index] else minValues[index]
        maxValues[index] = newMax if newMax > maxValues[index] else maxValues[index]


def closestTo(location: Coordinates, domain: set) -> tuple:
    """Determines which of the coordinates in the provide coordinate set
    is closest to the provided location using the Manhattan distance formula

    Args:
        location (Coordinates): starting coordinates
        coordinateSet (set): domain of coordinates to search

    Returns:
        Coordinates: closest coordinate to location from domain
    """
    shortestDistance: tuple = None
    for point in domain:
        if isinstance(point, Coordinates):
            # find the manhattan distance
            distance = distanceTo(location, point)
            if not shortestDistance or distance < shortestDistance[0]:
                shortestDistance = (distance, point)
        else:
            error('domain does not contain only Coordinates')
            return None
            
    return (shortestDistance[1], shortestDistance[0]) or None



    # found = False
    # increment = 1
    ## debugging
    
    # while not found:
    #     # determine the range from sensor using a point {increment} distance away
    #     testPoint = Coordinates(sensor['x'] + increment, sensor['y'] + increment)
    #     # testPointBag.add(testPoint)
    #     testRange = abs(sensor['x'] - testPoint['x']) + abs(sensor['y'] - testPoint['y'])
    #     debug(f'  testing range: {testRange} around {sensor}') if (testRange % 100) == 0 else None
    #     for yoff in range(testRange):
    #         xlim = testRange - yoff
    #         for xoff in range(xlim):
    #             ur = dl = dr = ul = None
    #             ur = Coordinates(sensor['x'] + xoff, sensor['y'] + yoff)
    #             dl = Coordinates(sensor['x'] - xoff, sensor['y'] - yoff)
    #             dr = Coordinates(sensor['x'] + xoff, sensor['y'] - yoff)
    #             ul = Coordinates(sensor['x'] - xoff, sensor['y'] + yoff)
    #             if not ur and not dl and not dr and not ul:
    #                 # nothing left to test in this row
    #                 # debug(f'points checked around {sensor} before leaving: {testPointBag}')
    #                 break
    #             if ur and ur in beacons:
    #                 # debug(f'points checked around {sensor} before finding {ur}: {testPointBag}')
    #                 return Coordinates(ur['x']+1, ur['y'])
    #             if dl and dl in beacons:
    #                 # debug(f'points checked around {sensor} before finding {dl}: {testPointBag}')
    #                 return Coordinates(dl['x']-1, dl['y'])
    #             if dr and dr in beacons:
    #                 # debug(f'points checked around {sensor} before finding {dr}: {testPointBag}')
    #                 return Coordinates(dr['x']+1, dr['y'])
    #             if ul and ul in beacons:
    #                 # debug(f'points checked around {sensor} before finding {ul}: {testPointBag}')
    #                 return Coordinates(ul['x']-1, ul['y'])
    #     increment += 1


def populateDataSets(file) -> None:
    global sensors, beacons, coverage, minValues, maxValues
    
    for line in list(map(lambda l: l.strip(), file.readlines())):
        dataPoints = COORDINATES_PATTERN.match(line).groups()
        x1 = int(dataPoints[0])
        y1 = int(dataPoints[1])
        x2 = int(dataPoints[2])
        y2 = int(dataPoints[3])
        sensors.add(Coordinates(x1, y1))
        beacons.add(Coordinates(x2, y2))
        if not coverage.get(y1):
            coverage[y1] = set()
        coverage[y1].add(x1)
        
        xMin = min([x1, x2])
        yMin = min([y1, y2])
        xMax = max([x1, x2])
        yMax = max([y1, y2])
        updateMinMax('x', xMin, xMax)
        updateMinMax('y', yMin, yMax)        
        
    for sensor in sensors:
        info(f'Finding closest beacon for sensor {sensor}')
        beaconPos, sensorRange = closestTo(sensor, beacons)
        # sensorRange = abs(sensor['x'] - beaconPos['x']) + abs(sensor['y'] - beaconPos['y']) + 1
        info(f'Storing beacon location, sensor range, and updating min/max')
        sensorMap[sensor] = (beaconPos, sensorRange)
        updateMinMax('x', sensor['x'] - sensorRange, sensor['x'] + sensorRange)
        updateMinMax('y', sensor['y'] - sensorRange, sensor['y'] + sensorRange)
        # info(f'updating sensor coverage (range: {sensorRange})')
        # for yoff in range(sensorRange):
        #     xlim = sensorRange - yoff
        #     for xoff in range(xlim):
        #         if not coverage.get(sensor['y'] + yoff):
        #             coverage[sensor['y'] + yoff] = set()
        #         if not coverage.get(sensor['y'] - yoff):
        #             coverage[sensor['y'] - yoff] = set()
        #         coverage[sensor['y'] + yoff].add(sensor['x'] + xoff)
        #         coverage[sensor['y'] - yoff].add(sensor['x'] - xoff)
        #         coverage[sensor['y'] + yoff].add(sensor['x'] - xoff)
        #         coverage[sensor['y'] - yoff].add(sensor['x'] + xoff)


def part1(file, args):
    info("Populating datasets...")
    populateDataSets(file)
    debug("drawing the map...")
    drawMap() if logLevel.DEBUG == getLogLevel() else None
    checkRow = int(args[0]) if args and args[0] else 2000000
    info(f"Calculating available positions for a beacon in row {checkRow}")
    count = len(re.findall('[^\.B]', renderRow(checkRow)))
    print(f'Number of blank spaces in y={checkRow}: {count}')


def 


def part2(file, args):
    info("Populating datasets...")
    populateDataSets(file)
    debug("drawing the map...")
    drawMap() if logLevel.DEBUG == getLogLevel() else None
    checkRow = int(args[0]) if args and args[0] else 2000000
    info(f"Calculating position of distress beacon and its tuning frequency...")
    


# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel, args = parseAndLoad()
file = openFile(inputfile)
partsMap = {"1": part1, "2": part2}
runFile(parts, partsMap, file, args)