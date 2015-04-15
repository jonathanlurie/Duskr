import Tkinter as tkinter
import tkFileDialog
import Tkconstants
import time
import Utils
import webbrowser
from _version import __version__


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
        copyrightLbl = tkinter.Label(self._mainWindow, text="github.com/jonathanlurie/duskr", font=("Helvetica", 14), fg="gray", cursor="hand2")
        copyrightLbl.bind("<Button-1>", self.openUrl)
        copyrightLbl.pack(side="bottom")


        self._addMenu()





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





    def _addMenu(self):
        menubar = tkinter.Menu(self._mainWindow)

        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self._displayAboutWindow)
        helpmenu.add_command(label="Help", command=self._displayHelpWindow)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self._mainWindow.config(menu=menubar)

    def _displayAboutWindow(self):
        print "displaying the About window"
        print "displaying the Help window"
        content = Utils.loadTextFile("text/about.txt") + "\n\nVersion : " + __version__

        self._displayGenericTextWindow(content, "About")

    def _displayHelpWindow(self):
        print "displaying the Help window"
        content = Utils.loadTextFile("text/help.txt")
        self._displayGenericTextWindow(content, "Help")


    def _displayGenericTextWindow(self, content, title):
        # example taken at
        # http://www.python-course.eu/tkinter_text_widget.php


        # create a new window
        genericWindow = tkinter.Toplevel()

        # give a title to the window
        genericWindow.title(title)

        # set window size
        genericWindow.geometry("800x400")
        genericWindow.resizable(0, 0)

        # creating left pane, with an image
        leftPane = tkinter.Text(genericWindow, height=20, width=40)

        photo = tkinter.PhotoImage(file='images/logo.gif')
        leftPane.insert(tkinter.END,'\n')
        leftPane.config(takefocus=False)
        leftPane.image_create(tkinter.END, image=photo)
        leftPane.config(state=tkinter.DISABLED)
        leftPane.pack(side=tkinter.LEFT)


        # creating right pane, scrollabale
        rightPane = tkinter.Text(genericWindow, height=20, width=65)

        scroll = tkinter.Scrollbar(genericWindow, command=rightPane.yview)
        rightPane.configure(yscrollcommand=scroll.set)
        rightPane.configure(wrap="word")

        # defining some styles
        rightPane.tag_configure('bold_italics', font=('Helvetica', 12, 'bold', 'italic'))
        rightPane.tag_configure('big', foreground='#BBBBBB', font=('Helvetica', 40, 'bold'))
        rightPane.tag_configure('regular', foreground='#555555', font=('Helvetica', 14))
        rightPane.tag_bind('follow', '<1>', lambda e, t=rightPane: t.insert(tkinter.END, "Not now, maybe later!"))
        rightPane.insert(tkinter.END, str(title) + '\n', 'big')

        # adding content
        rightPane.insert(tkinter.END, "\n" + content, 'regular')

        rightPane.config(state=tkinter.DISABLED)

        # packing
        rightPane.pack(side=tkinter.LEFT)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)



        # opening the window
        genericWindow.mainloop()


    def openUrl(self, event):
        webbrowser.open_new(r"http://www.github.com/jonathanlurie/duskr")
