import Tkinter as tkinter
import tkFileDialog
import Tkconstants


class DuskrView:
    _mainWindow = None
    _backgroundImageLabel = None
    _logo = None
    _genericButton = None
    _informationLabel = None
    _firstRawFilename = None

    _xmpManger = None

    def __init__(self, xmpMngr):

        # associating the XmpManager object
        self._xmpManger = xmpMngr

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
        self._informationLabel = tkinter.Label(self._mainWindow, text="\nStep 1\n\nOpen the first raw file of your sequence\n", font=("Helvetica", 14), fg="#777777")
        self._informationLabel.pack()

        self._genericButton = tkinter.Button(self._mainWindow, command=self.openFile, text="Open file")
        self._genericButton.pack()


        # copyright label
        copyrightLbl = tkinter.Label(self._mainWindow, text="github.com/jonathanlurie/duskr", font=("Helvetica", 14), fg="gray")
        copyrightLbl.pack(side="bottom")


        self._mainWindow.mainloop()


    def openFile(self):
        #self._informationLabel.config(text = "hello there")


        self._firstRawFilename = tkFileDialog.askopenfilename()

        print self._firstRawFilename

        # can be restricted to some files
        #filename = tkFileDialog.askopenfilename(filetypes=[("Text files","*.txt"), ("Gif Images", "*.gif")])
        #print(self._firstRawFilename)



        self.displayStep2()



    def displayStep2(self):
        print "here is step 2"
        #fileExtension = self._firstRawFilename

        # label
        self._informationLabel.config(text = "\nStep 2\n\nClick on the GO! button to\nstart the interpolation process\n")

        # button
        self._genericButton.config(command=self.startInterpolation)
        self._genericButton.config(text="Go!")


    def startInterpolation(self):


        # hiding buttons
        self._genericButton.pack_forget()

        # updating the message
        self._informationLabel.config(text = "\nLooking for raw files...\n")

        self._xmpManger.setFirstRawImage(self._firstRawFilename)
        isSuccess = self._xmpManger.processPart1()

        xmpBaseListOk = self._xmpManger.isXmpBaseListOk()



        if(isSuccess and xmpBaseListOk):
            self._informationLabel.config(text = "\n" + str(self._xmpManger.getNumberOfRawFiles()) + " raw files were found.\n\nInterpolation in process...")

            isSuccess2 = self._xmpManger.processPart2()

            if(isSuccess2):
                self._informationLabel.config(font=("Helvetica", 18))
                self._informationLabel.config(fg="#00CC00")
                self._informationLabel.config(text = "\n\nJob is done!\n")

            else:
                self._informationLabel.config(fg="#CC0000")
                self._informationLabel.config(text = "\nERROR\n\nSomething failed [2]\nXmp files do not seem compliant.")

        else:
            if(not isSuccess):
                self._informationLabel.config(fg="#CC0000")
                self._informationLabel.config(text = "\nERROR\n\nSomething failed [1]")

            if(not xmpBaseListOk):
                self._informationLabel.config(fg="#CC0000")
                self._informationLabel.config(text = "\nERROR\n\nThe .xmp file must be present for the first\nand the last raw image.\n\nYou must develop those two images\nwith Adobe CameraRaw first. [3]")
