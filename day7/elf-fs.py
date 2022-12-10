## Day 7 - find the free space
# Today's problem is a filesystem traversal and free space challenge.
# Calculate the directory sizes and find candidates for deletion in order
# to free up space.
##

import re
from functools import total_ordering

# A Python class that represents an individual node
# in a Tree
@total_ordering
class DirOrFile:
    def __init__(self,name=None,size=0,isDir=False):
        self.children = dict()
        self.name = name
        self.size = size
        self.parent: DirOrFile = None
        self.isDir = isDir
    
    def __checkValidity(self, node: "DirOrFile"):
        if node.name == None and node.parent != None:
            raise Exception('Cannot create a DirOfFile without a name')
        if node.isDir and node.size > 0:
            raise Exception(f"Cannot have a directory with a file size. ({node.name})")
        if node.size < 0:
            raise Exception(f'Cannot have a negative file size. ({node.size})')
    
    def __str__(self) -> str:
        # build a display string for this node including parent path
        path = self.getPath()
        fileSizeStr = ''
        if not self.isDir:
            fileSizeStr = f'{self.size}'
        displayStr = f'{path}'
        if fileSizeStr != '':
            displayStr += f" size:{fileSizeStr}"

        return displayStr
    
    def __repr__(self) -> str:
        return str(self.__str__())
    
    def __lt__(self, obj: "DirOrFile"):
        return ((self.getPath()) < (obj.getPath())) if obj != None else False

    def __gt__(self, obj: "DirOrFile"):
        return ((self.getPath()) > (obj.getPath())) if obj != None else True
    
    def __eq__(self, obj: "DirOrFile"):
        
        return ((self.getPath()) == (obj.getPath())) if obj != None else False
        
    def __hash__(self):
        return self.getPath.__hash__()
    
    def printTree(self) -> str:
        displayStr = self.__str__() + "\n"
        if self.isDir:
            child: DirOrFile
            for child in self.getChildNodes():
                displayStr += child.printTree()
        return displayStr
            
    def addChild(self, node: "DirOrFile") -> bool:
        if not self.isDir:
            raise Exception("Cannot set a child node on a file.")
        self.__checkValidity(node)
        if self.children.get(node.name) == None:
            # node doesn't exist, add it
            self.children[node.name] = node
            node.parent = self
            return True
        return False
    
    def getChild(self, name: str) -> "DirOrFile":
        return self.children.get(name)
        
    def getPath(self):
        # return parent.getPath() unless parent None (root)
        # root returns `/`
        myPath = ''
        if self.parent != None:
            myPath += self.parent.getPath()
        if self.name:
            myPath += f'{self.name}'
        if self.isDir:
            myPath += '/'
        return myPath

    # returns a sorted list of child nodes, if any
    def getChildNodes(self):
        return sorted(self.children.values())
    
    def getParent(self) -> "DirOrFile":
        return self.parent

# this pattern is reused for command execution
dirPattern = r'(?:dir|cd) (.*)'
treeRoot: DirOrFile

# construct a tree from the input file
def buildDirTree(treeFile: str) -> DirOrFile:
    validCommands = ['$ cd', '$ ls']
    filePattern = r'(\d+) (.*)'
    global treeRoot
    global dirPattern
    
    fh = open(treeFile, 'r')
    # create root node in tree
    treeRoot = DirOrFile('', 0, True)
    currentDir = treeRoot
    # loop through the input lines, and build the tree as we find nodes
    for line in list(map(lambda l: l.strip(), fh.readlines())):
        isCommand = False
        for cmd in validCommands:
            if line.startswith(cmd):
                isCommand = True
                break
        
        if isCommand:
            currentDir = executeCommand(currentDir, line)
        else:
            # not a command, must be a file listing
            if re.match(dirPattern, line) != None:
                matches = re.match(dirPattern, line)
                if matches.group(1):
                    # new directory, add to current node
                    currentDir.addChild(DirOrFile(matches.group(1), 0, True))
                else:
                    raise Exception(f'Directory listing missing name: {{{line}}}')
            elif re.match(filePattern, line) != None:
                matches = re.match(filePattern, line)
                fileSize = matches.group(1)
                fileName = matches.group(2)
                if fileSize and fileName:
                    # new file, add to current node
                    currentDir.addChild(DirOrFile(fileName, int(fileSize)))
                else:
                    raise Exception(f'File listing invalid: {{{line}}}')
    return treeRoot

