import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("App")
        self.geometry("300x300")
        self.resizable(False, False)
        self._frame = None
        self.switch_frame(PageMain)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        
        self._frame = new_frame
        self._frame.pack()

class PageMain(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.is_changing_shortcut = False
        self.shortcut = []

        self.title = tk.Label(self, text="Main Page")
        self.title.pack()

        self.label = tk.Label(self, text="Set shortcut")
        self.label.pack()

        self.text_var = tk.StringVar()
        self.text = tk.Entry(self, textvariable=self.text_var)
        self.text.pack()

        self.button = tk.Button(self, text="Change", command=self.change_shortcut)
        self.button.pack()

        self.bind_all("<KeyPress>", self.shortcut_press_handler)
        self.bind_all("<KeyRelease>", self.shortcut_release_handler)
    
    def change_shortcut(self):
        self.is_changing_shortcut = True
        self.button.configure(state = tk.DISABLED, text='Press key')

    def shortcut_press_handler(self, event):
        if self.is_changing_shortcut:
            if event.keysym in ["Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"]:
                self.shortcut.append(event.keysym)
                self.text_var.set("+".join(self.shortcut))


    def shortcut_release_handler(self, event):
        if self.is_changing_shortcut:
            if event.keysym in ["Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"]:
                self.shortcut.remove(event.keysym)
                self.text_var.set("+".join(self.shortcut))
            else:
                self.shortcut.append(event.keysym)
                self.text_var.set("+".join(self.shortcut))
                self.shortcut.clear()
                self.button.configure(state=tk.NORMAL, text='Change')
                self.is_changing_shortcut = False

def main():
    app = App()
    app.switch_frame(PageMain)
    app.mainloop()

if __name__ == "__main__":
    main()
