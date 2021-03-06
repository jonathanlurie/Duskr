'''
Durskr
=============
Copyright (c) 2015, Jonathan LURIE, All rights reserved.
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library.
'''

import os
import glob
import re
import fnmatch
import time

from SettingFileReader import *

import tracer

from subprocess import call

class XmpManagerV1:

    # contains the xmp file address of the first and the last
    _xmpBaseList = None

    # contains the file adress of all the raw files
    _rawImageList = None

    # is a 2D dictionary, over xmp files and settings
    _xmpDictionary = None

    # where all the images and xmp files are (or will be)
    _imageFolder = None

    # image developement setting names
    _settingCouples = None

    # the regex for finding a setting in the xmp file
    _settingRegexPattern = '="([-+]?\d*[.]?\d+)"'

    _xmpExtension = ".xmp"

    _rawExtension = None

    # used to conserve an orinal xmp file aside
    _xmpMatrixFileName = "xmpMatrix.xmp"



    def __init__(self):
        self._xmpBaseList = []
        self._xmpDictionary = {}
        self._settingCouples = []
        settings = SettingFileReader()
        self._settingCouples = settings.getItems('rawDevSettings')

        print self._settingCouples

        exit()


    # The folder conains raw images
    def setFirstRawImage(self, FirstRawImage):
        # guessing the raw extension from the first image
        self._rawExtension = os.path.splitext(os.path.basename(FirstRawImage))[1]

        # guessing the input folder from the first image
        self._imageFolder = os.path.dirname(FirstRawImage)

        self._xmpMatrixFileName =  self._imageFolder + os.sep + self._xmpMatrixFileName

    # used for moitoring
    def getNumberOfRawFiles(self):
        return len(self._rawImageList)


    # the xmp list is ok if the first xmp hase the same name as the first raw
    # idem for the last
    def isXmpBaseListOk(self):

        firstOk = os.path.splitext(os.path.basename(self._rawImageList[0]))[0] == os.path.splitext(os.path.basename(self._xmpBaseList[0]))[0]
        lastOk = os.path.splitext(os.path.basename(self._rawImageList[-1]))[0] == os.path.splitext(os.path.basename(self._xmpBaseList[-1]))[0]

        return (firstOk and lastOk)

    # parse the image folder, meaning:
    # read what extension should be considered for image raw files
    # make the list of raw files
    # make the short list of xmp files
    # build the xmp disctionary on the flow
    def _parseFolder(self):

        # finding the raw files
        self._rawImageList = sorted(glob.glob(self._imageFolder + os.sep + '*' + self._rawExtension))

        # finding the xmp files
        self._xmpBaseList = sorted(glob.glob(self._imageFolder + os.sep + '*' + self._xmpExtension))


        # build the xmp dictionnary
        for img in self._rawImageList:

            nameNoExtension = os.path.splitext(os.path.basename(img))[0]
            #print nameNoExtension
            self._xmpDictionary[nameNoExtension] = {}

            # completion of the dictionnay with setting names
            for rawSettingCouple in self._settingCouples:
                self._xmpDictionary[nameNoExtension][rawSettingCouple[1]] = None


    # fill the 1st and last occurence, the one for which we have the xmp files
    def _fillDictionnary(self):
        # parse the original xmp list
        for baseXmp in self._xmpBaseList :

            nameNoExtension = os.path.splitext(os.path.basename(baseXmp))[0]

            # open (read) the xmp file
            with open(baseXmp, "rt") as xmpIn:

                # read line by line
                for line in xmpIn:

                    # we are looking for all kind of settings (crs:saturation, etc.)
                    for setting in self._settingCouples:
                        #print stempRegex
                        tempRegex = setting[1] + self._settingRegexPattern
                        regexResult = re.search(tempRegex, line)

                        if(regexResult):
                            #print regexResult.group(1)
                            self._xmpDictionary[nameNoExtension][setting[1]] = float(regexResult.group(1))

    # Fill the None values of the dictionaty by interpolation
    # between the first and the last
    # TODO : expand this finctionality to intermediate settings
    def _interpolateDictionary(self):
        numberOfSamples = len(self._xmpDictionary)

        # we are looking for all kind of settings (crs:saturation, etc.)
        for setting in self._settingCouples:

            # save the first and last for later
            firstValue = sorted(self._xmpDictionary.items())[0][1][setting[1]]
            lastValue = sorted(self._xmpDictionary.items())[-1][1][setting[1]]

            # a boolean to check if an interpolation is needed
            needInterpolation = (firstValue != lastValue)
            imageIterator = 0

            # parsing the dict over file names
            for xmp in sorted(self._xmpDictionary.items()):

                #default case
                newValue = firstValue

                if(needInterpolation):
                    newValue = self._interpolate(firstValue, lastValue, numberOfSamples, imageIterator)

                xmp[1][setting[1]] = newValue
                imageIterator = imageIterator + 1


    # Fill the None values of the dictionaty by interpolation
    # between the first and the last

    def _interpolateDictionary2(self):


        sortedDict = sorted(self._xmpDictionary.items())


        # we are looking for all kind of settings (crs:saturation, etc.)
        for settingCouple in self._settingCouples:

            settingName = settingCouple[1]

            # for which raw file is there an xmp?
            # at least the first and the last...
            xmpPositions = []

            # finding xmp positions
            counter = 0
            for xmp in sortedDict:
                if(xmp[1][settingName]):
                    xmpPositions.append(counter)

                counter = counter + 1


            # loop over the xmp positions.
            # starting from the second because we are intrepolation
            # between i-1 and i
            for i in range(1, len(xmpPositions)):

                self._interpolateSubpartDictionary(settingName, xmpPositions[i-1], xmpPositions[i])

        for img in sortedDict:
            print img


    # extrapolate values of the dictionary. Works for more than 2 xmp files
    def _interpolateSubpartDictionary(self, setting, start, end):
        sortedDict = sorted(self._xmpDictionary.items())

        startValue = sortedDict[start][1][setting]
        endValue = sortedDict[end][1][setting]

        needInterpolation = (startValue != endValue)

        numberOfSamples = end - start + 1
        counter = 0

        # computing inter values.
        for i in range(start, end):

            #default case
            newValue = startValue

            if(needInterpolation):
                newValue = self._interpolate(startValue, endValue, numberOfSamples, counter)

            sortedDict[i][1][setting] = newValue
            counter = counter + 1


    # Linear interpolation of values.
    # gives the value at outputSamplePosition
    def _interpolate(self, firstValue, lastValue, totalNumberOfSamples, outputSamplePosition):

        rangeOfData = lastValue - firstValue
        step = rangeOfData / ( totalNumberOfSamples - 1 )
        outputValue = firstValue + ( outputSamplePosition * step )

        # we do not want tons of decimal here
        return round(outputValue, 2)


    # loop the dictionnary in order to write an xmp file for each page.
    # relies mainly on _writeXmpFile() though.
    def _writeAllXmp(self):
        # conserve an original xmp file aside
        #os.system('rsync -ptgo -A -X "' + self._xmpBaseList[0] + '" "' + self._xmpMatrixFileName + '"')
        os.system('cp "' + self._xmpBaseList[0] + '" "' + self._xmpMatrixFileName + '"')
        #call(["rsync", "-ptgo", "-A", "-X", self._xmpBaseList[0], self._xmpMatrixFileName])


        for xmp in sorted(self._xmpDictionary.items()):
            self._writeXmpFile(xmp)


    # copy an xmp file and replace the fields by the one from xmpOccurence.
    # xmpOccurence is basically "one page of" the _xmpDictionary
    def _writeXmpFile(self, xmpOccurence):

        baseNameNoExt = xmpOccurence[0]

        # for replacing the name or the image itself in the output xmp file
        xmpOriginalFileBasenameNoExt = os.path.splitext(os.path.basename(self._xmpMatrixFileName))[0]

        # output xmp file
        xmpFileOutput = self._imageFolder + os.sep + baseNameNoExt + self._xmpExtension

        # copy an original file rather than creating from scratch,
        # it will keep the xattr that we need
        #os.system('rsync -ptgo -A -X "' + self._xmpMatrixFileName + '" "' + xmpFileOutput + '"')
        os.system('cp "' + self._xmpMatrixFileName + '" "' + xmpFileOutput + '"')
        open(xmpFileOutput, 'w').close()


        # line by line, we read and write on the flow
        #with open(xmpFileOutput, "wt") as fout:
        fout = open(xmpFileOutput,'w')

        with open(self._xmpMatrixFileName, "rt") as fin:

            for line in fin:
                outputLine = line
                patternFound = False

                # we are looking for all kind of settings (crs:saturation, etc.)
                for setting in self._settingCouples:

                    #print stempRegex
                    tempRegex = setting[1] + self._settingRegexPattern
                    regexResult = re.search(tempRegex, line)

                    if(regexResult):
                        interpolatedValue = xmpOccurence[1][setting[1]]
                        outputLine = setting[1] + '="' + str(interpolatedValue) + '"\n'

                        # no need to look for another pattern on this line
                        break

                # replace the image name within the xmp, if found (line by line)
                outputLine = outputLine.replace(xmpOriginalFileBasenameNoExt, baseNameNoExt)

                # writing a line in the output file
                fout.write(outputLine)
        fout.close()

    # just a call of processPart1 and part2
    def process(self):
        self.processPart1()
        self.processPart2()


    def processPart1(self):
        isSuccess = False
        try:
            # process
            print("[Start processing]")
            print("\tBrowsing input folder...")
            self._parseFolder()

            isSuccess = True
        except:
            None

        return isSuccess

    def processPart2(self):
        isSuccess = False

        #try:
        print("\tFilling the dictionary...")
        self._fillDictionnary()

        print "-----------------------"



        print("\tLinear interpolation...")
        self._interpolateDictionary2()





        print("\tXmp file writing...")
        self._writeAllXmp()

        self._finish()

        isSuccess = True

        self._launchPhotoshop()
        #except:
        #None



        return isSuccess


    # look for photoshop on the computer, if found, lauched.
    def _launchPhotoshop(self):
        psdGuess = glob.glob('/Applications/*[pP]hotoshop*.app')
        psdGuess = psdGuess + glob.glob('/Applications/*/*[pP]hotoshop*.app')

        #psdGuess.remove("*[Ll]ightroom*")

        # remove lightroom from the list!
        for item in psdGuess:
            regexp = re.compile(r'[Ll]ightroom')
            if(regexp.search(item)):
                psdGuess.remove(item)


        # if photoshop was found
        if(psdGuess):
            print("\n[Launching Adobe Photoshop]")
            os.system("open -a '" + psdGuess[0] + "' " + " ".join(self._rawImageList))



    def _finish(self):
        # remove the xmp matrix
        os.remove(self._xmpMatrixFileName)
