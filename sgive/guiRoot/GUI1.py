import tkinter as tk
import json


def json_read():
    f = open('config.json')
    data = json.load(f)
    value = data['data']['appResolution-Y']
    valueX = data['data']['appResolution-X']
    print(value)
    f.close()
    return [value, valueX]
_is_running = False
class GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        global _is_running
        def __close_frame():
            global _is_running
            _is_running = False #for now this resest _is_running before closing frame :)
            tk.Frame.destroy(frame)
            self.destroy()

        if _is_running:
            return
        _is_running = True

        frame = tk.Frame(height=json_read()[0], width=json_read()[1], bg='#5A5A5A')
        frame.pack_propagate(False)
        frame.pack()

        w = tk.Label(frame, text="WEB BROWSER DUMMY .PY THING")
        w.pack(fill=tk.X)

        b = tk.Button(frame, text="E X I T ", command=lambda: __close_frame())
        b.pack()



if __name__ == "__main__":
    gui = GUI()
    gui.pack(fill="both", expand=True)
    gui.mainloop()
