import os
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.ttk import Progressbar

class Gui:

    def __init__(self):
        self.CANVAS_WIDTH = 550
        self.CANVAS_HEIGHT = 250
        self.master = Tk()
        
        self.master_radio_btn = IntVar()
        self.settings_radio_btn = IntVar()
        self._canvas_init()

    def main_loop(self):
        mainloop()
        
    def settings_window(self):
        win = Toplevel(self.master)
        win.title("Settings")
        win.geometry(f'{self.CANVAS_WIDTH-20}x{self.CANVAS_HEIGHT-60}')
        
        h_info = "Enables file hashing to check for duplicates. Enabling will increase run-time."
        o_info = "Outputs log info into a text file in current directory."
        default_info = "[JPG, JPEG, PNG, GIF, RAW, MP4, MOV, AVI]"
        all_info = "All file types. Caution: ALL files will be renamed based on date created."
        custom_info = "Enter file types seperated by commas."
        
        LabelFrame(win, text="Optional").place(x=15, y=5, height=70, width=500)
        Checkbutton(win, text=f"Hashing - {h_info}").place(x=20, y=20)
        Checkbutton(win, text=f"Output - {o_info}").place(x=20, y=40)
        
        LabelFrame(win, text="Allowed Files").place(x=15, y=80, height=70, width=450)
        default_btn = Radiobutton(win, text=f"Default - {default_info}", var=self.settings_radio_btn, value=4)
        Radiobutton(win, text=f"All - {all_info}", var=self.settings_radio_btn, value=5).place(x=20, y=115)
        default_btn.place(x=20, y=95)
        default_btn.select()
        # Potential future feature
        # Radiobutton(win, text=f"Custom - {custom_info}", var=self.radio_btn, value=3).place(x=20, y=105)
        
    def options(self):
        pass
    
    def count_files(self, d):
        pth, ds, fs = next(os.walk(d))
        return len(fs)
    
    def get_dir(self):
        d = askdirectory()
        n = self.count_files(d)
        self._dynamic_labels(False, d, n)
        
    def _frames(self):
        LabelFrame(self.master, text="Options").place(x=15, y=5, height=85, width=90)
        LabelFrame(self.master).place(x=15, y=65, height=35, width=90)  # Both divider
        LabelFrame(self.master, text="Directory").place(x=150, y=5, height=45, width=300)
        LabelFrame(self.master, text="Output").place(x=300, y=55, height=115, width=150)
        LabelFrame(self.master, text="Enabled Settings").place(x=150, y=55, height=115, width=135)
    
    def _radio_buttons(self):
        Radiobutton(self.master, text="Rename", var=self.master_radio_btn, value=1, command=self.options).place(x=20, y=20)
        Radiobutton(self.master, text="Move", var=self.master_radio_btn, value=2, command=self.options).place(x=20, y=40)
        bth = Radiobutton(self.master, text="Both", var=self.master_radio_btn, value=3, command=self.options)
        bth.place(x=20, y=70)
        bth.select()
        
    def _push_buttons(self):
        Button(self.master, text="Settings", command=self.settings_window, width=11).place(x=15, y=105)
        Button(self.master, text="Go!", width=11).place(x=15, y=135)
        Button(self.master, text="Select dir", command=self.get_dir, width=7).place(x=455, y=17)
        
    def _static_labels(self):
        Label(self.master, text="Total Files: ").place(x=15, y=190)
        
    def _dynamic_labels(self, default, working_dir, file_num):
        if default:
            working_dir = "No directory selected"
            file_num = 0
        Label(self.master, text=working_dir).place(x=155, y=23)
        Label(self.master, text=file_num).place(x=75, y=190)
    
    def _progress_bar(self):
        progress = Progressbar(self.master, orient=HORIZONTAL, length=300, mode="determinate").place(x=150, y=190)
    
    def _canvas_init(self):
        self.master.title("Photo Sorter")
        # self.master.iconbitmap('../imgs/icon.ico')  # Throws not defined error.
        self.master.geometry(f'{self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT}')
        self._frames()
        self._static_labels()
        self._dynamic_labels(True, None, None)
        self._radio_buttons()
        self._push_buttons()
        self._progress_bar()
        # self.settings_window()  #DEBUG