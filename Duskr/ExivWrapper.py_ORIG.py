# the ExivWrapper class provides a interface to comunicate easilly with
# Eviv2 application.
# It is not a proper wrapper because it calls directly the executable binary
# file.

import os

class ExivWrapper :

    # location of the executable file exiv2
    _binaryLocation = "/Users/jonathanlurie/Documents/code/gitRepo/Duskr/extbin/exiv2"

    # the XMP file does not have to be a propper XMP
    # it can be a file embedding XMP data as well (i.e. DNG)
    _xmpFile = ""

    def __init__(self):
        None


    # shell calling with popen.
    # return an array with the result (empty array if no print)
    def _executeCommand(self, cmd):
        rawOutput = os.popen(cmd).read()

        # the result can contain several lines
        outputLines = rawOutput.split('\n')

        cleanResult = []

        # each lines must be split with spaces
        for line in outputLines:
            cleanResult.append( line.split())

        # the last one is most of the time empty
        cleanResult = filter(None, cleanResult)

        #print cleanResult

        #exit()


        return cleanResult

    # a string as input.
    # If it's a int, returns a int,
    # if it's a float, returns a float,
    # otherwise, returns a string
    def _castToWhatItShouldBe(self, val):

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


    # the XMP file does not have to be a propper XMP
    # it can be a file embedding XMP data as well  (i.e. DNG)
    def setXmpFile(self, fileAddress):
        self._xmpFile = fileAddress


    # return the value of the tag, as :
    # - a number (XmpText but actually a number
    # - a string (XmpText)
    # - a list (XmpSeq)
    def getValue(self, tag):
        cmd = self._binaryLocation + " -P X " + self._xmpFile + " | grep " + tag
        arrayResult = self._executeCommand(cmd)

        result = None

        # the arrayResult might contain other fieds than the requested
        for line in arrayResult:

            # condition 1.
            if(line[0] == tag):
                result = line
                break

        # if was not found, exit
        if(not result):
            return None

        # empty list to store the clean and casted result
        cleanResult = []

        # check the result instegrity
        # 2. this must be an array of size 4 minimu
        if(len(result) >= 4):


            # 3. the second must be "XmpSeq" or "XmpText"
            if(result[1] == "XmpText"):


                # we dont really care about result[2] which is the size of the value,
                # so we just take the value
                resultString = ' '.join( result[3:] )
                cleanResult.append(self._castToWhatItShouldBe(resultString))

            elif(result[1] == "XmpSeq"):
                # we dont really care about result[2] which is the size of the value
                # so lets start casting value:
                for i in range(3, len(result)):

                    # in a XmpSeq, values are split by "," comma, so we have to strop them
                    tempValue = result[i]

                    if(tempValue[-1] == ","):
                        tempValue = tempValue[0:-1]

                    cleanResult.append(self._castToWhatItShouldBe(tempValue))

            else:
                # another type of data, not processed
                None

        return cleanResult


    # sets a value of a tag.
    # If value if a list, then you can chose to add to or to replace the exsting
    # default is replacing. set add to True to add.
    # The value will be converted to strings (or to a list of string in cas of sequence)
    def setValue(self, tag, value, add=False):

        # is it list we want to add ?
        if(isinstance(value, list)):

            # we do not add, but replace. Meaning erase first
            if(not add):
                self.eraseTag(tag)

            basicCmd = self._binaryLocation + ' -M"set ' + tag + ' XmpSeq '

            # over all values
            for val in value:
                cmd = basicCmd + str(val) + '" ' + self._xmpFile

                self._executeCommand(cmd)

        # this is not a list, just a single value
        else:
            cmd = self._binaryLocation + ' -M"set ' + tag + ' XmpText ' + str(value) + '" ' + self._xmpFile
            self._executeCommand(cmd)



    # erase a tag and its value
    def eraseTag(self, tag):
        cmd = self._binaryLocation + ' -M"del ' + tag + '" '  + self._xmpFile
        self._executeCommand(cmd)




# main tester
if __name__ == '__main__':


    ew = ExivWrapper()
    ew.setXmpFile("/Users/jonathanlurie/Desktop/test.xmp")

    val = ew.getValue("Xmp.crs.ToneCurve")
    print val

    #ew.setValue("Xmp.crs.testIt", 39.8)
    #ew.eraseTag("Xmp.crs.testIt")

    #ew.setValue("Xmp.crs.testSeq", [41, 42, 43.5, 44], add=True)
    ew.eraseTag("Xmp.crs.testSeq")
