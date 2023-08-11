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

        self.title = tk.Label(self, text="Main page")
        self.title.pack()

        self.label = tk.Label(self, text="Set shortcut")
        self.label.pack()

        self.shortcut_widget = ShortcutWidget(self, self.shortcut)
        self.shortcut_widget.pack()

class ShortcutWidget(tk.Frame):
    def __init__(self, master, shortcut):
        tk.Frame.__init__(self, master)
        self.service_keys = ["Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"]
        self.is_bad_shortcut = True
        self.is_changing_shortcut = False
        self.old_shortcut = []
        self.shortcut = shortcut

        self.text_var = tk.StringVar()
        self.text = tk.Entry(self, textvariable=self.text_var)
        self.text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.button = tk.Button(self, text="Change", command=self.change_shortcut)
        self.button.pack(side=tk.LEFT)

        self.bind_all("<KeyPress>", self.shortcut_press_handler)
        self.bind_all("<KeyRelease>", self.shortcut_release_handler)

    def shortcut_has_general_keys(self):
        for key in self.shortcut:
            if key in self.service_keys:
                continue

            return True
            
        return False
    
    def shortcut_sort(self):
        self.shortcut.sort(key=lambda x: self.service_keys.index(x) if x in self.service_keys else len(self.service_keys))

    def shortcut_key_add(self, key):
        if not key in self.shortcut:
            self.shortcut.append(key)
            self.shortcut_sort()
            self.text_var.set("+".join(self.shortcut))

    def change_shortcut(self):
        self.shortcut = []
        self.is_changing_shortcut = True
        self.button.configure(state = tk.DISABLED, text='Press key')

    def shortcut_press_handler(self, event):
        if self.is_changing_shortcut:
            self.shortcut_key_add(event.keysym)

    def shortcut_release_handler(self, event):
        if self.is_changing_shortcut:
            if not self.shortcut_has_general_keys():
                # Reset shortcut
                self.shortcut = self.old_shortcut
                self.text_var.set("+".join(self.shortcut))
                self.is_changing_shortcut = False
                self.button.configure(state = tk.NORMAL, text='Change')
            else:
                # Apply shortcut
                self.old_shortcut = self.shortcut
                self.text_var.set("+".join(self.shortcut))
                self.is_changing_shortcut = False
                self.button.configure(state = tk.NORMAL, text='Change')

def main():
    app = App()
    app.switch_frame(PageMain)
    app.mainloop()

if __name__ == "__main__":
    main()