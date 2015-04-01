# ExivCRawRequester request XMP files (or XMP containing file) the fields setup
# by Adobe CameraRaw.
# To perform such request, it needs an XmpSettingLister instance and an ExivWrapper

from XmpSettingLister import *
from ExivWrapper import *

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
    def readValue(self, tag):

        # fetching the value
        requestedValue = self._exivWrapper.getValue(tag)

        return requestedValue


    # write a XMP field to an XMP compliant file
    def writeValue(self, tag, val):

        # if it's a curve sequence
        if(tag in self._xmpSettingLister.getCurvesSettingTags()):

            # Since curves use coordinate system, it works with pairs
            for i in range(0, len(val)/2):
                # making sub-arrays containing a string with coma
                coordCoupleStr = [str(val[2*i]) + ", " +   str(val[2*i+1])]

                self._exivWrapper.setValue(tag, coordCoupleStr, add=(i!=0))

        # it is not a sequence related to curves
        else:
            self._exivWrapper.setValue(tag, val)



# main tester
if __name__ == '__main__':


    # XMP compliant file
    xmpFile = "/Users/jonathanlurie/Desktop/_NIK4447_norot.dng"

    # read setting tag list
    xmpSL = XmpSettingLister()
    xmpSL.read()

    ecrr = ExivCRawRequester(xmpSL)
    ecrr.setXmpFile(xmpFile)

    # reading a field
    #print ecrr.readValue("Xmp.crs.ToneCurveBlue")

    ecrr.writeValue("Xmp.crs.ToneCurvePV2012", [11, 22, 33, 44, 55, 66, 77, 88])
