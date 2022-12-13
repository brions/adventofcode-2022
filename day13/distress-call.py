from ast import literal_eval
from io import TextIOWrapper
from helpers import info, debug, trace, parseAndLoad, openFile, runfile
from itertools import zip_longest

######
#


#####
# Main logic
###

# this will hold the indices of the ordered packet pairs
orderedPackets = list()

# this will hold all the lines in sorted order
encodedMessage = list()


def coerceToList(num: int) -> list:
    return [num]


def compareLists(left: list, right: list) -> int:
    """Compares two lists by their length and content. Each item of the left
    will be compared to the complementary item in right. The result of this
    function will be negative if the first list (left) is shorter or its
    element results in a negative comparison with the right element.

    Args:
        left (list): 'left' side list
        right (list): 'right' side list

    Returns:
        int: negative if left is shorter, 0 if lists are equal in length and
        content, positive if right is shorter
    """
    returnValue = None

    itemCount = min(len(left), len(right))
    trace(f'smallest list is length: {itemCount}')

    for idx in range(itemCount):
        if returnValue is not None and returnValue != 0:
            break
        if isinstance(left[idx], list) and isinstance(right[idx], list):
            returnValue = compareLists(left[idx], right[idx])
        elif isinstance(left[idx], list):
            returnValue = compareLists(left[idx], coerceToList(right[idx]))
        elif isinstance(right[idx], list):
            returnValue = compareLists(coerceToList(left[idx]), right[idx])
        else:
            # both are integers
            returnValue = compareValues(left[idx], right[idx])

    if returnValue == 0 or returnValue is None:
        # check the list lengths are the same, if not return the right value
        returnValue = compareValues(len(left), len(right))

    return returnValue


def compareValues(v1: int, v2: int) -> int:
    """Compares two integers. Returns negative if v1 is smaller than v2, 0 if
    they are equal, and positive of v1 is larger than v2.

    Args:
        v1 (int): 'left' side integer
        v2 (int): 'right' side integer

    Returns:
        int: negative if v1 is smaller than v2, 0 if they are equal, and 
        positive of v1 is larger than v2.
    """
    return v1 - v2


def parseLine(line: str, currentList: None) -> list:
    """Parse the provided line and add digits or resolved lists to the current list. Return the
    completed list.

    Args:
        line (str): the line to parse
        currentList (list): the list currently being added to

    Returns:
        list: the list of parsed items
        line: current state of parsing
    """
    pLine = line
    done = False
    while not done:
        idx = 0
        if idx >= len(pLine):
            done = True
            break

        while pLine:
            char = pLine[0]
            if char == '[':
                # recurse with a new list and reset the line
                nextIdx = idx + 1
                newList, pLine = parseLine(pLine[nextIdx:], list())
                if not currentList:
                    currentList = list()
                currentList.append(newList)
                break
            elif char == ']':
                # short ciruit here and return the line with one fewer characters
                return currentList, pLine[idx + 1:]
            elif char.isdigit():
                foundEnd = False
                howMany = 1
                next = pLine[howMany:howMany+1]
                while not foundEnd:
                    if next.isdigit():
                        howMany += 1
                        next = pLine[howMany:howMany+1]
                    else:
                        foundEnd = True
                digit = int(pLine[:howMany]) if howMany > 1 else int(char)
                currentList.append(digit)
                # move the index as far as we read
                if howMany > 1:
                    idx += howMany - 1
            # lose any other characters and continue
            pLine = pLine[idx+1:]
            idx = 0

    # done parsing the line, return the list and an empty line
    return currentList, pLine


def part1(file: TextIOWrapper):
    info("part1")
    index = 1
    for packet in zip_longest(*[file]*2):
        debug(f'packet: {packet}')
        result = compareLists(literal_eval(packet[0].rstrip()),
                              literal_eval(packet[1]))
        if result < 0 or result == 0:
            info('in order')
            orderedPackets.append(index)
        else:
            info('not in order')

        index += 1

        # read one more line to consume the blank line
        file.readline()

    debug(f'ordered indices: {orderedPackets}')
    print(f'Sum of ordered indices: {sum(orderedPackets)}')


def insertSort(newList, oldList):
    index = 0
    resolved = False
    for sortedList in encodedMessage:
        trace(f'sortedList: {sortedList}')
        trace(f'line: {newList}')
        result = compareLists(newList, sortedList)
        if result < 0:
            # out of order, insert before sortedLine
            encodedMessage.insert(index, newList)
            resolved = True
            break
        elif result > 0:
            if len(encodedMessage) > index + 1:
                # in order but not equal - check against the next one
                index += 1
                continue
            else:
                # add this at the end
                encodedMessage.append(newList)
                resolved = True
                break
        else:
            # in order and equal, insert after sortedLine
            encodedMessage.insert(index + 1, newList)
            resolved = True
            break
    if not resolved:
        encodedMessage.append(newList)


def part2(file: TextIOWrapper):
    info("part2")

    # add the first line to the final message so we have something to sort 
    # against
    encodedMessage.append(parseLine(file.readline().strip(), list())[0][0])

    for line in file:
        line = line.strip()
        debug(f'handling line: "{line.strip()}"')
        if line:
            trace(f'literal line: "{line}"')
            parsedList = parseLine(line, list())[0][0] if isinstance(line, str) else line
            insertSort(parsedList, encodedMessage)

    insertSort([[2]], encodedMessage)
    insertSort([[6]], encodedMessage)
    debugString = "\n".join(map(str, encodedMessage))
    debug(f'sorted lines: {debugString}')
    
    # search the encoded message for the divider packets [[2]] and [[6]], and
    # and record the indices
    divider2: int = -1
    divider6: int = -1
    index = 1
    for item in encodedMessage:
        if compareLists(item, [[2]]) == 0:
            divider2 = index
        elif compareLists(item, [[6]]) == 0:
            divider6 = index
        index += 1

    debug(f'divider2: {divider2}')
    debug(f'divider6: {divider6}')
    decoderKeyIndex = divider2 * divider6
    print(f'Decoder key found at: {decoderKeyIndex}')


# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel = parseAndLoad()
file = openFile(inputfile)
partsMap = {"1": part1, "2": part2}
runfile(parts, partsMap, file)
