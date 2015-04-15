# ExivCRawRequester request XMP files (or XMP containing file) the fields setup
# by Adobe CameraRaw.
# To perform such request, it needs an XmpSettingLister instance and an ExivWrapper

from XmpSettingLister import *
from ExivWrapper import *

import Utils

class ExivCRawRequester:

    # the XMP file does not have to be a propper XMP
    # it can be a file embedding XMP data as well (i.e. DNG)
    _xmpFile = ""

    # wrapper to access the xmp data within files
    _exivWrapper = None

    # object that contains a list of all setting tags
    _xmpSettingLister = None


    # constructor, take a XmpSettingLister that has been already read()
    def __init__(self, xmpSetListr):
        self._exivWrapper = ExivWrapper()
        self._xmpSettingLister = xmpSetListr


    # set the xmp compliant file
    def setXmpFile(self, xmpFileAddress):
        self._exivWrapper.setXmpFile(xmpFileAddress)


    # read a XMP value from a XMP compliant file
    # returns an array, no matter the number of output
    def readValue(self, tag):

        # fetching the value
        requestedValue = self._exivWrapper.getValue2(tag)

        # to store the return value
        result = None

        # None check, because the requested field might be
        # absent from the xmp file
        if(requestedValue):
            result = []

            # if it is a sequence
            if(requestedValue[1]):
                # sequence are for curves, split by coma ","
                for elem in requestedValue[0]:
                    for coord in elem.split(','):
                        result.append(Utils.castToWhatItShouldBe(coord))


            # if it is not a sequence
            else:
                result.append(Utils.castToWhatItShouldBe(requestedValue[0]))

        return result


    # write a XMP field to an XMP compliant file
    def writeValue(self, tag, val):

        # if the value is not set (None), no xmp writing
        if(not val):
            return

        # if it's a curve sequence
        if(tag in self._xmpSettingLister.getCurvesSettingTags()):

            valConcat = []
            # Since curves use coordinate system, it works with pairs
            for i in range(0, len(val)/2):
                # making sub-arrays containing a string with coma. Split again with a pipe
                valConcat.append( str(val[2*i]) + ", " +   str(val[2*i+1]) )

            self._exivWrapper.setValue(tag, valConcat)

        # it is not a sequence related to curves
        else:
            self._exivWrapper.setValue(tag, val)



# main tester
if __name__ == '__main__':


    # XMP compliant file
    xmpFile = "/Users/jonathanlurie/Desktop/_NIK4337.xmp"

    # read setting tag list
    xmpSL = XmpSettingLister()
    xmpSL.read()

    ecrr = ExivCRawRequester(xmpSL)
    ecrr.setXmpFile(xmpFile)

    # reading a field
    #print ecrr.readValue("Xmp.crs.Highlights2012")

    ecrr.writeValue("Xmp.crs.MyCustomCurve", [11, 22, 33, 44, 55, 66, 77, 88])
    #ecrr.writeValue("Xmp.crs.MyCustomValue", "hello")
