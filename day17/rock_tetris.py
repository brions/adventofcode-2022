from helpers import *
from enum import Enum

class ShapeDef(Enum):
    """Known shapes

    Args:
        Enum (SHAPE_TYPE): a tuple of (width, height)
    """
    H_LINE = (4,1)
    V_LINE = (1,4)
    CROSS  = (3,3)
    J_LINE = (3,3)
    SQUARE = (2,2)
    FLOOR  = (7,0)  ## special case


###
# Objects
#####

class Shape:
    def __init__(self, shape: ShapeDef, tl_coordinate: Coordinates) -> None:
        if shape == ShapeDef.FLOOR:
            raise ValueError('FLOOR is a disallowed Shape')
        self.height = shape.value[1]
        self.width = shape.value[0]
        self.shape = shape
        self.tl_coords = tl_coordinate
        self.moveable = True
    
    def __eq__(self, __o: "Shape") -> bool:
        return self.shape == __o.shape and self.tl_coords == __o.tl_coords
    
    def __getitem__(self, item) -> int:
        if item == 0 or item == 'x':
            value = self.tl_coords[0]
        elif item == 1 or item == 'y':
            value = self.tl_coords[1]
        else:
            raise IndexError(f'{item} is not a tl_coordinate index')
        return value
        
    def intersects(self, shape_coord: Coordinates, shape: ShapeDef) -> bool:
        overlaps = False
        ## special cases: cross, j-line, and floor
        if shape == ShapeDef.CROSS:
            # detect collisions with anything other than corners
            if shape.shape == ShapeDef.CROSS:
                # tricky - check coordinates
                if shape_coord['y'] == self.tl_coords['y'] + 1 and \
                   shape_coord['x'] == self.tl_coords['x']:
                       pass
            pass
        elif shape == ShapeDef.J_LINE:
            # detect collisions with tl square
            pass
        elif shape == ShapeDef.FLOOR:
            # detect collision with the floor
            if self.tl_coords['y'] - self.height < shape_coord['y']:
                # we hit floor
                overlaps = True
        else:
            # detect if shape overlaps anywhere on this shape
            if shape == ShapeDef.H_LINE:
                for y in range(self.tl_coords['y'] - self.height, self.tl_coords['y']):
                    if shape_coord['y'] == y:
                        overlaps = True
                        break
            elif shape == ShapeDef.V_LINE:
                for x in range(self.tl_coords['x'], self.tl_coords['x'] + self.width):
                    if shape_coord['x'] + shape.value[0] > x:
                        # we hit the right wall
                        overlaps = True
                        break
                    elif shape_coord['x'] < x:
                        # we hit the left wall
                        overlaps = True
                        break
        return overlaps
    
    def move(self, direction: Direction) -> None:
        if direction == Direction.DOWN:
            self.tl_coords['y'] = self.tl_coords['y'] - 1
        elif direction == Direction.UP:
            self.tl_coords['y'] = self.tl_coords['y'] + 1
        elif direction == Direction.LEFT:
            self.tl_coords['x'] = self.tl_coords['x'] - 1
        elif direction == Direction.RIGHT:
            self.tl_coords['x'] = self.tl_coords['x'] + 1
        else:
            error(f'Invalid direction to move ({direction})')
    
    def land(self) -> None:
        self.moveable = False
    
    


###
# Globals
#####
floorHeight = 0
stackHeight = floorHeight
landedRocks = list()
SHAPE_DROP_SEQ = [ShapeDef.H_LINE, ShapeDef.CROSS, ShapeDef.J_LINE,
                  ShapeDef.V_LINE, ShapeDef.SQUARE]

###
# Main execution
#####





def part1(lines: list, args: list):
    global stackHeight, floorHeight, landedRocks, SHAPE_DROP_SEQ
    
    movesLine = lines.pop()
    movesLineIdx = 0
    maxRockCount = int(args[0]) if args else 2022
    while len(landedRocks) < maxRockCount:
        activeRockShape = SHAPE_DROP_SEQ[len(landedRocks) % len(SHAPE_DROP_SEQ)]
        nextRock: Shape
        for char in movesLine[movesLineIdx:]:
            movesLineIdx += 1      
            moveDir = Direction.LEFT if char == '<' else Direction.RIGHT
            # step one: place rock +2 from left, and +3 from stack/floor height 
            # + rock.height (floor height is 0 @ (0,-1))
            nextRock = Shape(activeRockShape, Coordinates(2, stackHeight + 2 + 
                                                          activeRockShape.value[1]))
            
            # step two: move the rock in moveDir (if we can)
            nextRock.move(moveDir)
            # make sure we didn't move past either edge
            if nextRock.intersects(Coordinates(6,nextRock['y']), ShapeDef.V_LINE):
                nextRock.move(Direction.LEFT)
            elif nextRock.intersects(Coordinates(0, nextRock['y']), ShapeDef.V_LINE):
                nextRock.move(Direction.RIGHT)
            
            # step three: move the rock down
            nextRock.move(Direction.DOWN)
            
            # step test for collision with previous rock(s)/floor
            previousRockIndex = len(landedRocks) - 1
            while nextRock.moveable:
                if previousRockIndex >= 0:
                    if nextRock.intersects(landedRocks[previousRockIndex].tl_coords,
                                           landedRocks[previousRockIndex].shape):
                        nextRock.move(Direction.UP)
                        nextRock.land()
                        landedRocks.append(nextRock)
                        # move up the "floor" height to the top of the highest rock
                        if nextRock.tl_coords['y'] > stackHeight:
                            stackHeight = nextRock.tl_coords['y']
                        break
                    previousRockIndex -= 1
                else:
                    # we ran out of rocks to compare against, 
                    # check for hitting the floor
                    if nextRock.intersects(Coordinates(0,0), ShapeDef.FLOOR):
                        nextRock.move(Direction.UP)
                        nextRock.land()
                        landedRocks.append(nextRock)
                        # move up the "floor" height to the top of the highest rock
                        if nextRock.tl_coords['y'] > stackHeight:
                            stackHeight = nextRock.tl_coords['y']
                        break

                # didn't hit anything, move down again
                nextRock.move(Direction.DOWN)            

            # make sure we haven't landed
            if not nextRock.moveable:
                break
        


def part2(lines, args):
    pass


# parse the command line, read the input file, and run the part(s)
parts, inputfile, logLevel, args = parseAndLoad()
lines = readLines(inputfile)
partsMap = {"1": part1, "2": part2}
runLines(parts, partsMap, lines, args)