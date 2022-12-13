input = "[[[], 3, 1, [[4], 3, 0, [2, 2]]], [[[0, 3, 4]], [0, 2, [4, 10, 1, 5]]], [], [6, [], 9]]"

print(f'input: {input}')
# lst = input.strip('][').split(',')


def parseLine(line: str, startingList: list = None) -> list:
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
    currentList = startingList
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
                if currentList is not None:
                    currentList.append(newList)
                else:
                    currentList = newList
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
    
    # done parsing the line, return an empty line
    return currentList, pLine

# def convert(string: str) -> list:
#     converted = string.strip('][').split(',')
#     return resolveList(converted)


# def coerce(string: str):
#     if string == '':
#         return []
#     elif string.startswith('['):
#         return resolveList(convert(string))
#     else:
#         return int(string)


# def resolveList(lst: list) -> list:
#     rList = list()
#     item: str
#     for item in lst:
#         item = item.strip()
#         newitem = None
#         if isinstance(item, str) and item.startswith('['):
#             newitem = convert(item)
#         elif isinstance(item, str):
#             newitem = str(item)
#         else:
#             newitem = item
#         rList.append(newitem) if isinstance(newitem, list) else \
#             rList.append(coerce(newitem))
#     return rList


finalList, line = parseLine(input)
# for item in lst:
#     item = item.strip()
#     newitem: lst
#     if item.startswith('['):
#         newitem = convert(item)
#     else:
#         newitem = item
#     finalList.append(newitem) if isinstance(newitem, list) else \
#         finalList.append(coerce(newitem))

print(f'finalList: {finalList}')