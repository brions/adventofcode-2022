## Day 10 - Interpreting Elvish assembly code
# Today's problem involves parsing a set of instructions that take some amount of time to execute
# and checking the 'signal strength' throughout the execution periodically.
##

from enum import Enum

##################
# Definitions Start Here
########################

####
# globals
#########
debug = False

# keep track of the CPU clock cycles - 1 = 1 tick/cycle
clock = 0
registerX = 1

# cause the CPU to pass through one cycle and update all in-process commands in order
def tick(inProcessList: list=None) -> None:
    global clock
    global registerX
    
    print(f'cycle: {clock}') if debug else None
    # print(f'inProcess: {inProcessList}') if debug else None
    inProcessList[0].tick() if inProcessList else None
    # command: Command
    # for command in inProcessList:
    #     command.tick()
        # print(f'registerX: {registerX}') if debug else None
        
    clock +=1


# enumeration of CPU instruction (value is intrinsic CPU cost)
class Instruction(Enum):
    noop = 1
    addx = 2

# clock cycles to check 'signal strength'
checkCycle = [20, 60, 100, 140, 180, 220]

class Command:
    instruction: Instruction
    value: int
    cyclesRemaining: int
    
    def __init__(self, instr: Instruction, value: int=None) -> None:
        self.instruction = instr
        self.value = value
        self.cyclesRemaining = instr.value
    
    def __str__(self) -> str:
        return f'{self.instruction}' + (f' {self.value}' if self.value else '')
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def tick(self) -> None:
        self.cyclesRemaining -= 1 if self.cyclesRemaining > 0 else 0
        
    def result(self) -> int:
        if self.cyclesRemaining == 0:
            return self.value
        else:
            return None
    
    def isComplete(self) -> bool:
        return self.cyclesRemaining == 0
    

def calculateSignalStrength() -> int:
    return registerX * clock

def printSignal() -> None:
    print(f'Signal strength at clock cycle {clock}: {calculateSignalStrength()}')

def drawPixel(on: bool) -> None:
    print('#', end='') if on else print('.', end='')

##################
# Logic Start Here
########################

## Part 1
def part1(lines: list) -> None:
    global debug
    global registerX
    
    signals = list()
    commandList = list()
    inProcess = list()
    
    line: str
    for line in lines:
        print(f'line: {line}') if debug else None
        try:
            instruction, value = line.split()
            instruction = Instruction[instruction]  # convert value into enum
        except ValueError:
            # this is ok, it just means have a noop
            instruction = Instruction.noop
            value = None
        # print(f'instruction: \'{instruction}\', value: \'{value}\'') if debug else None
        commandToAdd = Command(instruction, value)
        print(f'command: {commandToAdd}') if debug else None
        commandList.append(commandToAdd)
        
    # reverse the command list and pop one off each cycle
    commandList.reverse()
    
    # start the CPU clock ticking
    for cycle in range(1, 221, 1):        
        command = commandList.pop() if commandList else None
        inProcess.append(command) if command else None
        
        cmd: Command
        for cmd in inProcess:
            result = cmd.result()
            if result:
                registerX += int(result)
            inProcess.remove(cmd) if cmd.isComplete() else None

        # increase the cpu cycle and update every in-process command
        tick(inProcess)
        
        print(f'registerX: {registerX}') if debug else None

        if cycle in checkCycle:
            signals.append(calculateSignalStrength())
            printSignal() if debug else None
            
    print(f'Total signal strength: {sum(signals)}')

## Part 2
def part2(lines: list) -> None:
    global debug
    global registerX
    
    crtHPos: int = 0
    
    signals = list()
    commandList = list()
    inProcess = list()
    
    line: str
    for line in lines:
        print(f'line: {line}') if debug else None
        try:
            instruction, value = line.split()
            instruction = Instruction[instruction]  # convert value into enum
        except ValueError:
            # this is ok, it just means have a noop
            instruction = Instruction.noop
            value = None
        # print(f'instruction: \'{instruction}\', value: \'{value}\'') if debug else None
        commandToAdd = Command(instruction, value)
        print(f'command: {commandToAdd}') if debug else None
        commandList.append(commandToAdd)
        
    # reverse the command list and pop one off each cycle
    commandList.reverse()
    
    # start the CPU clock ticking
    for cycle in range(1, 241, 1):        
        command = commandList.pop() if commandList else None
        inProcess.append(command) if command else None
        
        cmd: Command
        for cmd in inProcess:
            result = cmd.result()
            if result:
                registerX += int(result)
            inProcess.remove(cmd) if cmd.isComplete() else None

        drawPixel(crtHPos in list(range(registerX-1, registerX+2)))
        if crtHPos == 39:
            print('\n', end='')
            
        # increase the cpu cycle and update every in-process command
        tick(inProcess)
        # increase the crt position
        crtHPos = (crtHPos + 1) % 40
        
        print(f'registerX: {registerX}') if debug else None

        if cycle in checkCycle:
            signals.append(calculateSignalStrength())
            printSignal() if debug else None
            
    print(f'\nTotal signal strength: {sum(signals)}')
    


#### main execution area ####
import getopt
import sys

opts, args = getopt.getopt(sys.argv[1:], 'dp:f:', ["debug", "part=", "file="])

availableParts = {'1': part1, '2': part2}

executeParts = []
inputFile = 'input.txt'

for opt, value in opts:
    if opt == '-p' or opt == '--part':
        executeParts.append(value)
    elif opt == 'f' or opt == '--file':
        inputFile = value
    elif opt == 'd' or opt == '--debug':
        debug = True
        
if not executeParts:
    executeParts.append('1')
        
# read input to get set of hypothetical moves
fh = open(inputFile, 'r')
lines = list(map(lambda l: l.rstrip(), fh.readlines()))

for part in executeParts:
    if part in availableParts:
        availableParts[part](lines)
