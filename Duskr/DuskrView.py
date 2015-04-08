import Tkinter as tkinter
import tkFileDialog
import Tkconstants
import time



class DuskrView:
    _mainWindow = None
    _backgroundImageLabel = None
    _logo = None
    _genericButton = None
    _informationLabel = None
    _firstRawFilename = None

    _controller = None

    _infoStringVar = None

    def __init__(self):

        # create a new window
        self._mainWindow = tkinter.Tk()

        # give a title to the window
        self._mainWindow.title("Duskr")

        # set window size
        self._mainWindow.geometry("320x500")
        self._mainWindow.resizable(0, 0)

        # display image on the backfroung
        self._logo = tkinter.PhotoImage(file="images/logo.gif")
        self._backgroundImageLabel = tkinter.Label(self._mainWindow, image=self._logo)
        self._backgroundImageLabel.pack()

        # display step 1
        self._infoStringVar = tkinter.StringVar()
        self._informationLabel = tkinter.Label(self._mainWindow, font=("Helvetica", 14), textvariable=self._infoStringVar)
        self._informationLabel.pack()
        self.updateInfoMessage("Step 1\n\nOpen the first raw file of your sequence")

        self._genericButton = tkinter.Button(self._mainWindow, command=self.openFile, text="Open file")
        self._genericButton.pack()


        # copyright label
        copyrightLbl = tkinter.Label(self._mainWindow, text="github.com/jonathanlurie/duskr", font=("Helvetica", 14), fg="gray")


        copyrightLbl.pack(side="bottom")


    def display(self):
        self._mainWindow.mainloop()


    # set the controller of the MVC architecture
    def setController(self, ctrl):
        self._controller = ctrl


    # show a Quit button.
    # used when process is done or in case of error
    def showQuitButton(self):
        self._genericButton.pack()
        self._genericButton.config(command=self._quit)
        self._genericButton.config(text="Quit")


    # function that actually quit
    def _quit(self):
        print("This is where we quit...")
        self._mainWindow.destroy()


    # update the information message.
    # made to be called by the controller
    def updateInfoMessage(self, msg, isError = False):

        self._refreshWidgets()

        if(isError):
            self._informationLabel.config(fg="#CC0000")
            msg = "\nERROR\n" + msg + "\n"
        else:
            msg = "\n" + msg + "\n"
            self._informationLabel.config(fg="#777777")

        #self._informationLabel.config(text = msg)
        self._infoStringVar.set(msg)


    def _refreshWidgets(self):
        try:

            self._genericButton.update_idletasks()
            self._genericButton.update()
        except:
            None

        self._mainWindow.update_idletasks()
        self._mainWindow.update()

        try:
            self._informationLabel.update_idletasks()
            self._informationLabel.update()
        except:
            None

    # opens a file dialog
    def openFile(self):

        # ********* PART 1 *********
        self._firstRawFilename = tkFileDialog.askopenfilename()

        if(not self._firstRawFilename):
            print("no file selected")
            return

        print self._firstRawFilename

        # can be restricted to some files
        #filename = tkFileDialog.askopenfilename(filetypes=[("Text files","*.txt"), ("Gif Images", "*.gif")])
        #print(self._firstRawFilename)


        # ********* PART 2 *********
        # set the file to the model, and parse the folder.
        # this may take some time...
        self._controller.corePrepareFiles(self._firstRawFilename)

        # check if it"s ok to continue
        if(self._controller.coreHasEnoughDataToWork()):

            # button to launch the interpolation
            self._genericButton.config(command=self.startProcess)
            self._genericButton.config(text="Go!")
            self._refreshWidgets()





    # starting the interpolation and xmp file writing
    def startProcess(self):
        self._genericButton.pack_forget()

        self._refreshWidgets()

        self.updateInfoMessage("Reading files...")

        # hiding buttons

        self._controller.coreLaunchProcess()

    def displayPhotoshopButton(self):
        psdButton = tkinter.Button(self._mainWindow, command=self._controller.launchPhotoshop, text="Open in Photoshop")
        psdButton.pack()
