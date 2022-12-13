import getopt
import sys
from enum import Enum


class LogLevel(Enum):
    WARN = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4

# global #


lines: list
logLevel: LogLevel = LogLevel.WARN


def setLogLevel(level: LogLevel) -> None:
    global logLevel
    if level:
        logLevel = level
    else:
        print('ERROR: invalid log level')


def getLogLevel() -> LogLevel:
    global logLevel
    return logLevel


def error(msg: str) -> None:
    print(f'ERROR: {msg}')


def warn(msg: str) -> None:
    global logLevel
    if logLevel >= LogLevel.WARN:
        print(f'WARN: {msg}')


def info(msg: str) -> None:
    global logLevel
    if logLevel >= LogLevel.INFO:
        print(f'INFO: {msg}')


def debug(msg: str) -> None:
    global logLevel
    if logLevel >= LogLevel.DEBUG:
        print(f'DEBUG: {msg}')


def trace(msg: str) -> None:
    global logLevel
    if logLevel >= LogLevel.TRACE:
        print(f'TRACE: {msg}')


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
        level (LogLevel)
    """
    global lines

    opts, args = getopt.getopt(sys.argv[1:], 'dp:f:', ["debug", "part=",
                                                       "file="])

    executeParts = []
    inputFile = 'input.txt'

    for opt, value in opts:
        if opt == '-p' or opt == '--part':
            executeParts.append(value)
        elif opt == 'f' or opt == '--file':
            inputFile = value
        elif opt == 'd' or opt == '--debug':
            setLogLevel(LogLevel.DEBUG)

    if not executeParts:
        executeParts.append('1')

    return [executeParts, inputFile, getLogLevel()]


# given a list of parts to execute and the mapping of those part names to
# functions, run each part in turn provided the list input lines
def run(executeParts, partsMap, lines) -> None:
    for part in executeParts:
        try:
            partsMap[part](lines)
        except KeyError as e:
            error(f'part {part} not found ({e})')


# read the lines of the provided file and return them as a list
def readLines(inputFile: str) -> list:
    # read input to get set of hypothetical moves
    fh = open(inputFile, 'r')
    return list(map(lambda line: line.rstrip(), fh.readlines()))
