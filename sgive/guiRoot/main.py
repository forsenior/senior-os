import tkinter
from tkinter import *
import tkinter.font as font
import json
"""
Written by: RYUseless, BPC-IBE
"""

def screenResMath(tk):
    print("Pocitanicko")
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    res = "{a}x{b}".format(a=int(screen_width), b=int(screen_height))
    return [res,int(screen_width/6),int(screen_height/6)]#fullRes->0    width/6->1  Height/6->2
class JsonActions():
    def __init__(self,resolution,appResolution,font,size,weight):
        self.resolution = resolution
        self.appResolution = appResolution
        self.font = font
        self.size = size
        self.weight = weight

        dictionary = {
            "screenResolution": resolution,
            "appResolution" : appResolution,
            "fontName": font,
            "fontSize": size,
            "fontWeight": weight
        }

        json_object = json.dumps(dictionary, indent=4)

        with open("CoolEpicName.json", "w") as outfile:
            outfile.write(json_object)
class MenuFrame:
    def __init__(self, masterFrame):
        self.browserButton = None
        self.emailButton = None
        self.backButton = None
        self.menuButton = None
        self.masterFrame = masterFrame
        self.fontSize = font.Font(family='Halvetica', size=36, weight=font.BOLD)
        sixWidth =  screenResMath(masterFrame)[1]
        sixHeight = screenResMath(masterFrame)[2]

        def menuClicked(): #schová "MENU" a ukáže "BACK"
            print("menuClicked")
            self.menuButton.pack_forget()
            self.emailButton.pack(side=LEFT)
            self.browserButton.pack(side=LEFT)
            self.backButton.pack()

        def backClicked():#reverse oproti menuClicked()
            print("backClicked")
            self.menuButton.pack()
            self.emailButton.pack_forget()
            self.browserButton.pack_forget()
            self.backButton.pack_forget()

        def createMenuButtons(fontSize):
            print("we craftin menu")
            self.menuButton = tkinter.Button(menuBar, text="MENU", command=menuClicked)
            self.menuButton['width'] = sixWidth
            self.menuButton['height']= sixHeight
            self.menuButton['font']= fontSize
            self.menuButton.pack()
            self.backButton = tkinter.Button(menuBar, text="BACK", command=backClicked)
            self.backButton['width'] = sixWidth
            self.backButton['height'] = sixHeight
            self.backButton['font'] = fontSize

        def createExitButton(fontSize):
            print("we craftin exit")
            exitButtonPokus = tkinter.Button(exitBar, text="EXIT",command=self.masterFrame.destroy)
            exitButtonPokus['width'] = sixWidth
            exitButtonPokus['height']= sixHeight
            exitButtonPokus['font'] = fontSize
            exitButtonPokus.pack()

        def createOptionsButtons(fontSize):
            print("we craftin options")
            self.emailButton = tkinter.Button(optionsBar, text="EMAIL",command=lambda : print("email"))
            self.emailButton['height']= sixHeight
            self.emailButton['font'] = fontSize
            self.browserButton = tkinter.Button(optionsBar, text="BROWSER",command=lambda : print("browser"))
            self.browserButton['height']= sixHeight
            self.browserButton['font'] = fontSize

        # Main frame
        masterBar = Frame(masterFrame, height=sixHeight)
        masterBar.pack_propagate(False)  # zakazuje, aby se velikost baru fixne scaloval podle velikosti tlacitka
        masterBar.pack(side=TOP, fill=X)

        # sekce pro menu
        menuBar = Frame(masterBar, width=sixWidth)
        menuBar.pack_propagate(False)
        menuBar.pack(side=LEFT, fill=Y)

        # sekce pro exit
        exitBar = Frame(masterBar, width=sixWidth)
        exitBar.pack_propagate(False)
        exitBar.pack(side=RIGHT, fill=Y)

        # sekce pro options
        optionsBar = Frame(masterBar, bg='YELLOW') #až přijdeš čas, vrátit na bílou/černou barvu
        optionsBar.pack_propagate(False)
        optionsBar.pack(expand=True, fill=BOTH)

        #volání defů pro tlačítka
        createMenuButtons(self.fontSize)
        createOptionsButtons(self.fontSize)
        createExitButton(self.fontSize)

    def font(self):
        return self.fontSize

class ApplicationsFrame:
    def __init__(self, applicationsFrame):
        self.applicationsFrame = applicationsFrame

        print("app frame")
        heighNum = int(applicationsFrame.winfo_screenheight()-(applicationsFrame.winfo_screenheight()/6))
        applicationFrame = Frame(applicationsFrame,height=heighNum,bg="#bababa")
        applicationFrame.pack_propagate(False)
        applicationFrame.pack(fill=X)

        self.valueHeight = heighNum
        self.valueWidth = applicationFrame.winfo_screenwidth()
    def __str__(self):
        return f"{self.valueWidth}x{self.valueHeight}"
class App:
    def __init__(self, masterWindow):
        self.masterWindow = masterWindow
        masterWindow.title("for senior")
        masterWindow.attributes('-fullscreen', True)

if __name__ == '__main__':
    root = Tk()
    my_gui = App(root)
    menuframe = MenuFrame(root)
    appframe = ApplicationsFrame(root)
    pokusValue = menuframe.font()
    pokusJson = JsonActions(screenResMath(root)[0],str(appframe), pokusValue.cget('family'), pokusValue.cget('size'), pokusValue.cget('weight'))

    root.mainloop()