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
        # TODO : create a backup!
        # (check was performed before, we reach this point only if data are ok)

        self._core.mainProcess


    # call core method to check if the opened folder contains enough data
    # to run interpolation
    def coreAreDataOK(self):

        # check if there is too many xmp files (one per raw)
        # which is not good
        hasTooMany = self._core.hasTooManyXmp()

        # check if we have enough xmp files
        hasEnough = self._core.hasEnoughDataToWork()

        # we have too many xmp : not good
        if(hasTooMany):
            self.isBackupPossible() # might be asked by the view afterwards
            self.proposeBackup()# might be asked by the view afterwards
            self._controller.viewUpdateInfoMessage("There is too many xmp files.\n")

        # we dont have too many xmp : might be good
        else:

            # we have just enough xmp : good
            if(hasEnough):
                self.viewUpdateInfoMessage( str(self._core.getNumberOfRawFiles()) + " raw files were found.\n" + \
                    str(len(self._core.getNumberOfXmpFiles())) + " xmp files were found.\n\n" + \
                    "Press Go!\nto launch the interpolation")

            # not enough xmp : not good
            else:
                self.isBackupPossible()# might be asked by the view afterwards
                self.proposeBackup()# might be asked by the view afterwards
                self._controller.viewUpdateInfoMessage("xmp files must be available\nat least for the first and\nthe last image of the sequence", isError=True)

        return [hasEnough, hasTooMany]


    # TODO : return if a backup is present and able to be used
    def _isRestoreBackupPossible(self):
        None

    # TODO : ask (through view) to restore a backup
    def _proposeRestoreBackup(self):
        None

    # TODO : ask the core to perform a restoration from backup
    def coreRestore(self):

        None


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
