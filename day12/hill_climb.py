from adventofcode.adventofcode import helpers

lines: list


def part1():
    print("part1")


def part2():
    print("part2")


# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel = helpers.parseAndLoad()
lines = helpers.readLines(inputfile)
partsMap = {"1": part1, "2": part2}
helpers.run(parts, partsMap, lines)
