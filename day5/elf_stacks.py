## Today's challenge is to rearrange crates in stacks per the sequence identified as `move X from A to B`.
# The input takes the form of three parts:
# part 1 - `[C]`  stack elements (crates)
# part 2 - `1 2 3` stack identifiers (columns/stacks)
# part 3 - `move 1 from 2 to 1` move instructions (final move result desired, not intermediary moves)
# 
# parts 2 and 3 are separated by a blank line
# parts 1 and 2 are distinct in that part 2 does not have `[` `]` at all
#
# To load this input we'll do the following:
# 1. read each line and determine:
#   a. if it contains [], parse the line chunking it into fields of size 4 (each column is 4 chars wide - e.g. `[A] `) and add them to a stack keyed by the
#      field position in a map.  So if the first column was `[A] ` and the second was `[B] `, then the map would contain: `{0: ['A'], 1: ['B']`
#   b. if it contains only numbers - skip it because we already know how many columns we have by how many keys we added to the map
#   c. if it's a blank line stop line-by-line processing and load the rest of the file as instructions
# 2. for each stack in the map (all the values of the map) reverse the queue order (so `['A', 'Z']`` becomes `['Z', 'A']`QNNTGTPFN)
# 
# This will result in a single map, keyed by crate stack column, with one stack per key of the data in the correct order (first read from input = bottom of stack)
#
# Next we'll run through the instructions parsing `move X from A to B` as `howMany` to pop/push from stack key `A` to stack key `B`
# When all the instructions are executed, peeking (or popping) the top of each stack for every key in the map (in order) will result in the "word"
##

from collections import deque
import re

# create a map of stacks
mapOfStacks = {}

# open the file for reading, but only read one line at a time until we get to the start of the instruction data
fh = open('input.txt', 'r')

line = fh.readline().strip('\n')

# each column in the first section is 4 characters long - either spaces or data
cols = None

# print(f'line: {line}')

while re.match(r'.*\[.*', line):
    cols = [line[x+1:x+2] for x in range(0, len(line), 4)]
    # print(f'cols: {cols}')
    for x in range(0, len(cols)):
        if (cols[x].strip()):
            # get the current stack for the column
            stack = mapOfStacks.get(x)
            if not stack:
                stack = deque()
                mapOfStacks[x] = stack
            mapOfStacks[x].append(cols[x])
    line = fh.readline()
    # print(f'line: {line}')
    
# print(f'mapOfStacks: {mapOfStacks}')

# now that we've read everything, we need to reverse the order of the stacks (LIFO) because we read them in reverse order (FILO)
for stack in mapOfStacks.values():
    stack.reverse()
    
# print(f'mapOfStacks (reversed): {mapOfStacks}')

# the current line is the number of columns, but since we know that, read one more line before we start looping through the instructions
line = fh.readline()

# move howMany crates, one at a time using pop/append from src stack to dest stack
def moveCrates(howMany: int, src: int, dest: int):
    for i in range(howMany):
        mapOfStacks[dest].append(mapOfStacks[src].pop())
        # print(f'mapOfStacks: {mapOfStacks}')

# start looping through the instructions and modifying the stacks as instructed
for line in map(lambda l: l.strip(), fh.readlines()):
    # print(f'instruction: {line}')
    instructions = re.search(r"move (\d+) from (\d+) to (\d+)", line)
    if len(instructions.groups()) == 3:
        moveCrates(int(instructions.group(1)), int(instructions.group(2))-1, int(instructions.group(3))-1)
    
# print(f'mapOfStacks: {mapOfStacks}')

# read the top of every stack
word = ''
keys = list(mapOfStacks.keys())
keys.sort()
# print(f'mapOfStacks.keys(): {keys}')
for k in keys:
    word = word + mapOfStacks[k][-1]
    
print(f'word: {word}')