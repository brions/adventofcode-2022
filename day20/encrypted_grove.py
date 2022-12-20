from helpers import parseAndLoad, readLines, runLines, debug, getLogLevel, LogLevel

###
# Objects
#####


###
# Globals
#####



###
# Main execution
#####


def part1(lines, args):
    sequence = [int(x) for x in lines]
    workingCopy = list(sequence)
    
    sequenceLength = len(sequence)
    for idx in range(sequenceLength):
        #debug(f'start of loop: {workingCopy}')
        workingCopyOldIdx = workingCopy.index(sequence[idx])
        debug(f'moving orig. index {idx} ({sequence[idx]}) from working copy idx {workingCopyOldIdx}')
        nextIdx = workingCopyOldIdx + sequence[idx]
        debug(f'new index for value in working copy: {nextIdx}')
        if nextIdx > sequenceLength - 1:
            overlap = nextIdx % sequenceLength + 1
            nextIdx = overlap
        elif nextIdx <= 0:
            wrappedIdx = nextIdx % sequenceLength - 1
            nextIdx = wrappedIdx
        debug(f'new index for value in working copy (adjusted): {nextIdx}')
        value = sequence[idx]
        popped = workingCopy.pop(workingCopyOldIdx)
        # debug(f'(popped: {popped}), workingCopy: {workingCopy}')
        debug(f'(popped: {popped})')
        workingCopy.insert(nextIdx, value)
        #debug(f'end of loop: {workingCopy}')
        
    # find the index of value 0, and "loop" to the 1000th, 2000th, and 3000th "index"
    zeroIdx = workingCopy.index(0)
    i1 = (zeroIdx + 1000) % sequenceLength
    i2 = (zeroIdx + 2000) % sequenceLength
    i3 = (zeroIdx + 3000) % sequenceLength
    v1 = workingCopy[i1]
    v2 = workingCopy[i2]
    v3 = workingCopy[i3]
    
    print(f'Found values: v1={v1}, v2={v2}, v3={v3}; sum = {v1 + v2 + v3}')

def part2(lines, args):
    pass


# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel, args = parseAndLoad()
lines = readLines(inputfile)
partsMap = {"1": part1, "2": part2}
runLines(parts, partsMap, lines, args)