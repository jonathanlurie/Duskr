# XmpFileInterpolator intends to interpolate a (sub)list of XmpFileDescriptor instances.
# This (sub)list starts and ends by data based on a real xmp file, all the intermediates
# are data to be interpolated.
# Interpolation is linear (for now).


from XmpSettingLister import *
from XmpFileDescriptor import *
import Utils

class XmpFileInterpolator:

    # the sub list of XmpFileDescriptor instances
    _subDescriptorList = None

    # an instance of XmpSettingLister that has been read() already.
    # Gives access to all the settings tags
    _xmpSettingLister = None



    # constructor
    # just about getting the lists of tags through an XmpSettingLister
    def __init__(self, xmpStListr):
        self._xmpSettingLister =xmpStListr

    # set the sublist to be interpolated
    def setSubList(self, slist):
        self._subDescriptorList = slist


    # launch interpolation
    def interpolate(self):
        self._interpolateBasicSettings()
        self._interpolateCropSettings()
        self._interpolateCurveSettings()


    # interpolation of basic settings only
    def _interpolateBasicSettings(self):

        # for each BASIC setting
        for setting in self._xmpSettingLister.getBasicSettingTags():

            # check if we do need an interpolation of if a value-copy is enough
            firstValue = self._subDescriptorList[0].getFromDictionary(setting)
            lastValue = self._subDescriptorList[-1].getFromDictionary(setting)
            needsInterpolation = (firstValue != lastValue and (firstValue or lastValue))





            # the necessary to interpolate
            counter = 0

            # for each Descriptor of the sublist
            for desc in self._subDescriptorList:

                # we DO need an interpolation
                if(needsInterpolation):

                    # if it's a string, we dont interpolate, just copy it
                    if(type(firstValue) == type('') or type(lastValue) == type('')):
                        desc.setToDictionary(setting, firstValue)
                        continue

                    # replacing a None by a 0.0 if needed
                    if(firstValue == None):
                        firstValue = 0.0
                        #firstValue = lastValue  # safer like that, even though the following is bit useless

                    if(lastValue == None):
                        lastValue = 0.0
                        #lastValue = firstValue  # safer like that, even though the following is bit useless

                    step = (float(lastValue) - float(firstValue) ) / float(len(self._subDescriptorList) - 1.0)

                    # computing the interpolated value
                    interpolValue = firstValue + counter*step

                    # assigning to the Descriptor
                    desc.setToDictionary(setting, interpolValue)

                # we do NOT need an interpolation
                else:
                    desc.setToDictionary(setting, firstValue)

                counter = counter + 1


    # interpolation of croping related settings
    def _interpolateCropSettings(self):

        hasCropTag = "Xmp.crs.HasCrop"

        # check if needed
        hasCrop1 = self._subDescriptorList[0].getFromDictionary(hasCropTag)
        hasCrop2 = self._subDescriptorList[-1].getFromDictionary(hasCropTag)

        # disorder in croping settings
        if( (hasCrop1 == "False" or hasCrop1 == None) and hasCrop2 == "True"):
            self._subDescriptorList[0].setToDictionary(hasCropTag, "True")
        elif(  (hasCrop2 == "False" or hasCrop2 == None ) and hasCrop1 == "True"):
            self._subDescriptorList[-1].setToDictionary(hasCropTag, "True")
        elif( (hasCrop1 == "False" or hasCrop1 == None) and (hasCrop2 == "False" or hasCrop2 == None ) ):
            return


        # updates Xmp.crs.CropConstrainToWarp if None (first)
        if(self._subDescriptorList[0].getFromDictionary("Xmp.crs.CropConstrainToWarp") == None and \
            self._subDescriptorList[-1].getFromDictionary("Xmp.crs.CropConstrainToWarp") != None ):

            self._subDescriptorList[0].setToDictionary("Xmp.crs.CropConstrainToWarp", self._subDescriptorList[-1].getFromDictionary("Xmp.crs.CropConstrainToWarp"))


        # updates Xmp.crs.CropConstrainToWarp if None (last)
        if(self._subDescriptorList[-1].getFromDictionary("Xmp.crs.CropConstrainToWarp") == None and \
            self._subDescriptorList[0].getFromDictionary("Xmp.crs.CropConstrainToWarp") != None ):

            self._subDescriptorList[-1].setToDictionary("Xmp.crs.CropConstrainToWarp", self._subDescriptorList[0].getFromDictionary("Xmp.crs.CropConstrainToWarp"))



        # for each CROP setting
        for setting in self._xmpSettingLister.getCropSettingTags():

            # check if we do need an interpolation of if a value-copy is enough
            firstValue = self._subDescriptorList[0].getFromDictionary(setting)
            lastValue = self._subDescriptorList[-1].getFromDictionary(setting)
            needsInterpolation = (firstValue != lastValue and (firstValue or lastValue))




            # the necessary to interpolate
            counter = 0

            # for each Descriptor of the sublist
            for desc in self._subDescriptorList:

                # we DO need an interpolation
                if(needsInterpolation):

                    # replacing a None by a 0.0 or 1.0 if needed
                    if(firstValue == None):
                        if(setting == "Xmp.crs.CropRight" or setting == "Xmp.crs.CropBottom"):
                            firstValue = 1.0
                        else:
                            firstValue = 0.0

                    if(lastValue == None):
                        if(setting == "Xmp.crs.CropRight" or setting == "Xmp.crs.CropBottom"):
                            lastValue = 1.0
                        else:
                            lastValue = 0.0

                    step = (float(lastValue) - float(firstValue) ) / float(len(self._subDescriptorList) - 1.0)

                    # computing the interpolated value
                    interpolValue = firstValue + counter*step

                    # assigning to the Descriptor
                    desc.setToDictionary(setting, interpolValue)


                # we do NOT need an interpolation
                else:
                    desc.setToDictionary(setting, firstValue)



                counter = counter + 1


    # a default curve is NOT an empty curve.
    # a default cuves starts at (0, 0) and ends at (255, 255)
    def _isDefaultCurve(self, curve):
        isDefault = False

        if(len(curve) == 4):
            if(int(curve[0]) == 0 and int(curve[1]) == 0 and int(curve[2]) == 255 and int(curve[3]) == 255):
                isDefault = True

        return isDefault



    # interpolation of tone curve related settings
    def _interpolateCurveSettings(self):


        # we compare first/last consistency and correct it
        for setting in self._xmpSettingLister.getCurvesSettingTags():

            # check if we do need an interpolation of if a value-copy is enough
            firstValue = self._subDescriptorList[0].getFromDictionary(setting)
            lastValue = self._subDescriptorList[-1].getFromDictionary(setting)

            # check if it was set...

            # both are set
            if(firstValue and lastValue):

                # Not the same size but one is default (last)
                if(not self._isDefaultCurve(firstValue) and self._isDefaultCurve(lastValue)):
                    blankCurve = self._generateBlankCurve(firstValue)
                    self._subDescriptorList[-1].setToDictionary(setting, blankCurve)

                # Not the same size but one is default (last) (first)
                elif(self._isDefaultCurve(firstValue) and not self._isDefaultCurve(lastValue)):
                    blankCurve = self._generateBlankCurve(lastValue)
                    self._subDescriptorList[0].setToDictionary(setting, blankCurve)

                # Not the same size and none is default
                # and they dont have the same size
                elif(not self._isDefaultCurve(firstValue) and not self._isDefaultCurve(lastValue) and \
                    len(firstValue) != len(lastValue)):
                    # TODO : implement a interpolation using cubic spline, see
                    # http://blog.ivank.net/interpolation-with-cubic-splines.html
                    # or
                    # https://docs.scipy.org/doc/scipy-0.15.1/reference/tutorial/interpolate.html

                    None

            # NOT SUPPOSED TO HAPPEN
            # the first is set but not the second.
            # we create an artificial blank curve as the last one
            elif(firstValue and not lastValue):
                blankCurve = self._generateBlankCurve(firstValue)
                self._subDescriptorList[-1].setToDictionary(setting, blankCurve)


            # NOT SUPPOSED TO HAPPEN
            # the second is set but not the first
            # we create an artificial blank curve as the first one
            elif(not firstValue and lastValue):
                blankCurve = self._generateBlankCurve(lastValue)
                self._subDescriptorList[0].setToDictionary(setting, blankCurve)


            # both are None, no interpolation to be done
            else:
                None



        # actual interpolation
        for setting in self._xmpSettingLister.getCurvesSettingTags():

            # check if we do need an interpolation of if a value-copy is enough
            firstValue = self._subDescriptorList[0].getFromDictionary(setting)
            lastValue = self._subDescriptorList[-1].getFromDictionary(setting)

            # check if it was set...

            # both are set
            if(firstValue and lastValue):

                # both have the same number of couple
                if(len(firstValue) == len(lastValue) ):

                    # the necessary to interpolate
                    counter = 0

                    # for each descriptor
                    for desc in self._subDescriptorList:

                        # the list of coordinates
                        coords = []

                        # for each coordinate
                        for coord in range(0, len(firstValue)):

                            # re-computing the step
                            step = (float(lastValue[coord]) - float(firstValue[coord]) ) / float(len(self._subDescriptorList) - 1.0)
                            interpolatedValue = float(firstValue[coord]) + counter * step
                            coords.append(int(interpolatedValue))

                        # setting the list of coordinates as a curve
                        desc.setToDictionary(setting, coords)

                        counter = counter + 1

                # TODO : cubic spline needs to be implemented
                else:
                    None

            # both are None, noe interpolation to be done
            else:
                None



    # generates a straight "curve", starting from 0,0 and ending at 255, 255
    # with the same number of points in-between
    def _generateBlankCurve(self, baseCurve):
        numberOfCouples = len(baseCurve)/2

        # create it ith the firstPoint
        blankCurve = []
        blankCurve.append(0)
        blankCurve.append(0)

        for i in range(1, numberOfCouples - 1):
            # for x
            blankCurve.append(baseCurve[i*2])

            # for y
            blankCurve.append(baseCurve[i*2])

        # adding the last point
        blankCurve.append(255)
        blankCurve.append(255)

        return blankCurve


            #needsInterpolation = (firstValue != lastValue and (firstValue or lastValue))
