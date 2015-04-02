# XmpDescriptor is specific to one XMP-compliant file.
# It contains all the XMP settings, original or interpolated.
# It also contains the information about the fact that is was insterpolated or not



import os

from XmpSettingLister import *
from ExivCRawRequester import *

import Utils


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

    # we need it for the name field
    _rawImageExtension = None


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

    def setRawImageExtension(self, ext):
        self._rawImageExtension = ext


    # returns True if this descriptor was base on a original xmp file
    def isOriginalFile(self):
        return self._isOriginalFile

    def getName(self):
        nameField = "Xmp.crs.RawFileName"
        return self._xmpDictionnary[nameField]


    # For debugging purpose
    # TODO : remove when done!!
    def getDictionary(self):
        return self._xmpDictionnary


    # update the raw image name in the dictionary
    def _updateFileName(self):
        nameField = "Xmp.crs.RawFileName"

        basenameNoExt = Utils.getBasenameNoExt(self._xmpFileName)
        newName = basenameNoExt + self._rawImageExtension
        self._xmpDictionnary[nameField] = newName


    # fills the dictionary with
    # - Nones if there is no original values
    # - original values if it's a original file
    def initDictionary(self):

        # concatenate all list of tags for an easier process
        allTags = self._xmpSettingList.getBasicSettingTags() + \
            self._xmpSettingList.getCurvesSettingTags() + \
            self._xmpSettingList.getCropSettingTags()

        # each tag is...
        for tag in allTags:

            # ... attributed to None
            value = None

            # ... or read in the original xmp file
            if(self._isOriginalFile):
                value = self._exivCRawRequester.readValue(tag)

                if(value and len(value) == 1):
                    value = value[0]

            # updating the dictionary
            self._xmpDictionnary[tag] = value

        # updating the filename in the dictionary
        self._updateFileName()


    # write the content of the dictionary into the XMP file
    def writeDictionary(self):

        for couple in self._xmpDictionnary.items():
            self._exivCRawRequester.writeValue(couple[0], couple[1])


    # return a value from the dictionary, giving a tag
    # or None if the tag does not exist
    def getFromDictionary(self, tag):
        if(tag in self._xmpDictionnary):
            return self._xmpDictionnary[tag]
        else:
            return None


    # set the value into the dictionary (no further verification)
    def setToDictionary(self, tag, value):
        self._xmpDictionnary[tag] = value


# main tester
if __name__ == '__main__':

    # list of setting tags
    xmpSL = XmpSettingLister()
    xmpSL.read()

    # XMP compliant file
    xmpFile = "/Users/jonathanlurie/Desktop/test2.xmp"
    #xmpFile = "/Users/jonathanlurie/Desktop/_NIK4447_ORIG.dng"
    #xmpFile = "/Users/jonathanlurie/Desktop/_NIK4447_norot.dng"

    xmpDesc = XmpFileDescriptor(xmpFile, xmpSL)
    xmpDesc.setRawImageExtension(".NEF")
    xmpDesc.setIsOriginal(True)
    xmpDesc.initDictionary()

    print xmpDesc.getFromDictionary("Xmp.crs.Exposure2012")

    xmpDesc.setToDictionary("Xmp.crs.Exposure2012", -1.05)

    print xmpDesc.getFromDictionary("Xmp.crs.Exposure2012")

    xmpDesc.writeDictionary()
