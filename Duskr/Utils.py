import os

def getBasenameNoExt(wholeAddress):
    return os.path.splitext(os.path.basename(wholeAddress))[0]

def getFolderName(wholeAddress):
    return os.path.dirname(wholeAddress)

def getFileExt(wholeAddress):
    return os.path.splitext(os.path.basename(wholeAddress))[1]
