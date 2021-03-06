import os
import name_format
import date_move
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.ttk import Labelframe, Progressbar

class Gui:

    def __init__(self):
        self.master = Tk()
        
        self.CANVAS_WIDTH = 550
        self.CANVAS_HEIGHT = 250
        self.SCREEN_WIDTH = self.master.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.master.winfo_screenheight()
        self.POS_X = int((self.SCREEN_WIDTH / 2) - (self.CANVAS_WIDTH / 2))
        self.POS_Y = int((self.SCREEN_HEIGHT / 2) - (self.CANVAS_HEIGHT / 2))
        
        self.options_radio_btn = IntVar()
        self.settings_radio_btn = IntVar()
        self.settings = {'Files': 'Default',
                         'Hashing': False,
                         'Output': False}
        self.default_files = ['JPG', 'JPEG', 
                              'PNG', 'GIF', 
                              'RAW', 'MP4', 
                              'MOV', 'AVI']
        self.target_dir = ''
        self.num_files = 0
        self.default = True
        self.out_list = []
        self._canvas_init()


    def main_loop(self):
        mainloop()
    
    def _run_logic(self, run):
        self.output_lb['state'] = NORMAL
        self.output_lb.insert(END, '*'*20)
        while True:
            try:
                self.output_lb['state'] = NORMAL
                out = next(run)
                self.output_lb.insert(END, out)
                self.out_list.append(out)
                self.output_lb.see(END)
                self.output_lb['state'] = DISABLED
                self.progress_bar['value'] += 10
            except:
                break

        if self.settings['Output']:
            self._output(self.out_list)
        
        self.progress_bar['value'] = 100
        self.output_lb['state'] = NORMAL
        self.output_lb.insert(END, '-- Done --')
        self.out_list.append('-- Done --')
        self.output_lb.see(END)
        self.output_lb['state'] = DISABLED

# Main execution logic           
    def _rename_1(self, allowed_files):
        self.output_lb['state'] = NORMAL
        self.output_lb.insert(END, '-- Renaming --')
        self.out_list.append('-- Renaming --')
        n_f = name_format.main(self.target_dir, allowed_files)
        self._run_logic(n_f)
                    
    def _move_2(self, allowed_files):
        self.output_lb['state'] = NORMAL
        self.output_lb.insert(END, '-- Moving --')
        self.out_list.append('-- Moving --')
        d_m = date_move.main(self.target_dir, allowed_files, self.settings['Hashing'])
        self._run_logic(d_m)

    def _both_3(self, allowed_files):
        self._rename_1(allowed_files)
        self._move_2(allowed_files)
        
    def _call_run(self):
        if self.target_dir == "":
            self.output_lb['state'] = NORMAL
            self.output_lb.insert(END, '!! No directory selected !!')
            self.output_lb['state'] = DISABLED
            return
        if self.num_files == 0:
            self.output_lb['state'] = NORMAL
            self.output_lb.insert(END, '!! No Files in directory !!')
            self.output_lb['state'] = DISABLED
            return
        
        options = {1: self._rename_1, 
                   2: self._move_2, 
                   3: self._both_3}
        
        if self.settings['Files'] == 'Default':
            allowed_files = self.default_files
        else:
            allowed_files = 'All'
            
        options[self.options_radio_btn.get()](allowed_files)

    def _output(self, out_list):
        with open('output.txt', 'w') as f:
                for o in out_list:
                    f.write(f'{o}\n')
        self.output_lb['state'] = NORMAL
        self.output_lb.insert(END, 'Output written to file: out.txt')
        self.output_lb.see(END)
        self.output_lb['state'] = DISABLED
                    
    def _clear_frames(self, *f):
        for frame in f:
            for w in frame.winfo_children():
                w.destroy()
                
    def _output_labels(self):
        pass

    def _count_files(self, d):
        # pth, ds, fs = next(os.walk(d))  # Can be used if only current dir file tot is required
        f_tot = 0
        for pth, ds, fs in os.walk(d):
            for n in fs:
                f_tot += 1
        return f_tot
    
    def _get_dir(self):
        self.target_dir = askdirectory()
        if self.target_dir == '':
            self.default = True
            self._dynamic_labels(self.default, self.target_dir, self.num_files, self.settings)
            return
        self.num_files = self._count_files(self.target_dir)
        self.default = False
        self.progress_bar['value'] = 0
        self._dynamic_labels(self.default, self.target_dir, self.num_files, self.settings)
       
