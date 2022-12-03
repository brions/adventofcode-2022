## Today's puzzle is to help identify misplaced items in an elf's rucksack
#
# The basic premise is each line of input includes mixed-case alphabetics, the first half of which represent items in one compartment of the rucksack
# the second half of which represent items in the second compartment of the rucksack.
#
# Each case-sensitive letter is associated with a priority value.  The goal of the first part is to sum the priorities of all the common items in both
# compartments of the rucksack.
#

import fileinput

# translation map of ascii values for A-Z and a-z
#captialRange = [65,90]
#lowerRange = [97,122]

def parseRucksack(items: str):
    prioritySets = [set() for s in range(2)]
    # print(f'prioritySets: {prioritySets}')
    pocketMax = (len(items) / 2) - 1
    pos = 0

    for char in items:
        if ord(char) >= 97 and ord(char) <= 122:
            # we have a lowercase letter, subtract 96 to get the priority
            # print(f'found lowercase letter {char} ({ord(char)})')
            # convert it to its priority and sort it into the correct pocket
            priorityValue = ord(char) - 96
            # print(f'adding priority of {char} ({priorityValue}) to pocket {0 if pos < pocketMax else 1}')
            prioritySets[0].add(priorityValue) if pos < pocketMax else prioritySets[1].add(priorityValue)
        elif ord(char) >= 65 and ord(char) <= 90:
            # we have a lowercase letter, subtract 96 to get the priority
            # print(f'found uppercase letter {char} ({ord(char)})')
            # convert it to its priority and sort it into the correct pocket
            priorityValue = ord(char) - 38
            # print(f'adding priority of {char} ({priorityValue}) to pocket {0 if pos < pocketMax else 1}')
            prioritySets[0].add(priorityValue) if pos < pocketMax else prioritySets[1].add(priorityValue)
        pos += 1
    return prioritySets

prioritySum = 0

# load file in here
for line in fileinput.input('input.txt'):
    if not line.strip():
        continue
    
    prioritySets = parseRucksack(line)

    # print(f'contents of pocket 1: {prioritySets[0]}\ncontents of pocket 2: {prioritySets[1]}')
    # print(f'sum of pocket 1: {sum(prioritySets[0])}\nsum of pocket 2: {sum(prioritySets[1])}')

    # find the intersection of the prioritySets
    common = prioritySets[0].intersection(prioritySets[1])

    print(f'Common set: {common}') if len(common) > 0 else print(f'### Nothing in common! ###')
    
    # add common to the sum unless there's nothing in common
    prioritySum += sum(common) if len(common) > 0 else 0
    
print(f'Total sum of common priorities: {prioritySum}')