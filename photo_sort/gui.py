from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.ttk import Progressbar

class Gui:

    def __init__(self):
        self.CANVAS_WIDTH = 550
        self.CANVAS_HEIGHT = 250
        self.master = Tk()
        
        self.rename_btn, self.move_btn, self.both_btn = IntVar(), IntVar(), IntVar()
        self._canvas_init()

    def main_loop(self):
        mainloop()
        
    def isChecked(self):
        pass
    
    def _frames(self):
        LabelFrame(self.master, text="Options").place(x=15, y=5, height=85, width=90)
        LabelFrame(self.master).place(x=15, y=65, height=35, width=90)  # Both divider
        LabelFrame(self.master, text="Directory").place(x=150, y=5, height=45, width=300)
        LabelFrame(self.master, text="Output").place(x=300, y=55, height=115, width=150)
        LabelFrame(self.master, text="Enabled Settings").place(x=150, y=55, height=115, width=135)
        

    def _check_buttons(self):
        # state=DISABLED to prevent grey-out
        Checkbutton(self.master, text="Rename", var=self.rename_btn, command=self.isChecked).place(x=20, y=20)
        Checkbutton(self.master, text="Move", var=self.move_btn, command=self.isChecked).place(x=20, y=40)
        Checkbutton(self.master, text="Both", var=self.both_btn, command=self.isChecked).place(x=20, y=70)
        
    def _push_buttons(self):
        Button(self.master, text="Settings", width=11).place(x=15, y=105)
        Button(self.master, text="Go!", width=11).place(x=15, y=135)
        Button(self.master, text="Select dir", width=7).place(x=455, y=17)
        
    def _static_labels(self):
        Label(self.master, text="Total Files: ").place(x=15, y=190)
        
    def _dynamic_labels(self, default, working_dir, file_num):
        if default:
            working_dir = "No directory selected"
            file_num = 0
        Label(self.master, text=working_dir).place(x=155, y=23)
        Label(self.master, text=file_num).place(x=75, y=190)
        
    def _get_dir(self):
        # d = askdirectory()
        pass
    
    def _progress_bar(self):
        progress = Progressbar(self.master, orient=HORIZONTAL, length=300, mode="determinate").place(x=150, y=190)
    
    def _canvas_init(self):
        self.master.title("Photo Sorter")
        # self.master.iconbitmap('../imgs/icon.ico')  # Throws not defined error.
        self.master.geometry(f'{self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT}')
        self._frames()
        self._static_labels()
        self._dynamic_labels(True, None, None)
        self._check_buttons()
        self._push_buttons()
        self._progress_bar()
