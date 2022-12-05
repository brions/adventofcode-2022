
class Assignment:
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper
    
    def __str__(self):
        return f'Working area: {self.lower}-{self.upper}'
        
    def __repr__(self):
        return f'{self.lower}:{self.upper}'
        
    def contains(self, other: "Assignment"):
        # determine if my lower/upper contains the other's lower/upper range completely (bounds are inclusive)
        if self.lower <= other.lower and self.upper >= other.upper:
            return True
        return False

        

# all the assignments
lines = list(map(lambda line: line.strip(), open('input.txt', 'r')))

supersetPairs = 0

for line in lines:
    assignments = list(list(map(int, x.split('-'))) for x in (line.split(',')))
    objects = [Assignment(assignments[0][0], assignments[0][1]), Assignment(assignments[1][0], assignments[1][1])]
    
    # print(f'assignments: {assignments}')
    # print(f'objects: {objects}')
    
    # consider the largest range - that set becomes the bounds, and check to see the other set is contained within that range
    if objects[0].contains(objects[1]) or objects[1].contains(objects[0]):
        supersetPairs += 1        
        print(f'===> found a superset {objects}')
                    
print(f'number of superset pairs: {supersetPairs}')
