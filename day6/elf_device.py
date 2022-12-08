## Day 6 - The broken device fixer-upper routine
# You've been given a broken Elven device and you need to find the first 4-character
# sequence that has no repeated characters in the input stream, and report that final position.
#
# For example:
# input of - bhskeugh
# the output should be 4 becuase the fourth character ends the first occurence of a
# unique sequence of characters.  Note: this is 1-based, not 0-based
##

from collections import deque

fh = open('input.txt', 'r')

lines = list(map(lambda l: l.strip(), fh.readlines()))

sopFound = False
somFound = False

# part 1
for line in lines:
    # keep only the last 4 character read
    codeBuffer = deque(maxlen=4)

    for char in line[0:4]:
        codeBuffer.append(char)
    pos = 4

    def isSOPUnique(buffer: deque):
        test = set(buffer)
        return len(test) == len(buffer)

    while not isSOPUnique(codeBuffer):
        pos += 1
        codeBuffer.append(line[pos-1])

    # print(f'codeBuffer is: {codeBuffer}')    
    print(f'Determined start-of-packet to be at position: {pos}')

# part 2
for line in lines:
    messageBuffer = deque(maxlen=14)

    for char in line[0:14]:
        messageBuffer.append(char)
    messagePos = 14

    def isSOMUnique(buffer: deque):
        test = set(buffer)
        return len(test) == len(buffer)

    while not isSOMUnique(messageBuffer):
        messagePos += 1
        messageBuffer.append(line[messagePos-1])

    # print(f'messageBuffer is: {messageBuffer}')    
    print(f'Determined start-of-message to be at position: {messagePos}')
