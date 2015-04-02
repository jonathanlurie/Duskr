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
        self._interpolateBasicSettings()


    # interpolation of basic settings only
    def _interpolateBasicSettings(self):

        # for each setting
        for setting in self._xmpSettingLister.getBasicSettingTags():

            # check if we do need an interpolation of if a value-copy is enough
            firstValue = self._subDescriptorList[0].getFromDictionary(setting)
            lastValue = self._subDescriptorList[-1].getFromDictionary(setting)
            needsInterpolation = (firstValue != lastValue and firstValue and lastValue)

            # the necessary to interpolate
            counter = 0

            # for each Descriptor of the sublist
            for desc in self._subDescriptorList:

                # we DO need an interpolation
                if(needsInterpolation):

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
            None


        # interpolation of tone curve related settings
        def _interpolateCurveSettings(self):
            None