def executeCommand(currentDir: DirOrFile, cmd: str):
    global treeRoot
    if cmd.startswith('$ cd'):
        dirName = re.search(dirPattern, cmd).group(1)
        # change directory and return the new directory if the dir is not `/`
        if dirName == '..':
            return currentDir.parent if currentDir and currentDir.parent else currentDir
        if not dirName == '/':
            if not currentDir.getChild(dirName):
                newDir = DirOrFile(dirName, 0, True)
                currentDir.addChild(newDir)
                return newDir
            return currentDir.getChild(dirName)
        else:
            return treeRoot
    else:
        return currentDir

### Part 1 ###
# build the tree
treeFile = 'input.txt'
treeRoot = buildDirTree(treeFile)
print(f'Directory Tree\n{treeRoot.printTree()}')

# for a given node, total all the files sizes in the hierarchy recursively
def totalForNode(node: DirOrFile) -> int:
    nodeTotal = node.size
    if (node.isDir):
        child: DirOrFile
        for child in list(node.getChildNodes()):
            nodeTotal += totalForNode(child)
    return nodeTotal

validNodes = dict()
rejected = dict()

def pick(node: DirOrFile, total: int):
    # only pick if we haven't picked it before and it's not already been rejected
    if not validNodes.get(node) and not rejected.get(pick):
        print(f'==> picking {node.getPath()} ({total})')
        validNodes[node] = total

def reject(node: DirOrFile, total: int):
    print(f'### rejecting {node.getPath()} ({total}) because it\'s out of bounds')
    rejected[node] = True
                
def ignore(node: DirOrFile, reason: str='(same as recommended)'):
    # print(f'<-- ignoring {node.getPath()} {reason}')
    pass

# for a given node (directory or file) return the picked node
# nodes that should not be considered will return None (such as ignored files)
def consider(node: DirOrFile, targetSize=100000, sizeIsMax = True) -> DirOrFile:

    # don't consider files
    if not node.isDir:
        ignore(node, reason='(not a directory)')
        return None
    
    total = totalForNode(node)
    wasRejected = False
    
    if sizeIsMax and total > targetSize:
        reject(node, total)
        wasRejected = True
    elif not sizeIsMax and total < targetSize:
        reject(node, total)
        wasRejected = True

    if node.getChildNodes():
        for child in node.getChildNodes():
            next = consider(child, targetSize, sizeIsMax)
            if not next:
                continue
            nextTotal = totalForNode(next)
            
            # consider this candidate against the recommended and limits
            if sizeIsMax and nextTotal > targetSize:
                reject(next, nextTotal)
                continue
            elif not sizeIsMax and nextTotal < targetSize:
                reject(next, nextTotal)
                continue
            
            if (sizeIsMax and nextTotal > 0) or not sizeIsMax:
                pick(next, nextTotal)
        
    if not wasRejected:
        pick(node, total)
        
    # return node if it wasn't rejected
    return None if wasRejected else node
    

# perform a breadth-first traversal of the root node and collect directories
# that are <= 100000 size
consider(treeRoot)

def debugValidNodes():            
    print('validNodes:\n', end='')
    for node, size in validNodes.items():
        print(f'\t{node} {size}'.rstrip())

debugValidNodes()

sumTotal = sum(value for value in validNodes.values())
print(f'sum: {sumTotal}')

## Part 2: The directory death hunt
# Find the smallest directory that can be deleted that will free up sufficient space to allow the
# 30Mb update to be installed.
# Calculate the necessary sized directory to delete by subtracting the total amount of used storage
# you have (/ size) from the total amount storage available (70Mb) in order to find out how
# large of a directory you need to delete to free up 30MB
##

TOTAL_CAPACITY = 70000000
REQUIRED_FREE_SPACE = 30000000

totalUsed = totalForNode(treeRoot)

# clean the validNodes!!
validNodes.clear()

minRequiredSpace = REQUIRED_FREE_SPACE - (TOTAL_CAPACITY - totalUsed)

# this will consider directories that are at least large enough to free up enough space
consider(treeRoot, minRequiredSpace, False)

debugValidNodes()

smallestValid = None
node: DirOrFile
for node in validNodes.keys():
    nodeSize = totalForNode(node)
    
    if not smallestValid and nodeSize >= minRequiredSpace:
        smallestValid = node
    elif nodeSize < minRequiredSpace:
        continue
        
    if nodeSize < totalForNode(smallestValid):
        smallestValid = node
        
print(f'Deleting smallest directory {smallestValid.getPath()} will free up: {totalForNode(smallestValid)}')