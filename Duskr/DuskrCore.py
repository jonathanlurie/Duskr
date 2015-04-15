
import os
import glob
import time
import re

from XmpSettingLister import *
from XmpFileDescriptor import *
from XmpFileInterpolator import *
import Utils

import time
import datetime
#import tracer


class DuskrCore:

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

    _controller = None

    _photoshopAddress = None

    # Constructor
    def __init__(self):

        # create an empty list of XmpFileDescriptor
        self._xmpDescriptors = []

        # construct the setting tag lister , and read() once
        self._xmpSettingLister = XmpSettingLister()
        self._xmpSettingLister.read()


    def setController(self, ctrl):
        self._controller = ctrl


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


    # return the number of raw files
    def getNumberOfRawFiles(self):
        return len(self._rawImageList)

    def parseSequenceFolder(self):
        self._controller.viewUpdateInfoMessage("Looking for raw files...")

        # finding the raw files
        self._rawImageList = sorted(glob.glob(self._imageFolder + os.sep + '*' + self._rawExtension))

        self._controller.viewUpdateInfoMessage("Loking for xmp files...")

        # finding the xmp files
        self._xmpBaseList = sorted(glob.glob(self._imageFolder + os.sep + '*' + self._xmpExtensionGuess))



    # return True if we have:
    # - at least two raw images
    # - at an xmp file for the first image and one for the last
    # otherwise, return false
    def hasEnoughDataToWork(self):

        self._controller.viewUpdateInfoMessage("Checking data consistency...")

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

        # we dont have enough raw files
        if(not moreThanTwoRaws):
            self._controller.viewUpdateInfoMessage("Duskr needs a sequence of raw images", isError=True)
        # we dont have at least 2 xmp files
        elif(not xmpAtBothEnds):
            self._controller.viewUpdateInfoMessage("xmp files must be available\nat least for the first and\nthe last image of the sequence", isError=True)
        # othewise, it's ok
        else:
            self._controller.viewUpdateInfoMessage( str(len(self._rawImageList)) + " raw files were found.\n" + \
                str(len(self._xmpBaseList)) + " xmp files were found.\n\n" + \
                "Press Go!\nto launch the interpolation")

        return (moreThanTwoRaws and xmpAtBothEnds)

    # build all the descriptors (but do not interplate them)
    def buildXmpDescriptors(self):
        self._controller.viewUpdateInfoMessage("Fetching xmp data...")

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



    # performs the interpolation of setting, using checkpoints
    def runInterpolation(self):
        self._controller.viewUpdateInfoMessage("Interpolation running..." )

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

    # writes all xmp file :
    # - copy all xmp file, based on the first one
    # - update settings in each of them
    def writeXmpFiles(self):
        self._controller.viewUpdateInfoMessage("Writing xmp files..." )

        #t0 = datetime.datetime.now()
        for desc in self._xmpDescriptors:
            #os.system('cp "' + self._xmpBaseList[0] + '" "' + desc.getFilename() + '"')
            Utils.copyFile(self._xmpBaseList[0], desc.getFilename())
            desc.writeDictionary()

        #t1 = datetime.datetime.now()
        #delta = t1-t0

        print str(delta.seconds) + "sec " + str(delta.microseconds)

        # it's done, so lets display some finish statement
        self._controller.viewUpdateInfoMessage("Interpolation\nDONE" )

        self._detectPhotoshop()
        if(self._photoshopAddress):
            self._controller.viewDisplayPhotoshopButton()

        self._controller.viewShowQuitButton()



    def printStuff(self):
        for desc in self._xmpDescriptors:
            #print str(desc.getFromDictionary("Xmp.crs.CropTop")) + "\t" + str(desc.isOriginalFile())
            print desc.getFromDictionary("Xmp.crs.CropAngle")
            #print desc.getDictionary()
            #print("\n\n")


    def _detectPhotoshop(self):


        self._photoshopAddress = glob.glob('/Applications/*[pP]hotoshop*.app')
        self._photoshopAddress = self._photoshopAddress + glob.glob('/Applications/*/*[pP]hotoshop*.app')

        #psdGuess.remove("*[Ll]ightroom*")

        # remove lightroom from the list!
        for item in self._photoshopAddress:
            regexp = re.compile(r'[Ll]ightroom')
            if(regexp.search(item)):
                self._photoshopAddress.remove(item)


    # maybe it would be preferable to externalze this method, since it's not xmp stuff...
    def launchPhotoshop(self):
        # if photoshop was found
        if(self._photoshopAddress):
            print("\n[Launching Adobe Photoshop]")
            os.system("open -a '" + self._photoshopAddress[0] + "' " + " ".join(self._rawImageList))




# main tester
if __name__ == '__main__':

    aRawFileFromTheSequence = "/Users/jonathanlurie/Documents/code/data/NEFpictures/_NIK4337.NEF"

    # not much to do
    xmpMngr = DuskrCore()

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

        # write the content into xmp files
        xmpMngr.writeXmpFiles()

        #xmpMngr.printStuff()

    else:
        print("ERROR : not enought data to perform interpolation")
