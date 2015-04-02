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
        # part 1 : the basic settings
        #self._interpolateBasicSettings()
        self._interpolateCropSettings()


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

                    # replacing a None by a 0.0 if needed
                    if(firstValue == None):
                        firstValue = 0.0

                    if(lastValue == None):
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

                    # replacing a None by a 0.0 if needed
                    if(firstValue == None):
                        firstValue = 0.0

                    if(lastValue == None):
                        lastValue = 0.0

                    step = (float(lastValue) - float(firstValue) ) / float(len(self._subDescriptorList) - 1.0)

                    # computing the interpolated value
                    interpolValue = firstValue + counter*step

                    # assigning to the Descriptor
                    desc.setToDictionary(setting, interpolValue)

                    if(setting == "Xmp.crs.CropAngle"):
                        print("firstValue : " + str(firstValue))
                        print("lastValue : " + str(lastValue))
                        print("counter : " + str(counter))
                        print("interpolValue : " + str(interpolValue))
                        print("step : " + str(step))

                        print("\n")


                # we do NOT need an interpolation
                else:
                    desc.setToDictionary(setting, firstValue)



                counter = counter + 1


    # interpolation of tone curve related settings
    def _interpolateCurveSettings(self):
        None
