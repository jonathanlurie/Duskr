# XmpDescriptor is specific to one XMP-compliant file.
# It contains all the XMP settings, original or interpolated.
# It also contains the information about the fact that is was insterpolated or not



import os

from XmpSettingLister import *
from ExivCRawRequester import *


class XmpFileDescriptor:

    # tell if the settings comes from an orinal XMP file.
    # if False, it means it was interpolated
    _isOriginalFile = False


    # address of the xmp-compliant file
    _xmpFileName = None


    # the dictionary is a 'key'=value container
    # where the key is the xmp tag and the value can be
    # a float, an int, a string or a list
    _xmpDictionnary = None


    # the settings list is a instance of XmpSettingLister.
    # for knowing the whole list of tags
    _xmpSettingList = None


    # to read and/or write xmp data to the xmp file
    _exivCRawRequester = None


    # Constructor
    # xmpSettingList must be read() in advance
    def __init__(self, xmpFile, xmpSettingList):

        # file name
        self._xmpFileName = xmpFile


        # the setting list
        self._xmpSettingList = xmpSettingList

        # requester
        self._exivCRawRequester = ExivCRawRequester(self._xmpSettingList)
        self._exivCRawRequester.setXmpFile(self._xmpFileName)

        # empty dict
        self._xmpDictionnary = {}


    # isIt must be True if the xmp file is an original one
    def setIsOriginal(self, isIt):
        self._isOriginalFile = isIt


    # update the raw image name in the dictionary
    def updateFileName(self):
        nameField = "Xmp.crs.RawFileName"

        # check it first, then update it if necessary
        currentName = self._exivCRawRequester.readValue(nameField)

        # since it's a list
        if(currentName):
            # getting rid of the list structure
            currentName = currentName[0]

            # the filename within xmp data is NOT up to date
            #if(os.path.splitext(currentName)[0] != os.path.splitext(os.path.basename(self._xmpFileName))[0] ):
            newName = os.path.splitext(os.path.basename(self._xmpFileName))[0] + os.path.splitext(currentName)[1]
            #self._exivCRawRequester.writeValue(nameField, newName)
            self._xmpDictionnary[nameField] = newName


    # fills the dictionary with Nones or with orinal value if it's a original file
    def fillDictionary(self):

        allTags = self._xmpSettingList.getBasicSettingTags() + self._xmpSettingList.getCurvesSettingTags() + self._xmpSettingList.getCropSettingTags()

        for tag in allTags:

            value = None

            if(self._isOriginalFile):
                value = self._exivCRawRequester.readValue(tag)

                if(value and len(value) == 1):
                    value = value[0]


            self._xmpDictionnary[tag] = value

        self.updateFileName()

        print self._xmpDictionnary


# main tester
if __name__ == '__main__':

    # list of setting tags
    xmpSL = XmpSettingLister()
    xmpSL.read()

    # XMP compliant file
    xmpFile = "/Users/jonathanlurie/Desktop/_NIK4337_name.xmp"
    #xmpFile = "/Users/jonathanlurie/Desktop/_NIK4447_ORIG.dng"
    #xmpFile = "/Users/jonathanlurie/Desktop/_NIK4447_norot.dng"

    xmpDesc = XmpFileDescriptor(xmpFile, xmpSL)


    xmpDesc.setIsOriginal(True)

    xmpDesc.fillDictionary()
