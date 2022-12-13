## Day 11
#

##################
# Definitions Start Here
########################

####
# globals
#########
debug = False

##################
# Logic Start Here
########################

## Part 1
def part1(lines: list) -> None:
    pass

## Part 2
def part2(lines: list) -> None:
    pass

#### main execution area ####
from AdventOfCode import helper

partsMap = {'1': part1, '2': part2}

executeParts, inputFile, logLevel = helper.parseAndLoad()

executeParts = []
inputFile = 'input.txt'

for opt, value in opts:
    if opt == '-p' or opt == '--part':
        executeParts.append(value)
    elif opt == 'f' or opt == '--file':
        inputFile = value
    elif opt == 'd' or opt == '--debug':
        debug = True
        
if not executeParts:
    executeParts.append('1')
        
# read input to get set of hypothetical moves
fh = open(inputFile, 'r')
lines = list(map(lambda l: l.rstrip(), fh.readlines()))

for part in executeParts:
    if part in availableParts:
        availableParts[part](lines)
