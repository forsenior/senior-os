import tkinter
from tkinter import *
import tkinter.font as font



class DesktopFrame:
    def __init__(self, masterFrame):
        self.options1Button = None
        self.backButton = None
        self.menuButton = None
        self.masterFrame = masterFrame

        __fontSize = font.Font(family='Halvetica', size=36, weight=font.BOLD)
        def menuClicked(): #schová "MENU" a ukáže "BACK"
            print("menuClicked")
            self.menuButton.pack_forget()
            self.options1Button.pack(side=LEFT)
            self.backButton.pack()

        def backClicked():#reverse oproti menuClicked()
            print("backClicked")
            self.menuButton.pack()
            self.options1Button.pack_forget()
            self.backButton.pack_forget()

        def createMenuButtons(fontSize):
            print("we craftin menu")
            self.menuButton = tkinter.Button(menuBar, text="MENU", width=int(masterFrame.winfo_screenwidth() / 6),height=int(masterFrame.winfo_screenwidth() / 6), command=menuClicked)
            self.menuButton['font']= fontSize
            self.menuButton.pack()
            self.backButton = tkinter.Button(menuBar, text="BACK", width=int(masterFrame.winfo_screenwidth() / 6),height=int(masterFrame.winfo_screenheight() / 6), command=backClicked)
            self.backButton['font'] = fontSize

        def createExitButton(fontSize):
            print("we craftin exit")
            exitButtonPokus = tkinter.Button(exitBar, text="EXIT", width=int(masterFrame.winfo_screenwidth() / 6),height=int(masterFrame.winfo_screenheight() / 6),command=self.masterFrame.destroy)
            exitButtonPokus['font'] = fontSize
            exitButtonPokus.pack()

        def createOptionsButtons():
            print("we craftin options")
            self.options1Button = tkinter.Button(optionsBar, text="OPTIONS_1",height=int(masterFrame.winfo_screenheight() / 6))



        # Main frame
        masterBar = Frame(masterFrame, height=int(masterFrame.winfo_screenheight() / 6))
        masterBar.pack_propagate(False)  # zakazuje, aby se velikost baru fixne scaloval podle velikosti tlacitka
        masterBar.pack(side=TOP, fill=X)

        # sekce pro menu
        menuBar = Frame(masterBar, width=int(masterFrame.winfo_screenwidth() / 6))
        menuBar.pack_propagate(False)
        menuBar.pack(side=LEFT, fill=Y)

        # sekce pro exit
        exitBar = Frame(masterBar, width=int(masterFrame.winfo_screenwidth() / 6))
        exitBar.pack_propagate(False)
        exitBar.pack(side=RIGHT, fill=Y)

        # sekce pro options
        optionsBar = Frame(masterBar, bg='YELLOW')  # pak dat barvu pryč
        optionsBar.pack_propagate(False)
        optionsBar.pack(expand=True, fill=BOTH)

        #volání defů pro tlačítka
        createMenuButtons(__fontSize)
        createOptionsButtons()
        createExitButton(__fontSize)
class App:
    def __init__(self, masterWindow):
        self.masterWindow = masterWindow
        masterWindow.title("for senior")

        screen_width = masterWindow.winfo_screenwidth()
        screen_height = masterWindow.winfo_screenheight()
        res = "{a}x{b}".format(a=int(screen_width), b=int(screen_height))

        masterWindow.geometry(res)
        masterWindow.overrideredirect(True)



if __name__ == '__main__':
    root = Tk()
    my_gui = App(root)
    idk = DesktopFrame(root)
    root.mainloop()