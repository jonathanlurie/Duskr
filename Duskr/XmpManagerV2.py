
import os
import glob
import time

from XmpSettingLister import *
from XmpFileDescriptor import *
from XmpFileInterpolator import *
import Utils

#import tracer


class XmpManager:

    # list of XmpFileDescriptor
    _xmpDescriptors = None

    # raw image extension, to be guessed
    _rawExtension = None

    # raw image folder, to be guessed
    _imageFolder = None

    # xmp file extension to guess
    _xmpExtensionGuess = ".[Xx][Mm][Pp]"

    # the real xmp extention, to be guessed
    _xmpExtensionActual = None

    # list of raw images
    _rawImageList = None

    # list of original xmp file (must be of size 2, at least)
    _xmpBaseList = None

    # gather all the setting tags used in Adobe CameraRaw
    _xmpSettingLister = None


    # Constructor
    def __init__(self):

        # create an empty list of XmpFileDescriptor
        self._xmpDescriptors = []

        # construct the setting tag lister , and read() once
        self._xmpSettingLister = XmpSettingLister()
        self._xmpSettingLister.read()




    # A random image from the sequence will help define:
    # - the folder address (here)
    # - the raw file extension (here)
    # - the list of raw image to compose the sequence (later)
    # - if xmp files are present in the folder (later)
    def setRandomImageFromSequence(self, imgAddress):

        # guessing the raw extension from the first image
        self._rawExtension = Utils.getFileExt(imgAddress)

        # guessing the input folder from the first image
        self._imageFolder = Utils.getFolderName(imgAddress)



    def parseSequenceFolder(self):
        # finding the raw files
        self._rawImageList = sorted(glob.glob(self._imageFolder + os.sep + '*' + self._rawExtension))

        # finding the xmp files
        self._xmpBaseList = sorted(glob.glob(self._imageFolder + os.sep + '*' + self._xmpExtensionGuess))


    # return True if we have:
    # - at least two raw images
    # - at an xmp file for the first image and one for the last
    # otherwise, return false
    def hasEnoughDataToWork(self):

        moreThanTwoRaws = False
        xmpAtBothEnds = False

        # check number of images
        if(len(self._rawImageList) > 2 ):
            moreThanTwoRaws = True

            # an xmp at both ends (at least)
            if(len(self._xmpBaseList) >= 2 ):

                # fetch the real xmp extention
                self._xmpExtensionActual = Utils.getFileExt(self._xmpBaseList[0])

                # at both ends?
                if( Utils.getBasenameNoExt(self._xmpBaseList[0]) == Utils.getBasenameNoExt(self._rawImageList[0]) \
                    and Utils.getBasenameNoExt(self._xmpBaseList[-1]) == Utils.getBasenameNoExt(self._rawImageList[-1]) ):
                    xmpAtBothEnds = True

        return (moreThanTwoRaws and xmpAtBothEnds)

    # build all the descriptors (but do not interplate them)
    def buildXmpDescriptors(self):

        # create a xmp descriptor for each raw image
        for raw in self._rawImageList:
            xmpFileAddress = self._imageFolder + os.sep + Utils.getBasenameNoExt(raw) + self._xmpExtensionActual

            # find out the original xmp among all
            isInxmpBaseList = (xmpFileAddress in self._xmpBaseList)

            # add a new XmpFileDescriptor to the list
            self._xmpDescriptors.append(XmpFileDescriptor(xmpFileAddress, self._xmpSettingLister))

            # set if it's an original xmp or one to be interpolated
            self._xmpDescriptors[-1].setIsOriginal(isInxmpBaseList)

            # giving the raw extension to make a real name field
            self._xmpDescriptors[-1].setRawImageExtension(self._rawExtension)

            # initialize the inner dictionary of this descriptor
            self._xmpDescriptors[-1].initDictionary()




    def runInterpolation(self):

        # find which xmpFileDescriptor are based on original xmp file
        originalXmpIndexes = []
        counter = 0
        for desc in self._xmpDescriptors:
            if(desc.isOriginalFile()):
                originalXmpIndexes.append(counter)
            counter = counter + 1

        # building a interpolator (will be reused)
        interpolator = XmpFileInterpolator(self._xmpSettingLister)

        for i in range(1, len(originalXmpIndexes)):
            firstPosition = originalXmpIndexes[i-1]
            lastPosition = originalXmpIndexes[i]

            interpolator.setSubList(self._xmpDescriptors[firstPosition : lastPosition+1])
            interpolator.interpolate()



    def printStuff(self):
        for desc in self._xmpDescriptors:
            print str(desc.getFromDictionary("Xmp.crs.CropAngle")) + "\t" + str(desc.isOriginalFile())

    def copyXmpFiles(self):
        None


# main tester
if __name__ == '__main__':

    aRawFileFromTheSequence = "/Users/jonathanlurie/Documents/code/data/NEFpictures/_NIK4337.NEF"

    # not much to do
    xmpMngr = XmpManager()

    # set one image from the sequence, no matter which
    xmpMngr.setRandomImageFromSequence(aRawFileFromTheSequence)

    # parse the sequence folder
    xmpMngr.parseSequenceFolder()

    # checks data integrity
    if(xmpMngr.hasEnoughDataToWork()):

        # builds the descriptor list
        xmpMngr.buildXmpDescriptors()

        # interpolate the empty Descriptors
        xmpMngr.runInterpolation()

        xmpMngr.printStuff()

    else:
        print("ERROR : not enought data to perform interpolation")
