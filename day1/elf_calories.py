# given a blank-line separated list of calorie counts per elf,
# sum each amount per line for each item in the list and store it
# associated with the elf's position in the list

import fileinput

# Calculate the sum of the list of input numbers
def sum_of_nums(num_list):
    result = 0
    for num in num_list:
        result += num
    return result

elf_calories_map = {}

# load the input file into the elf_calories_map
num_list = []
idx = 0
for line in fileinput.input(files=('input.txt')):
    if line.strip().isnumeric():
        num_list.append(int(line.strip()))
    elif line.strip() == '' :
        #print(f'Found blank line - adding {len(num_list)} items together and setting them as elf {idx}')
        elf_calories_map[idx] = sum_of_nums(num_list)
        idx += 1
        num_list = []
else:
    elf_calories_map[idx] = sum_of_nums(num_list)

# determine the elf with the most calories by finding the largest value
biggest_elf_value = 0
biggest_elf_pos = -1
for (elf, value) in elf_calories_map.items():
    if (value > biggest_elf_value):
        biggest_elf_pos = elf
        biggest_elf_value = value

# print out the biggest elf position and value
print(f'Elf {biggest_elf_pos} has {biggest_elf_value} calories')

## part 2 - find the top 3 elves and print out the sum of their calories
# Note: this is a bit redundant, but it's just for fun so...

# determine the top three elves with the most calories by adding each elf/value
# to a fixed list of size 3 keeping only the 3 highest values; if a new value
# exceeds any of the existing values, then drop the lowest and add the new value

# this is a sorted array of the top three values
top_three_elfs = []
# this is a map of elf pos => value of the top_three_elfs
top_three_map = {}
# reverse look-up map of value => elf pos
value_elf_map = {}

print(f'Top three values: {top_three_elfs}')
print(f'Top three elves: {top_three_map}')

for (elf, value) in elf_calories_map.items():
    # keep the top 3 sorted for more accurate ranking
    top_three_elfs.sort(reverse=True)
    
#    print(f'elf: {elf}:{value}')
#    print(f'top_three_elfs: {top_three_elfs}')
    # special case - < 3 values, just add the first 3 values
    if len(top_three_elfs) < 3:
        print(f'top_three_elfs has < 3 entries: {top_three_elfs}, adding one')
        top_three_elfs.append(value)
        top_three_map[elf] = value
        value_elf_map[value] = elf
        if (len(top_three_elfs) == 3):
            print(f'Top 3 elves at the start: {top_three_map}')
        continue

    for top_value in top_three_elfs:
        if value > top_value:
            print(f'found a new top_value: {top_value} (elf #{elf})')
            top_three_elfs.insert(0,value)          # insert ahead of the old value
            dropped_value = top_three_elfs[3]       # save the value about to be dropped
            top_three_elfs = top_three_elfs[0:3]    # trim the list to 3
            top_three_map[elf] = value              # add the elf to the map
            value_elf_map[value] = elf
            del top_three_map[value_elf_map[dropped_value]] # remove the dropped elf
            del value_elf_map[dropped_value]
#            print(f'top_three_map: {top_three_map}')
            break

print(f'Top 3 elves are: {top_three_map}')
print(f'Total of top 3 elves is: {sum_of_nums(top_three_elfs)}')
