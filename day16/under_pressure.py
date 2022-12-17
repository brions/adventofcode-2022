from helpers import *
from io import TextIOWrapper
import re
from queue import Queue
from collections import defaultdict

###
# Classes
####

class Valve:
    def __init__(self, name: str, rate: int, connections: set) -> None:
        self.name: str = name
        self.rate: int = rate
        self.connections: set = set()
        self.connections.update(connections)
        self.opened: bool = False

    def __eq__(self, __o: "Valve") -> bool:
        if not __o:
            return False
        return self.name == __o.name and self.rate == __o.rate and \
            self.connections == __o.connections and self.opened == __o.opened

    def __hash__(self) -> int:
        return (self.name, self.rate, self.opened).__hash__()

    def __str__(self) -> str:
        return f'({self.name}, {self.rate}, [{self.connections}])'    

    def __repr__(self) -> str:
        return self.__str__()

    def open(self) -> None:
        self.opened = True

class Graph:
    def __init__(self) -> None:
        self.graph = defaultdict(list)
        
    def addEdge(self, u: Valve, v: Valve, cost: int) -> None:
        self.graph[u].append[(cost, v)]
        
    def find(self, target: Valve, source: Valve) -> list
        """Starting from `source`, search the graph for `target` and return
        the path taken as a list of valves

        Returns:
            list: list of valves traversed from source -> target
        """
        visitedValves = [False for x in (max(self.graph) + 1)]
        searchQueue = []
        searchQueue.append(source)
        visitedValves[source] = True
        
        # build the result
        result = list()
        
        while searchQueue:
            nextValve: Valve
            nextValve = searchQueue.pop(0)
            
            for tuple in self.graph[nextValve]:
                child: Valve
                child = tuple[1]
                cost = tuple[0]
                if child == target:
                    # we reached the end, add the child to the list and return it
                    result.append(child)
                if not visitedValves[nextValve]:
                    if result.get(depth) is None:
                        result[depth] = list()
                
            
            if nextValve.connections:
                for valveName in nextValve.connections:
                    tmpValve = nameMap.get(valveName)
                    if tmpValve and tmpValve not in visitedValves:
                        # add this valve to the queue
                        searchQueue.put(tmpValve)
        

###
# Globals
#####
VALVE_PATTERN = re.compile(r'Valve ([A-Z]+).*?rate=(\d+).*?valves? (.*)$')
# valves we've already calculated and accumulated the cost of
visitedValves = set()
# valves we've discovered during traversal that are not yet visited
possibleValves = set()
# map of names -> valves
nameMap = dict()
totalPressureReleased: int

###
# Functions
#####


def calculatePressureReleaseForSeq(openSequence: list, graphRoot: Valve) -> int:
    """Calculate how much pressure is released in total while traversing the path.

    Returns:
        int: amount of pressure in 'flow rate'
    """
    total = 0
    valve: Valve
    time = 30
    # total time is 30s, but each move takes 1s and turning on a valve
    # takes 1s. The opened valve doesn't start releasing pressure until the 1s
    # after it's turned on.
    # the openSequence is the order of valves that are opened
    # the graphRoot is the starting point of the entire graph
    pps = 0
    lastMove = None
    lastOpenedValve = None
    nextNameIdx = 0
    for idx in range(0, time):
        if lastMove is None:
            # make the next move
            valve = nameMap.get(path[nextNameIdx])
        elif lastMove and lastOpenedValve is None:
            # 
        if valve.opened:
            total += valve.rate * time
        time -= 2
        if time == 0:
            break
    return total


def calculateGraph(start: Valve) -> list:
    """Using a BFS, calculates the total most cost-effective path from 'start' to 
    'dest' and return a list of path valve names.
    
    Returns:
        list of lists - first list is depth, additional lists are valves at that tree depth
    """
                
        

def getPathCosts(currentValve: Valve, connections: list) -> dict:
    resultDict = dict()
    for connection in connections:
        resultDict


def findDistance(fromValve: Valve, toValve: Valve) -> int:
    foundDistance = 0
    # find the distance from the current valve to the next valve from among its connections
    for valve in list(map(lambda next: nameMap.get(next), fromValve.connections)):
        if valve == toValve:
            # found it!
            foundDistance += 1
            break
        # recursively dig down
        

def nextValve(currentValve: Valve) -> list:
    """Main logic to return the path to the next most valuable, unopened Valve from the
    current Valve.

    Returns:
        Node: the path of names to the next most valuable valve
    """
    bestCandidate: Valve = None
    
    # get the Valves associated with the connections of this valve
    candidates = list(filter(lambda valve: valve.name in currentValve.connections,
                             nameMap.values()))
    
    # capture the cost to move from currentValue to candidate
    valvePathCosts = dict()
    candidate: Valve
    for candidate in candidates:
        if candidate not in visitedValves:
            valvePathCosts[candidate] = findSteps(candidate)


    debug(f'pathCosts: {valvePathCosts}')

    bestPath = list()
    return bestPath


def loadData(file: TextIOWrapper) -> None:
    """Read data from file and populate valve structures
    """
    global valveFlow
    
    for line in list(map(lambda l: l.strip(), file.readlines())):
        # datapoints will be name, flow rate, connections (comma-separated)
        dataPoints = VALVE_PATTERN.match(line).groups()
        connections = dataPoints[2].split(',') if dataPoints and dataPoints[2] else None
        connections = list(map(lambda item: item.strip(), connections))
        newValve = Valve(dataPoints[0], int(dataPoints[1]), connections)
        nameMap[newValve.name] = newValve


###
# Main execution
#####


def part1(file, args):
    global totalPressureReleased
    
    loadData(file)
    
    # build map of shortest path sequences
    calculatePaths()
    
    # start the countdown
    # start at 'AA'
    currentPos: Valve = nameMap.get('AA')
    pathToNext = nextValve(currentPos)
    for min in range(30):
        # take a step if our path isn't empty
        if pathToNext:
            # remove the first name from the list and move to that valve
            currentPos = nameMap.get(pathToNext.pop(0))
        elif currentPos and not currentPos.opened:
            currentPos.open()
            visitedValves.add(currentPos)
            pathToNext = nextValve(currentPos)

        # we're done - no more paths, no more unopened valves
        totalPressureReleased += calculatePressureReleaseMin()
    print(f'Time\'s up! Total pressure released: {totalPressureReleased}')
        


def part2(file, args):
    pass


# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel, args = parseAndLoad()
file = openFile(inputfile)
partsMap = {"1": part1, "2": part2}
runFile(parts, partsMap, file, args)