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

    # def isDir(self) -> bool:
    #     return self.isDir
            
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

# # given a base directory and a maximum file size, find all the files under the max size and return
# # the map of path -> size
# def findBySize(baseDir: DirOrFile, maxSize: int) -> dict:
#     foundMap = dict()
        
#     if baseDir == None or maxSize == None:
#         return foundMap
    
#     node: DirOrFile
#     for node in baseDir.getChildNodes():
#         if node.isDir:
#             dirResult = findBySize(node, maxSize)
#             if dirResult:
#                 foundMap.update(dirResult)
#         else:
#             if node.size <= maxSize:
#                 foundMap[node] = node.size
                    
#     return foundMap
    
# # this will be the map of all files found (starting at the root) that are <= 100,000 size keyed by node (which are sortable, comparable)
# foundMap = findBySize(treeRoot, 100000)

# print('foundMap:\n', end='')
# node: DirOrFile
# for node, size in foundMap.items():
#     print(f'\t{node.getPath()} {size}')

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
    print(f'### rejecting {node.getPath()} because it\'s too big {total}')
    rejected[node] = True
                
def ignore(node: DirOrFile, reason: str='(same as recommended)'):
    print(f'<-- ignoring {node.getPath()} {reason}')

def recommend(node: DirOrFile, total: int):
    print(f'==> recommending {node.getPath()} ({total})')
    
# for a given node (directory or file) return the recommended node
# optionally provide a recommended node to compare against
# nodes that should not be considered will return None (such as ignored files)
def consider(node: DirOrFile, recommended: DirOrFile=None, rTotal: int=0, includeFiles = False) -> DirOrFile:

    # don't consider files unless requested
    if not node.isDir and not includeFiles:
        ignore(node, reason='(not a directory)')
        return node
    
    total = totalForNode(node)
    print(f'...considering {node.getPath()} ({total})', end='')
    print(f' against recommended {recommended.getPath()} ({rTotal})') if recommended else print('')

    if total > 100000:
        reject(node, total)

    # if we don't already have a recommendation and this is good, recommend it
    if not recommended and total <= 100000 and total > 0:
        recommend(node, total)
        recommended = node
        rTotal = total

    if node.getChildNodes():
        newRecommended: DirOrFile = None
        nTotal = 0
        for child in node.getChildNodes():
            next = consider(child, newRecommended or recommended, 
                            nTotal or rTotal, includeFiles)
            if not next or (not next.isDir and not includeFiles):
                continue
            nextTotal = totalForNode(next)
            
            # consider this candidate against the recommended and limits
            if nextTotal > 100000:
                reject(next, nextTotal)
                continue
            
            if next != node and nextTotal == total and total > 0:
                ignore(next)
                continue
            elif next == node and nextTotal > 0:
                pick(next, nextTotal)
                continue
            elif nextTotal < rTotal and nextTotal > 0:
                recommend(next, nextTotal)
                newRecommended = next
                nTotal = nextTotal
                continue
            else:
                # don't consider this directory
                ignore(next, reason='(Not a dir)')
                continue
        
            
    # all things being equal, if this and its parent are the same, pick this
    if recommended != node and rTotal == total and total > 0:
        recommend(node, total)
        return recommended
    elif recommended == node:
        pick(recommended, rTotal)
        return None
    elif total < rTotal:
        pick(node, total)
        if recommended:
            recommend(recommended, rTotal)
        return recommended or None
    
    # if we got here with a recommendation, pick it
    if recommended:
        pick(recommended, rTotal)
        
    # return node if it wasn't rejected
    return recommended
    

# perform a breadth-first traversal of the root node and collect directories
# that are <= 100000 size
for rootNode in treeRoot.getChildNodes():
    consider(rootNode)
        
# keep going until we reach the root (parent == None) or we find a parent with a different total
# while(nextParent):
#     # don't bother if we've already added this parent from another path, or it's been rejected already
#     if not validNodes.get(nextParent) and not rejected.get(nextParent):
#         print(f'...considering {nextParent.getPath()}')
#         # the parent's total to compare to the 'toPick' total
#         nextTotal = totalForNode(nextParent)
#         # print(f'<nextParent totalForNode "{nextParent.getPath()}": {nextTotal}>')

#         # if we don't have a candidate yet, pick this one
#         if not toPick:
#             toPick = nextParent
#             pickTotal = nextTotal

#         if nextTotal > 100000:
#             # skip this parent from now on - it's too big

#         if pickTotal == nextTotal and nextTotal <= 100000:
#             # print(f'...candidate changed to: {nextParent.getPath()} ({nextTotal})')
#             toPick = nextParent
#         elif pickTotal != nextTotal:
#             if not rejected.get(toPick):
#                 print(f'==> picking {toPick.getPath()} ({pickTotal})')
#                 validNodes[toPick] = pickTotal
#                 toPick = None
#                 pickTotal = 0
#             break
#     elif not validNodes.get(toPick) and rejected.get(nextParent):
#         if toPick:
#             toPick = None
#             pickTotal = 0
#         break
    
#     # if nextParent.getParent() == None:
#         # print(f"We've reached the root: (node: {nextParent.getPath()})")
#     nextParent = nextParent.getParent()
            
print('validNodes:\n', end='')
for node, size in validNodes.items():
    print(f'\t{node} {size}'.rstrip())


sumTotal = sum(value for value in validNodes.values())
print(f'sum: {sumTotal}')