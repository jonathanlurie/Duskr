# the class DuskrController is one part of the 3-thirds architecture which
# Duskr is made of.
# construct an instance of the DuskrController is enough to run the app.


from DuskrCore import *
from DuskrView import *


class DuskrController:

    # the core, instance of DuskrCore
    _core = None

    # the view, instance of DuskrView
    _view = None


    # constructor, construct the core and the view
    def __init__(self):

        # building the core
        self._core = DuskrCore()
        self._core.setController(self)

        # building the view
        self._view = DuskrView()
        self._view.setController(self)

        self._view.display()


    # call the core method to initialize
    def corePrepareFiles(self, randomRaw):

        # set the first image
        self._core.setRandomImageFromSequence(randomRaw)

        # launch the first part of the process
        self._core.parseSequenceFolder()


    # call core methods to run the interpolation and write xmp files
    def coreLaunchProcess(self):
        # builds the descriptor list
        self._core.buildXmpDescriptors()

        # interpolate the empty Descriptors
        self._core.runInterpolation()

        # write the content into xmp files
        self._core.writeXmpFiles()


    # call core method to check if the opened folder contains enough data
    # to run interpolation
    def coreHasEnoughDataToWork(self):
        return self._core.hasEnoughDataToWork()


    # call view method to update the information message.
    # if isError is True:
    # - the message will start by "ERROR"
    # - will be displayed in red.
    # - the Quit button is shown
    def viewUpdateInfoMessage(self, msg, isError = False):

        print msg
        self._view.updateInfoMessage(msg, isError)

        if(isError):
            self.viewShowQuitButton()


    # calls a view method to show a Quit button
    def viewShowQuitButton(self):
        self._view.showQuitButton()


    def viewDisplayPhotoshopButton(self):
        self._view.displayPhotoshopButton()

    def launchPhotoshop(self):
        self._core.launchPhotoshop()
        print("launch photoshop!!")
