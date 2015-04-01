# XmpSettingLister will read the setting file to make a list of all the XMP
# settings.
# Those settings are grouped in categories among the setting.ini.
# The categories are maintained within an intance of XmpSettingLister.


from SettingFileReader import *

class XmpSettingLister:

    # contains the basic settings
    _rawDevSettingsBasic = None

    # contains the settings about curves
    _rawDevSettingsCurves = None

    # contains settings about cropping ans rotation
    _rawDevSettingsCrop = None

    # object for reading in a config file
    _settingFileReader = None


    # constructor. Not much to do
    def __init__(self):
        self._rawDevSettingsCrop = SettingFileReader()


    # reads all the settings and store them
    def read(self):

        self._rawDevSettingsBasic = self._rawDevSettingsCrop.getSettings('rawDevSettingsBasic')
        self._rawDevSettingsCurves = self._rawDevSettingsCrop.getSettings('rawDevSettingsCurves')
        self._rawDevSettingsCrop = self._rawDevSettingsCrop.getSettings('rawDevSettingsCrop')


    # returns the list of basics settings
    def getBasicSettingTags(self):
        return self._rawDevSettingsBasic

    # returns the list of curves settings
    def getCurvesSettingTags(self):
        return self._rawDevSettingsCurves

    # returns the list of crop settings
    def getCropSettingTags(self):
        return self._rawDevSettingsCrop


# main tester
if __name__ == '__main__':

    xmpSL = XmpSettingLister()
    xmpSL.read()

    #print xmpSL.getBasicSettingTags()
    #print xmpSL.getCurvesSettingTags()
    print xmpSL.getCropSettingTags()
