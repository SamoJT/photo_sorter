from tkinter import *
from tkinter.filedialog import askdirectory

class Gui:

    def __init__(self):
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 400
        self.master = Tk()
        
        self.rename_btn, self.move_btn, self.both_btn = IntVar(), IntVar(), IntVar()
        
        self._canvas_init()

    def main_loop(self):
        mainloop()
        
    def isChecked(self):
        pass
        
    def _check_buttons(self):
        # state=DISABLED to prevent grey-out
        frame = LabelFrame(self.master, text="Options").place(x=15, y=5, height=85, width=90)
        Checkbutton(frame, text="Rename", var=self.rename_btn, command=self.isChecked).place(x=20, y=20)
        Checkbutton(frame, text="Move", var=self.move_btn, command=self.isChecked).place(x=20, y=40)
        
        frame2 = LabelFrame(self.master).place(x=15, y=65, height=35, width=90)
        Checkbutton(frame2, text="Both", var=self.both_btn, command=self.isChecked).place(x=20, y=70)
        
    def _push_buttons(self):
        Button(self.master, text="Settings", width=11).place(x=15, y=105)
        Button(self.master, text="Go!", width=11).place(x=15, y=135)
    
    def _TODO(self):
        # Sort button to allow dir selection and display selected
        # dir to user.
        d = askdirectory()
        
    def _canvas_init(self):
        self.master.title("Photo Sorter")
        self.master.geometry(f'{self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT}')
        self._check_buttons()
        self._push_buttons()
        