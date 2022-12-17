import getopt
import sys
from io import TextIOWrapper
from enum import Enum
from functools import total_ordering

__all__ = ["Coordinates", "Direction", "LogLevel", "setLogLevel", 
           "getLogLevel", "error", "info", "warn", "debug", "trace", 
           "parseAndLoad", "runLines", "runFile", "readLines", "openFile"]


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    ANY = 'A'


# simple class represting an (x,y) coordinate pair
class Coordinates:
    """Represents a coordinate pair (x,y) that is comparable in a given
    dimension, scriptable, hashable, and can determine adjacency with another
    Coordinates object.
    """
    def __init__(self, xpos: int, ypos: int):
        self.x = xpos
        self.y = ypos

    def __str__(self) -> str:
        # build a display string for this TallTree
        return f'({self.x},{self.y})'

    def __repr__(self) -> str:
        return str(self.__str__())

    def __eq__(self, other: "Coordinates") -> bool:
        if other is None:
            return False
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other: "Coordinates") -> bool:
        if other is None:
            return True
        return (self.x, self.y) != (other.x, other.y)

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __getitem__(self, item) -> int:
        if item == 0 or item == 'x':
            value = self.x
        elif item == 1 or item == 'y':
            value = self.y
        else:
            raise IndexError(f'{item} is not a valid index')
        return value

    def __setitem__(self, item, value: int) -> None:
        if item == 0 or item == 'x':
            self.x = value
        elif item == 1 or item == 'y':
            self.y = value
        else:
            raise IndexError(f'{item} is not a valid index')

    def compareX(self, other: "Coordinates"):
        return self.x - other.x

    def compareY(self, other: "Coordinates"):
        return self.y - other.y

    def isAdjacent(self, other: "Coordinates", dir: Direction = Direction.ANY) -> bool:
        """Determines if the other Coordinates is adjacent to this in any
        cardinal direction.

        Args:
            other (Coordinates): Coordinate to compare to this

        Returns:
            bool: True if the other coordinate is adjacent; false otherwise
        """
        # if the other is the same coordinates, then they're "adjacent"
        if other == self:
            return True
        
        if dir == Direction.ANY:
            if other == Coordinates(self['x'], self['y']+1) or \
               other == Coordinates(self['x'], self['y']-1):
                return True
            if other == Coordinates(self['x']+1, self['y']) or \
               other == Coordinates(self['x']-1, self['y']):
                return True
        elif dir == Direction.DOWN:
            if other == Coordinates(self['x'], self['y']+1):
                return True
        elif dir == Direction.UP:
            if other == Coordinates(self['x'], self['y']-1):
                return True
        elif dir == Direction.RIGHT:
            if other == Coordinates(self['x']+1, self['y']):
                return True
        elif dir == Direction.LEFT:
            if other == Coordinates(self['x']-1, self['y']):
                return True
            
        return False

    def isDiagaonallyAdjacent(self, other: "Coordinates",
                              dir: Direction = Direction.ANY) -> bool:
        """Determines if the other Coordinates is adjacent to this in any
        diagonal direction. 

        Args:
            other (Coordinates): The coordinate to consider
            dir (Direction) (optional): Direction to consider only. Default ANY

        Returns:
            bool: True if 'other' is diagonally adjacent to this coordinate
        """
        ur = Coordinates(other['x']+1, other['y']+1)
        ul = Coordinates(other['x']-1, other['y']+1)
        dr = Coordinates(other['x']+1, other['y']-1)
        dl = Coordinates(other['x']-1, other['y']-1)

        if dir == Direction.ANY:
            return self == ur or self == ul or self == dr or self == dl
        elif dir == Direction.UP:
            return self == ur or self == ul
        elif dir == Direction.DOWN:
            return self == dr or self == dl
        elif dir == Direction.LEFT:
            return self == dl or self == ul
        elif dir == Direction.RIGHT:
            return self == ur or self == dr



@total_ordering
class LogLevel(Enum):
    WARN = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4

    def __lt__(self, other: "LogLevel") -> bool:
        return self._value_ < other._value_

    def __gt__(self, other: "LogLevel") -> bool:
        return self._value_ > other._value_

    def __eq__(self, other: "LogLevel") -> bool:
        return super().__eq__(other)

    def __ne__(self, other: "LogLevel") -> bool:
        return super().__ne__(other)


# global #


lines: list
logLevel: LogLevel = LogLevel.WARN


def setLogLevel(level: LogLevel) -> None:
    """Set the current log level.  Logging below this level will be logged.

    Args:
        level (LogLevel): maximum level to log
    """
    global logLevel
    if level:
        logLevel = level
    else:
        print('ERROR: invalid log level')


