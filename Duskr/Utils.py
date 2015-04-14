import os

def getBasenameNoExt(wholeAddress):
    return os.path.splitext(os.path.basename(wholeAddress))[0]

def getFolderName(wholeAddress):
    return os.path.dirname(wholeAddress)

def getFileExt(wholeAddress):
    return os.path.splitext(os.path.basename(wholeAddress))[1]



# a string as input.
# If it's a int, returns a int,
# if it's a float, returns a float,
# otherwise, returns a string
def castToWhatItShouldBe(val):

    # trying to cast to number
    try:
        # cast to float
        val = float(val)

        # if interger, cast to integer
        if(val.is_integer()):
            val = int(val)
        else:
            None

    except ValueError as e:
        None

    return val
