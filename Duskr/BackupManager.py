import Utils
import os
import shutil
import glob

class BackupManager:

    # the working folder, where are located raws and xmp
    _workingFolder = None

    # name of the backup subfolder
    _backupfolderPrefix = None

    def __init__(self, workingFolder):
        self._workingFolder = workingFolder
        self._backupfolder = "backup_"



    # perform a backup of wmp file into a subfolder of the working folder.
    def backupFiles(self, listOfXmp):

        # check if at least one xmp is present in the list
        # (we dont want an empty backup folder)
        xmpArePresent = False

        for xmp in listOfXmp:
            if(os.path.exists(xmp)):
                xmpArePresent = True

        # we dont backup an empty list
        if(not xmpArePresent):
            print("empty list..")
            return

        timestamp = Utils.getTimestamp()

        backupFolder = self._workingFolder + os.sep + self._backupfolder + str(timestamp)

        # creating the fbackup folder
        if not os.path.exists(backupFolder):
            os.makedirs(backupFolder)

        # for each file, copy it
        for f in listOfXmp:
            destFile = backupFolder + os.sep + Utils.getBasenameWithExt(f)
            Utils.copyFile(f, destFile)



    # copy the xmp file from one of the backup subfolder to
    # the regular working folder.
    # backupFolder must be relative (to _workingFolder)
    def restoreBackup(self, backupFolder):
        absBackupFolder = self._workingFolder + os.sep + backupFolder

        # step 0 : check the existance of folder
        if(not os.path.exists(absBackupFolder)):
            raise IOError('backup folder ' + str(absBackupFolder) + " does not exist.")

        # step 1 : erase potential xmp in working folder

        # xmp extension should of course be .xmp, but it's better to do it dynamically
        xmpExtension = Utils.getFileExt(glob.glob(absBackupFolder + os.sep + "*")[0])

        xmpInWorkingFolder = glob.glob(self._workingFolder + os.sep + "*" + xmpExtension)

        # removing all the xmp in the working folder
        for xmp in xmpInWorkingFolder:
            os.remove(xmp)

        # step 2 : restore by copy
        listOfXmpToBackup = glob.glob(absBackupFolder + os.sep + "*" + xmpExtension)

        # for each file in backup folder, copy it
        for f in listOfXmpToBackup:
            destFile = self._workingFolder + os.sep + Utils.getBasenameWithExt(f)
            Utils.copyFile(f, destFile)





    # returns the list of all backup folders present in the working directory
    def getBackupList(self):
        # list of absolute file path, in alphabetical order
        folderAbsList = sorted(glob.glob(self._workingFolder + os.sep + self._backupfolder + "*"))

        relativeList = []

        for folder in folderAbsList:
            relativeList.append(os.path.basename(folder))

        return relativeList


    # among all the backups, restore the most recent one
    def restoreLastBackup(self):
        listOfBackups = self.getBackupList()

        if(len(listOfBackups) > 0):
            self.restoreBackup(listOfBackups[-1])



    # remove the backup subfolder and its content
    def getBackupTuples(self):
        listOfBackups = self.getBackupList()

        listOfTuples = None

        if(len(listOfBackups) > 0):
            listOfTuples = []

            for bck in listOfBackups:
                tuple = (self._workingFolder + os.sep + bck, Utils.getDateFromTimestamp(bck[len(self._backupfolder):]))
                listOfTuples.append(tuple)


        return listOfTuples





if __name__ == '__main__':
    workingFolder = "/Users/jonathanlurie/Documents/code/data/NEFpictures/"

    xmpList = []
    xmpList.append("/Users/jonathanlurie/Documents/code/data/NEFpictures/_NIK4337.xmp")
    xmpList.append("/Users/jonathanlurie/Documents/code/data/NEFpictures/_NIK4341.xmp")
    xmpList.append("/Users/jonathanlurie/Documents/code/data/NEFpictures/_NIK4345.xmp")

    bmgr = BackupManager(workingFolder)

    # backup the files : OK
    #bmgr.backupFiles(xmpList)

    # get the list of backups : OK
    #listOfBackups = bmgr.getBackupList()

    # restore one of the backups
    #bmgr.restoreBackup(listOfBackups[-1])


    # restore the last backup with the built-in function
    #bmgr.restoreLastBackup()

    print bmgr.getBackupTuples()[0][0]
