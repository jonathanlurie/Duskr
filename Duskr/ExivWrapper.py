# the ExivWrapper class provides a interface to comunicate easilly with
# Eviv2 application.
# It is not a proper wrapper because it calls directly the executable binary
# file.

import os

from ctypes import cdll
from ctypes import c_char_p
from ctypes import c_int
from ctypes import byref
from ctypes import create_string_buffer

class ExivWrapper :

    # the XMP file does not have to be a propper XMP
    # it can be a file embedding XMP data as well (i.e. DNG)
    _xmpFile = ""

    # low level dynamic library (.dylib file) that wraps exiv2 methods
    _exiv2wrapperLib = None


    # functions imported from the low level wrapper
    _wrapperFunction_getXmpValue = None
    _wrapperFunction_getXmpValue2 = None
    _wrapperFunction_addXmpStrField = None
    _wrapperFunction_addXmpSeqField = None
    _wrapperFunction_deleteXmpField = None

    #def __init__(self, libLocation = "../Frameworks/libexiv2wrapper.dylib"):
    def __init__(self, libLocation = "lib/natives/libexiv2wrapper.dylib"):
        self._exiv2wrapperLib = cdll.LoadLibrary(libLocation)

        # initialize wrapper functions
        self._wrapperFunction_getXmpValue = self._exiv2wrapperLib.getXmpValue
        self._wrapperFunction_getXmpValue.restype = c_char_p
        self._wrapperFunction_getXmpValue2 = self._exiv2wrapperLib.getXmpValue2
        self._wrapperFunction_getXmpValue2.restype = c_char_p
        self._wrapperFunction_addXmpstrField = self._exiv2wrapperLib.addXmpStrField
        self._wrapperFunction_addXmpSeqField = self._exiv2wrapperLib.addXmpSeqField
        self._wrapperFunction_deleteXmpField = self._exiv2wrapperLib.deleteXmpField



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

        arrayResult = self._wrapperFunction_getXmpValue(self._xmpFile, tag)

        result = None


        # if tag was not found, exit
        if(arrayResult == "0"):
            print("The tag was not found")
            return None

        # if image was not found, exit
        if(arrayResult == "-1"):
            print("The xmp file was not found")
            return None


        # else, we split the result
        result = arrayResult.split()

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


    # Get a value giving a xmp tag.
    # returns None if value not found
    # In cas of success, return a size-2 array :
    # [0] :
    def getValue2(self, tag):

        res = None

        success = c_int(0)
        success.value = 0

        isSequence = c_int(0)
        isSequence.value = 0

        result = self._wrapperFunction_getXmpValue2(self._xmpFile, tag, byref(success), byref(isSequence))

        if(success.value):
            res = [None, isSequence.value]

            # if its a sequence, we split it to get a list
            if(isSequence.value):
                res[0] = filter(None, result.split('|'))


            # if it's a simple string, we take it like that
            else:
                res[0] = result

        return res



    # sets a value of a tag.
    # If value if a list, then you can chose to add to or to replace the exsting
    # default is replacing. set add to True to add.
    # The value will be converted to strings (or to a list of string in cas of sequence)
    def setValue(self, tag, value):

        # is it list we want to add ?
        if(isinstance(value, list)):
            # transform the list into a easily-splitable string
            #listStr = "|".join(value)
            listStr = "|".join(str(x) for x in value)

            self._wrapperFunction_addXmpSeqField(self._xmpFile, tag, listStr)

        # this is not a list, just a single value
        else:
            self._wrapperFunction_addXmpstrField(self._xmpFile, tag, str(value))



    # erase a tag and its value
    def eraseTag(self, tag):
        self._wrapperFunction_deleteXmpField(self._xmpFile, tag)




# main tester
if __name__ == '__main__':


    #ew = ExivWrapper( libLocation="../lib/natives/libexiv2wrapper.dylib")
    ew = ExivWrapper()
    ew.setXmpFile("/Users/jonathanlurie/Desktop/_NIK4337.xmp")

    #val = ew.getValue("Xmp.crs.ToneCurve")
    #print val

    #ew.setValue("Xmp.crs.testIt", 39.8)
    #ew.eraseTag("Xmp.crs.testIt")

    ew.setValue("Xmp.crs.testString", "bonjour hello")
    #ew.setValue("Xmp.crs.testSeq", [41, 42, 43.5, 44])
    #ew.setValue("Xmp.crs.testTxtSeq", ["bonjour", "hello", "good morning", "hi"])
    #ew.eraseTag("Xmp.crs.testSeq")

    #print ew.getValue("Xmp.crs.ToneCurveGreen")
