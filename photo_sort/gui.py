from tkinter import *


class Gui:

    def __init__(self):
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 400
        self.master = Tk()
        self._canvas_init()
        

    def main_loop(self):
        mainloop()

    def _canvas_init(self):
        w = Canvas(self.master, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        w.pack()