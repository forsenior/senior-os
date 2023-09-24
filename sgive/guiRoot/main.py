"""
Written by: RYUseless, BPC-IBE
"""
import tkinter
from tkinter import *
import tkinter.font as font
import json
import screeninfo
import GUI1


def get_monitor_from_coord(x, y): #testing for dualMonitor setup(where sometimes tkinter fails)
    monitors = screeninfo.get_monitors()
    for m in reversed(monitors):
        if m.x <= x <= m.width + m.x and m.y <= y <= m.height + m.y:
            return m
    return monitors[0]

def applications_launcher():
    gui1 = GUI1.GUI()
    gui1.pack(fill=tkinter.X)  # if width for x fails

def screenResMath(tk):
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    heighNum = int(tk.winfo_screenheight() - (tk.winfo_screenheight() / 6))
    res = "{a}x{b}".format(a=int(screen_width), b=int(screen_height))
    return [res,int(screen_width/6),int(screen_height/6),(heighNum),screen_width]
    #fullRes->0    width/6->1  Height/6->2  heighNumberForAplication -> 3   WidthNumberForAplication -> 4

class JsonActions():
    def __init__(self,resolution,appResolutionY,appResolutionX,font,size,weight):
        self.resolution = resolution
        self.appResolutionY = appResolutionY
        self.appResolutionX = appResolutionX
        self.font = font
        self.size = size
        self.weight = weight
        dictionary = {
            'data': {
                "screenResolution":resolution,
                "appResolution-Y":appResolutionY,
                "appResolution-X": appResolutionX,
                "fontName": font,
                "fontSize": size,
                "fontWeight": weight
            }
        }
        json_object = json.dumps(dictionary, indent=4)

        with open("config.json", "w") as outfile:
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
            exitButtonPokus = tkinter.Button(exitBar, text="EXIT",command=self.masterFrame.destroy)
            exitButtonPokus['width'] = sixWidth
            exitButtonPokus['height']= sixHeight
            exitButtonPokus['font'] = fontSize
            exitButtonPokus.pack()

        def createOptionsButtons(fontSize):
            self.emailButton = tkinter.Button(optionsBar, text="EMAIL",command=lambda : print("email"))
            self.emailButton['height']= sixHeight
            self.emailButton['font'] = fontSize
            self.browserButton = tkinter.Button(optionsBar, text="BROWSER", command=lambda : applications_launcher())
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
        optionsBar = Frame(masterBar, bg='#D3D3D3') #až přijdeš čas, vrátit na bílou/černou barvu
        optionsBar.pack_propagate(False)
        optionsBar.pack(expand=True, fill=BOTH)

        #volání defů pro tlačítka
        createMenuButtons(self.fontSize)
        createOptionsButtons(self.fontSize)
        createExitButton(self.fontSize)

    def font(self):
        return self.fontSize

class App:
    def __init__(self, master_window):
        self.master_window = master_window
        master_window.title("SeniorOS interface app")
        # these two should be the same as .attributes('-fullscreen'..etc)
        #master_window.resizable(False,False)
        #master_window.geometry(screenResMath(masterWindow)[0])
        master_window.attributes('-fullscreen', True)

if __name__ == '__main__':
    screeninfo.get_monitors()
    root = Tk()
    my_gui = App(root)
    menu_frame = MenuFrame(root)
    frame_value = menu_frame.font()
    JsonActions(screenResMath(root)[0], screenResMath(root)[3],screenResMath(root)[4], frame_value.cget('family'), frame_value.cget('size'), frame_value.cget('weight'))

    # Get the screen which contains top
    current_screen = get_monitor_from_coord(root.winfo_x(), root.winfo_y())

    # Get the monitor's size
    print("resolution get pokus:",current_screen.width, current_screen.height)

    root.mainloop()