def getLogLevel() -> LogLevel:
    """Returns the current logging level.

    Returns:
        LogLevel: current logging level
    """
    global logLevel
    return logLevel


def error(msg: str, end='\n') -> None:
    """Logs an error-level message. Error-level messages are always logged.

    Args:
        msg (str): message to log
    """
    print(f'ERROR: {msg}', end)


def warn(msg: str, end='\n') -> None:
    """Logs a WARN-level message

    Args:
        msg (str): message to log
    """
    global logLevel
    if logLevel >= LogLevel.WARN:
        print(f'WARN: {msg}', end)


def info(msg: str, end='\n') -> None:
    """Logs an INFO-level message.

    Args:
        msg (str): message to log
    """
    global logLevel
    if logLevel >= LogLevel.INFO:
        print(f'INFO: {msg}', end)


def debug(msg: str, end='\n') -> None:
    """Logs a DEBUG-level message.

    Args:
        msg (str): message to log
    """
    global logLevel
    if logLevel >= LogLevel.DEBUG:
        print(f'DEBUG: {msg}', end)


def trace(msg: str, end='\n') -> None:
    """Logs a TRACE-level message.

    Args:
        msg (str): message to log
    """
    global logLevel
    if logLevel >= LogLevel.TRACE:
        print(f'TRACE: {msg}', end)


##
# parse the command line into a list of:
# 1. parts to execute (list)
# 2. input file name (str)
# 3. current log level (LogLevel)
####
def parseAndLoad() -> list:
    """Parse the command line arguments into the parts to execute and file
    name.

    Returns:
        list: parts to execute (list), input file name (str), current log
        level (LogLevel), program arguments
    """
    global lines

    opts, args = getopt.getopt(sys.argv[1:], 'iwdtp:f:', ["info", "warn",
                                                          "debug", "trace",
                                                          "part=", "file="])

    executeParts = []
    inputFile = 'input.txt'

    for opt, value in opts:
        if opt == '-p' or opt == '--part':
            executeParts.append(value)
        elif opt == 'f' or opt == '--file':
            inputFile = value
        elif opt == 'i' or opt == '--info':
            setLogLevel(LogLevel.INFO)
        elif opt == 'w' or opt == '--warn':
            setLogLevel(LogLevel.WARN)
        elif opt == 'd' or opt == '--debug':
            setLogLevel(LogLevel.DEBUG)
        elif opt == 't' or opt == '--trace':
            setLogLevel(LogLevel.TRACE)

    if not executeParts:
        executeParts.append('1')

    return [executeParts, inputFile, getLogLevel(), args]


# given a list of parts to execute and the mapping of those part names to
# functions, run each part in turn provided the list input lines
def runLines(executeParts, partsMap, lines, args) -> None:
    """Executes the specified set of parts using the partsMap to match a part
    to a function, passing each function call the list if lines from a file

    Args:
        executeParts (_type_): a set of part names to execute
        partsMap (_type_): a map of part names to functions that take a single
        list argument
        lines (_type_): the list of lines in a file
    """
    for part in executeParts:
        try:
            partsMap[part](lines, args)
        except KeyError as e:
            error(f'part {part} not found ({e})')


# given a list of parts to execute and the mapping of those part names to
# functions, run each part in turn provided the open filehandle 'file'
def runFile(executeParts, partsMap, file, args) -> None:
    """Executes the specified set of parts using the partsMap to match a part
    to a function, passing each function call the filehandle called 'file'

    Args:
        executeParts (_type_): a set of part names to execute
        partsMap (_type_): a map of part names to functions that take a single
        filehandle argument
        file (_type_): an open filehandle to pass to the functions
    """
    for part in executeParts:
        try:
            partsMap[part](file, args)
        except KeyError as e:
            error(f'part {part} not found ({e})')


# read the lines of the provided file and return them as a list
def readLines(inputFile: str) -> list:
    """Reads an input file completely into a list of lines

    Args:
        inputFile (str): the input file to read

    Returns:
        list: a list of lines in the file
    """
    # read input to get set of hypothetical moves
    fh = open(inputFile, 'r')
    return list(map(lambda line: line.rstrip(), fh.readlines()))


def openFile(inputFile: str) -> TextIOWrapper:
    """Opens a text file for reading and returns the file handle as a
    TextIOWrapper object.

    Args:
        inputFile (str): file to open

    Returns:
        TextIOWrapper: file handle
    """
    return open(inputFile, 'r')
