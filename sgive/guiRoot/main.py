import tkinter
from tkinter import *
import tkinter.font as font
import json

class JsonActions():
    def __init__(self,resolution,font,size,weight):
        self.resolution = resolution
        self.font = font
        self.size = size
        self.weight = weight

        print("\n")
        print("res:",resolution)
        print("font:",font)
        print("size:",size)
        print("weight:",weight)
        print("\n")

        dictionary = {
            "screenResolution": resolution,
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

        __fontSize = font.Font(family='Halvetica', size=36, weight=font.BOLD)

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
            self.menuButton['width'] = int(masterFrame.winfo_screenwidth() / 6)
            self.menuButton['height']= int(masterFrame.winfo_screenwidth() / 6)
            self.menuButton['font']= fontSize
            self.menuButton.pack()
            self.backButton = tkinter.Button(menuBar, text="BACK", command=backClicked)
            self.backButton['width'] = int(masterFrame.winfo_screenwidth() / 6)
            self.backButton['height'] = int(masterFrame.winfo_screenheight() / 6)
            self.backButton['font'] = fontSize

        def createExitButton(fontSize):
            print("we craftin exit")
            exitButtonPokus = tkinter.Button(exitBar, text="EXIT",command=self.masterFrame.destroy)
            exitButtonPokus['width'] = int(masterFrame.winfo_screenwidth() / 6)
            exitButtonPokus['height']= int(masterFrame.winfo_screenwidth() / 6)
            exitButtonPokus['font'] = fontSize
            exitButtonPokus.pack()

        def createOptionsButtons(fontSize):
            print("we craftin options")
            self.emailButton = tkinter.Button(optionsBar, text="EMAIL",command=lambda : print("email"))
            self.emailButton['height']= int(masterFrame.winfo_screenwidth() / 6)
            self.emailButton['font'] = fontSize
            self.browserButton = tkinter.Button(optionsBar, text="BROWSER",command=lambda : print("browser"))
            self.browserButton['height']= int(masterFrame.winfo_screenwidth() / 6)
            self.browserButton['font'] = fontSize

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
        optionsBar = Frame(masterBar, bg='YELLOW') #až přijdeš čas, vrátit na bílou/černou barvu
        optionsBar.pack_propagate(False)
        optionsBar.pack(expand=True, fill=BOTH)

        #volání defů pro tlačítka
        createMenuButtons(__fontSize)
        createOptionsButtons(__fontSize)
        createExitButton(__fontSize)

        pokusValue = masterBar.winfo_reqheight()
        print("velikost:",pokusValue)
    def __str__(self):
        return 'Halvetica;36;BOLD'

class ApplicationsFrame:
    def __init__(self, applicationsFrame):
        self.applicationsFrame = applicationsFrame

        print("app frame")
        heighNum = int(applicationsFrame.winfo_screenheight()-(applicationsFrame.winfo_screenheight()/6))
        applicationFrame = Frame(applicationsFrame,height=heighNum,bg="#bababa")
        applicationFrame.pack_propagate(False)
        applicationFrame.pack(fill=X)
        print("velikost appSvine:",heighNum,"vs",applicationFrame.winfo_height())
class App:
    def __init__(self, masterWindow):
        self.masterWindow = masterWindow
        masterWindow.title("for senior")

        screen_width = masterWindow.winfo_screenwidth()
        screen_height = masterWindow.winfo_screenheight()
        self.res = "{a}x{b}".format(a=int(screen_width), b=int(screen_height))
        #todo: zapsat do json dokumentu

        masterWindow.geometry(self.res)
        masterWindow.overrideredirect(True)

    def __str__(self):
        return self.res


if __name__ == '__main__':
    root = Tk()
    my_gui = App(root)
    menuframe = MenuFrame(root)
    appframe = ApplicationsFrame(root)

    pokusValue = str(menuframe).split(';')
    pokusJson = JsonActions(str(my_gui),pokusValue[0],pokusValue[1],pokusValue[2])



    root.mainloop()