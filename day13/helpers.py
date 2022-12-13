import getopt
import sys
from io import TextIOWrapper
from enum import Enum
from functools import total_ordering


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


def error(msg: str) -> None:
    """Logs an error-level message. Error-level messages are always logged.

    Args:
        msg (str): message to log
    """
    print(f'ERROR: {msg}')


def warn(msg: str) -> None:
    """Logs a WARN-level message

    Args:
        msg (str): message to log
    """
    global logLevel
    if logLevel >= LogLevel.WARN:
        print(f'WARN: {msg}')


def info(msg: str) -> None:
    """Logs an INFO-level message.

    Args:
        msg (str): message to log
    """
    global logLevel
    if logLevel >= LogLevel.INFO:
        print(f'INFO: {msg}')


def debug(msg: str) -> None:
    """Logs a DEBUG-level message.

    Args:
        msg (str): message to log
    """
    global logLevel
    if logLevel >= LogLevel.DEBUG:
        print(f'DEBUG: {msg}')


def trace(msg: str) -> None:
    """Logs a TRACE-level message.

    Args:
        msg (str): message to log
    """
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

    return [executeParts, inputFile, getLogLevel()]


# given a list of parts to execute and the mapping of those part names to
# functions, run each part in turn provided the list input lines
def runlines(executeParts, partsMap, lines) -> None:
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
            partsMap[part](lines)
        except KeyError as e:
            error(f'part {part} not found ({e})')


# given a list of parts to execute and the mapping of those part names to
# functions, run each part in turn provided the open filehandle 'file'
def runfile(executeParts, partsMap, file) -> None:
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
            partsMap[part](file)
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
