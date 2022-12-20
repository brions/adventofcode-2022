from helpers import parseAndLoad, readLines, runLines, debug, getLogLevel, LogLevel
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

def getPrices(blueprintNum: int) -> dict:
    blueprint = robotBlueprints[blueprintNum]
    robotPrices = {'ore':[], 'clay':[], 'obsidian':[], 'geode':[]}
    for type, costs in blueprint.items():
        robotPrices[type] = costs
    return robotPrices


def selectRobotBuild(blueprintNum: int, materialStore: dict) -> str:
    """Select the next robot to build, or None if none can be built.
    """
    # the robot selection goes like this:
    # 1. if you have the materials to build a "geode", return "geode", else
    # 2. if you have the materials to build an "obsidian", return "obsidian", else
    # 3. if you have the materials to build a "clay", return "clay", else
    # 4. if you have the materials to build an "ore", return "ore", else
    # 5. return None
    robotPrices = getPrices(blueprintNum)
    blueprint = robotBlueprints[blueprintNum]
    
    geodeDef = blueprint['geode']
    canBuild = True
    for materialTuple in geodeDef:
        # check to see if we have enough of the materials for a "geode"
        if not canBuild:
            break
        if materialTuple == ('',''):
            continue
        for cost in robotPrices['geode']:
            if cost[0] > materialStore[materialTuple[1]]:
                canBuild = False
                break
    
    if canBuild:
        return 'geode'    

    obsidianDef = blueprint['obsidian']
    canBuild = True
    for materialTuple in obsidianDef:
        if not canBuild:
            break
        # check to see if we have enough of the materials for an "obsidian"
        if materialTuple == ('',''):
            continue
        for cost in robotPrices['obsidian']:
            if cost[0] > materialStore[materialTuple[1]]:
                canBuild = False
                break
    
    if canBuild:
        return 'obsidian'    

    clayDef = blueprint['clay']
    canBuild = True
    for materialTuple in clayDef:
        if not canBuild:
            break
        # check to see if we have enough of the materials for an "clay"
        if materialTuple == ('',''):
            continue
        for cost in robotPrices['clay']:
            if cost[0] > materialStore[materialTuple[1]]:
                canBuild = False
                break
    
    if canBuild:
        return 'clay'    

    oreDef = blueprint['ore']
    canBuild = True
    for materialTuple in oreDef:
        if not canBuild:
            break
        # check to see if we have enough of the materials for an "ore"
        if materialTuple == ('',''):
            continue
        for cost in robotPrices['ore']:
            if cost[0] > materialStore[materialTuple[1]]:
                canBuild = False
                break
    
    if canBuild:
        return 'ore'    


def printAssets(robots, materialStore):
    for type, count in robots.items():
        if count < 1:
            continue
        print(f'{count} {type}-mining robot collects {count} {type}; you now have {materialStore[type]} {type}.')


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
        countdown = 24
        materialStore = {'ore':0, 'clay':0, 'obsidian':0, 'geode':0}
        robots = {'ore':1, 'clay':0, 'obsidian':0, 'geode':0}
        robotPrices = getPrices(blueprintNum)
        
        while countdown > 0:
            if debug:
                print(f'== Minute {25-countdown} ==')
            inProgressRobot: str = None
            
            # check to see if we can build a new robot based on the blueprint - most expensive first
            robotType = selectRobotBuild(blueprintNum, materialStore)
            inProgressRobot = robotType
            if inProgressRobot:
                spent = dict()
                for cost in robotPrices[inProgressRobot]:
                    materialStore[cost[1]] -= cost[0]
                    spent[cost[1]] = cost[0]
                spendStr = ''
                for spend in spent.items():
                    if spendStr:
                        " and ".join(spendStr)
                    spendStr = f'{spend[1]} {spend[0]}'                    
                if debug:
                    print(f'Spend {spendStr} to start building a {inProgressRobot}-collecting robot.')

            # priceTuples = [('geode', robotPrices['geode']), ('obsidian', robotPrices['obsidian']),
            #                ('clay', robotPrices['clay']), ('ore', robotPrices['ore'])]
            # sortedPrices = sorted(priceTuples, reverse=True, key=lambda v: len(v[1]))
            # for rType, costs in sortedPrices:
            #     haveEnough = True
            #     for cost in costs:
            #         mType = cost[1]
            #         amount = cost[0]
            #         if materialStore[mType] < amount:
            #             haveEnough = False
            #             break
                
            #     if haveEnough:
            #         # "build" a new robot and subtract the amount of materials from the store
            #         inProgressRobot = rType
            #         break
                    
            # each robot collects one of its type and adds it to the store
            for rType, count in robots.items():
                if count > 0:
                    materialStore[rType] += count
                    
            if getLogLevel() == LogLevel.DEBUG:
                printAssets(robots, materialStore)                

            # finish building the robot
            if inProgressRobot:
                robots[inProgressRobot] += 1
                if debug:
                    print(f'The new {inProgressRobot}-collecting robot is ready; you now have {robots[inProgressRobot]} of them.')
                inProgressRobot = None

            if debug:
                print('')
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