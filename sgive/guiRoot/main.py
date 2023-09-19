import tkinter
from tkinter import font as tkFont

masterWindow = tkinter.Tk()
screen_width = masterWindow.winfo_screenwidth()
screen_height = masterWindow.winfo_screenheight()
res = "{a}x{b}".format(a=int(screen_width), b=int(screen_height))

masterWindow.title("for senios-alpha")
masterWindow.geometry(res)
masterWindow.overrideredirect(True)

#Master Frame
masterBar = tkinter.Frame(masterWindow, height=int(screen_height/6))
masterBar.pack_propagate(False) #zakazuje, aby se velikost baru fixne scaloval podle velikosti tlacitka
masterBar.pack(side=tkinter.TOP, fill=tkinter.X)

#innerFrame
menuBar = tkinter.Frame(masterBar, width=int(screen_width/6), bg='GREEN')
menuBar.pack_propagate(False)
menuBar.pack(side=tkinter.LEFT,fill=tkinter.Y)
exitBar = tkinter.Frame(masterBar, width=int(screen_width/10), bg='BROWN')
exitBar.pack_propagate(False)
exitBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
optionsBar = tkinter.Frame(masterBar, bg='YELLOW')
optionsBar.pack_propagate(False)
optionsBar.pack(expand=True, fill=tkinter.BOTH)

fontPokus = tkFont.Font(family='Halvetica',size=36,weight=tkFont.BOLD)
pokusButton = tkinter.Button(menuBar,text="MENU",width=int(screen_width/6), height=int(screen_height/6),font=fontPokus)
pokusButton.pack()

exitButtonPokus = tkinter.Button(exitBar, text="EXIT", width=int(screen_width / 6), height=int(screen_height / 6), font=fontPokus, command=masterWindow.destroy)
exitButtonPokus.pack()

masterWindow.mainloop()

if __name__ == '__main__':
    print("gui")
    print(res)