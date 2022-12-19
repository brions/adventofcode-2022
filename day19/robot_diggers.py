from helpers import parseAndLoad, readLines, runLines, debug, getLogLevel, LogLevel
from operator import itemgetter
import re


###
# Objects
#####


###
# Globals
#####
BLUEPRINT_REGEX = r'Blueprint (\d+)'
ROBOT_REGEX = r"(?:Each (\w+) robot costs (\d+) (\w+).(?:and (\d+) (\w+).)?)+"
robotBlueprints = dict()

###
# Main execution
#####

def part1(lines, args):
    # split the line on ':' and grab the blueprint number from the first part
    # then grab the robot type and cost(s) from the second part
    for line in lines:
        blueprint_str, robot_str = line.split(':')
        blueprintNumMatcher = re.match(BLUEPRINT_REGEX, blueprint_str.strip())
        blueprintNum = int(blueprintNumMatcher.group(1))
        robotBlueprints[blueprintNum] = dict()
        robotDefs = re.findall(ROBOT_REGEX, robot_str.strip())
        for robotDef in robotDefs:
            type = robotDef[0]
            costs = list()
            # split the resulting tuple with potentially multiple costs into tuples of 2:
            # cost & material, then only add non-empty costs to the blueprint
            for cost, material in tuple(robotDef[x:x + 2] \
                                  for x in range(1, len(robotDef), 2)):
                if cost and material:
                    costs.append((int(cost), material))
            robotBlueprints[blueprintNum][type] = costs

    if getLogLevel() == LogLevel.DEBUG:
        debug(f'Blueprints:')
        for key, value in robotBlueprints.items():
            debug(f'{key}: {value}')

    for blueprintNum, blueprint in robotBlueprints.items():
        robotPrices = {'ore':[], 'clay':[], 'obsidian':[], 'geode':[]}
        for type, costs in blueprint.items():
            robotPrices[type] = costs
            
        countdown = 24
        materialStore = {'ore':0, 'clay':0, 'obsidian':0, 'geode':0}
        robots = {'ore':1, 'clay':0, 'obsidian':0, 'geode':0}

        while countdown > 0:
            inProgressRobot: str = None
            
            # check to see if we can build a new robot based on the blueprint - most expensive first
            priceTuples = [('geode', robotPrices['geode']), ('obsidian', robotPrices['obsidian']),
                           ('clay', robotPrices['clay']), ('ore', robotPrices['ore'])]
            sortedPrices = sorted(priceTuples, reverse=True, key=lambda v: len(v[1]))
            for rType, costs in sortedPrices:
                haveEnough = True
                for cost in costs:
                    mType = cost[1]
                    amount = cost[0]
                    if materialStore[mType] < amount:
                        haveEnough = False
                        break
                
                if haveEnough:
                    # "build" a new robot and subtract the amount of materials from the store
                    inProgressRobot = rType
                    break
                    
            # each robot collects one of its type and adds it to the store
            for rType, count in robots.items():
                if count > 0:
                    materialStore[rType] += count
                    
            # finish building the robot
            if inProgressRobot:
                robots[inProgressRobot] += 1
                for cost in robotPrices[inProgressRobot]:
                    materialStore[cost[1]] -= cost[0]
                inProgressRobot = None
                
            countdown -= 1
                
        # countdown is over - print out what we've got
        print(f'Total robots: {robots}')
        print(f'Total materials collected: {materialStore}')
        

def part2(lines, args):
    pass

# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel, args = parseAndLoad()
lines = readLines(inputfile)
partsMap = {"1": part1, "2": part2}
runLines(parts, partsMap, lines, args)