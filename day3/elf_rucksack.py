## Today's puzzle is to help identify misplaced items in an elf's rucksack
#
# The basic premise is each line of input includes mixed-case alphabetics, the first half of which represent items in one compartment of the rucksack
# the second half of which represent items in the second compartment of the rucksack.
#
# Each case-sensitive letter is associated with a priority value.  The goal of the first part is to sum the priorities of all the common items in both
# compartments of the rucksack.
#

import fileinput
from string import ascii_letters

# translation map of ascii values for A-Z and a-z
#captialRange = [65,90]
#lowerRange = [97,122]

# load file in here stripping newlines
lines = list(map(lambda line: line.strip(), open('input.txt', mode='r', encoding='utf-8').readlines()))

prioritySum = 0

for line in lines:
    pocketMax = len(line) // 2
    pocketContents = set(line[:pocketMax]), set(line[pocketMax:])
    
    # find the intersection of the pockets
    common = pocketContents[0].intersection(pocketContents[1])
    commonVal = common.pop()

    # print(f'Pocket sets: {pocketContents}')
    # print(f'==> Common priority: {ascii_letters.index(commonVal) + 1} ({commonVal})') if commonVal != None else print(f'### Nothing in common! ###')
    
    prioritySum += ascii_letters.index(commonVal) + 1
    
print(f'====> Total sum of common priorities: {prioritySum}')

groupSum = 0

for idx in range(0, len(lines), 3):
    group = lines[idx:idx+3]
    badgeType = set(group[0]).intersection(group[1]).intersection(group[2])
    
    # print(f'badge type for group {idx//3}: {badgeType}')
    
    groupSum += ascii_letters.index(badgeType.pop()) + 1
    
print(f'====> Total sum of common group priorities: {groupSum}')