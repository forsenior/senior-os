import tkinter as tk
import json

def json_read():
    f = open('config.json')
    data = json.load(f)
    value = data['data']['appResolution-Y']
    valueX = data['data']['appResolution-X']
    print(value)
    f.close()
    return [value,valueX]
class GUI(tk.Frame):
    print("workey workey")
    def __init__(self):
        super().__init__()
        frame = tk.Frame(height=json_read()[0], width=json_read()[1], bg='#5A5A5A')
        frame.pack_propagate(False)
        frame.pack()


        b = tk.Button(frame, text="E X I T ")
        b['command']=frame.destroy
        b.pack()


if __name__ == "__main__":
    gui = GUI()
    gui.pack(fill="both", expand=True)
    tk.mainloop()