# Settings window logic and Init
    def _update_settings(self):
        if self.settings_radio_btn.get() == 4:
            f = 'Default'
        else:
            f = 'All'
        tmp = [f, self.h_var.get(), self.o_var.get()]
        c = 0
        for i in tmp:
            k = list(self.settings)[c]
            self.settings[k] = i
            c += 1

    def _apply_settings(self, win):
        self._clear_frames(self.settings_frame)
        self._dynamic_labels(self.default, self.target_dir, self.num_files, self.settings)
        applied = Label(win, text="Applied!", fg="Red")
        applied.place(x=70, y=153)
        applied.after(2500, lambda: applied.destroy())
        
    def _settings_window(self, applied):
        win = Toplevel(self.master)
        win.title("Settings")
        win.geometry(f'{self.CANVAS_WIDTH-20}x{self.CANVAS_HEIGHT-60}+{self.POS_X}+{self.POS_Y}')
        if applied:
            Label(win, text="Applied!", fg="Red").place(x=85, y=150)
        
        h_info = "Enables file hashing to check for duplicates. Enabling will increase run-time."
        o_info = "Outputs log info into a text file in current directory."
        default_info = f"{self.default_files}"
        all_info = "All file types. (Caution: ALL files will be renamed based on modified date)"
        custom_info = "Enter file types seperated by commas."
        self.h_var, self.o_var = BooleanVar(), BooleanVar()
        
        LabelFrame(win, text="Optional").place(x=15, y=5, height=70, width=500)
        hash_btn = Checkbutton(win, text=f"Hashing - {h_info}", var=self.h_var, command=self._update_settings)
        hash_btn.place(x=20, y=20)
        out_btn = Checkbutton(win, text=f"Output - {o_info}", var=self.o_var, command=self._update_settings)
        out_btn.place(x=20, y=40)
        
        LabelFrame(win, text="Allowed Files").place(x=15, y=80, height=70, width=450)
        default_btn = Radiobutton(win, text=f"Default - {default_info}", var=self.settings_radio_btn, value=4, command=self._update_settings)
        default_btn.place(x=20, y=95)
        all_btn = Radiobutton(win, text=f"All - {all_info}", var=self.settings_radio_btn, value=5, command=self._update_settings)
        all_btn.place(x=20, y=115)
        if self.options_radio_btn.get() == 1:
            self.settings['Hashing'] = False
            hash_btn.deselect()
            hash_btn['state'] = DISABLED
            self._dynamic_labels(self.default, self.target_dir, self.num_files, self.settings)
            self._apply_settings()
        if self.settings['Files'] == 'Default':
            default_btn.select()
        elif self.settings['Files'] == 'All':
            all_btn.select()
        if self.settings['Hashing']:
            hash_btn.select()
        if self.settings['Output']:
            out_btn.select()
            
        Button(win, text="Apply", command=lambda:self._apply_settings(win)).place(x=15, y=150)
        # Potential future feature
        # Radiobutton(win, text=f"Custom - {custom_info}", var=self.radio_btn, value=3).place(x=20, y=105)


# Main window objects and Init
    def _frames(self):
        LabelFrame(self.master, text="Options").place(x=15, y=5, height=85, width=90)
        LabelFrame(self.master).place(x=15, y=65, height=35, width=90)  # Both divider
        
        self.dir_frame = LabelFrame(self.master, text="Directory")
        self.dir_frame.place(x=150, y=5, height=45, width=300)
        
        self.out_frame = LabelFrame(self.master, text="Output")
        self.out_frame.place(x=300, y=55, height=105, width=200)
        
        self.settings_frame = LabelFrame(self.master, text="Enabled Settings")
        self.settings_frame.place(x=150, y=55, height=105, width=135)
        
        self.numF_frame = Frame(self.master)
        self.numF_frame.place(x=79, y=190, height=20, width=30)

    def _dynamic_labels(self, default, working_dir, file_num, enabled_settings):
        if default:
            working_dir = "No directory selected"
            file_num = 0
        self._clear_frames(self.dir_frame, self.numF_frame)
        Label(self.dir_frame, text=working_dir).place(x=5, y=0)
        Label(self.numF_frame, text=file_num).place(x=0, y=0)
        
        y = 3
        for k in enabled_settings:
            if enabled_settings[k]:
                out = f"{k} - {enabled_settings[k]}"
                tmp = Label(self.settings_frame, text=out).place(x=5, y=y)
                y += 20
                
    def _static_labels(self):
        Label(self.master, text="Total Files: ").place(x=15, y=190)
               
    def _listbox(self):
        sb = Scrollbar(self.out_frame)
        sb.pack(side=RIGHT, fill=Y)
        self.output_lb = Listbox(self.out_frame, width=29, height=5, yscrollcommand=sb.set)
        self.output_lb.place(x=0, y=0)
        sb.config(command=self.output_lb.yview)
        self.output_lb['state'] = DISABLED
            
    def _radio_buttons(self):
        Radiobutton(self.master, text="Rename", var=self.options_radio_btn, value=1).place(x=20, y=20)
        Radiobutton(self.master, text="Move", var=self.options_radio_btn, value=2).place(x=20, y=40)
        bth = Radiobutton(self.master, text="Both", var=self.options_radio_btn, value=3)
        bth.place(x=20, y=70)
        bth.select()
        
    def _push_buttons(self):
        Button(self.master, text="Settings", command=lambda:self._settings_window(False), width=11).place(x=15, y=105)
        Button(self.master, text="Go!", command=lambda:self._call_run(), width=11).place(x=15, y=135)
        Button(self.master, text="Select dir", command=self._get_dir, width=7).place(x=455, y=17)
        
    def _progress_bar(self):
        self.progress_bar = Progressbar(self.master, orient=HORIZONTAL, length=300, mode="determinate")
        self.progress_bar.place(x=150, y=190)
        
    def _canvas_init(self):
        self.master.resizable(width=False, height=False)
        self.master.title("Photo Sorter")
        # self.master.iconbitmap('../imgs/icon.ico')  # Throws not defined error.
        
        self.master.geometry(f'{self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT}+{self.POS_X}+{self.POS_Y}')
        
        
        self._frames()
        self._dynamic_labels(self.default, None, None, self.settings)
        self._static_labels()
        self._listbox()
        self._radio_buttons()
        self._push_buttons()
        self._progress_bar()
        
        # self.test_btn()

    def test_btn(self):
        Button(self.master, text="DEBUG", command=lambda:self.test()).place(x=470, y=200)

    def test(self):
        print("TESTING")
        print(f"Settings: {self.settings}\nOption: {self.options_radio_btn.get()}\nDir: {self.target_dir}")
        
        self.output_lb['state'] = NORMAL
        i = ('test', '\n', 'test2')
        self.output_lb.insert(END, i)
