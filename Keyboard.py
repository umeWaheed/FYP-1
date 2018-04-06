import tkinter as tk
import tkinter.ttk as ttk
import Global

# -- Declaration of font styles --- #
font_title = ("Helvetica", 18, "bold")
font_message = ("Helvetica", 14)
font_message_small = ("Helvetica", 11)
font_vKeyboard = ("Helvetica", 10)
font_vKeyboardSpecialKeys = ("Helvetica", 10, "bold")

# -- GUI's main class -- #
'''class GUI:
    def __init__(self, frame):
        # self.window = tk.Toplevel(parent)

        # container = frame    # ttk.Frame(parent, width=480, height=320)
        frame.grid_propagate(0)
        # container.pack(fill="both", expand=1)

        ttk.Style().configure("vKeyboard.TButton", font=font_vKeyboard)

        self.frames = {}

        page_name = StartPage.__name__
        StartPage(frame, controller=self)
        self.frames[page_name] = frame
'''

class StartPage:
    def __init__(self, frame):
        # ttk.Frame.__init__(self, parent)
        # label1 = ttk.Label(self, text="Example Page", font=font_title)
        # label1.pack(side="top", fill="x", pady=7, padx=10)

        # self.label1 = ttk.Label(self, text="Enter something:", font=font_message)
        # self.label1.pack(side="top")
        # self.entry1 = ttk.Entry(self)
        # self.entry1.pack(side="top")

        self.entry = ttk.Entry(frame)
        self.entry.pack(side="top")
        self.frame1 = ttk.Frame(frame, width=480, height=280)
        self.frame1.pack(side="top", padx= 50, pady=50)

        self.keysize = 4
        self.controller = self
        self.enterAction = "StartPage"

        self.entry.bind("<FocusIn>", lambda e:  self.show_vKeyboard(frame, 1))

        self.kb = vKeyboard(attach=self.entry,
                            x=self.entry.winfo_rootx(),
                            y=self.entry.winfo_rooty() + self.entry.winfo_reqheight(),
                            keysize=self.keysize,
                            parent=self.frame1,
                            controller=self.controller,
                            enterAction=self.enterAction)

    def show_vKeyboard(self,frame, k):
        if k == 1:
            self.frame1.destroy()
            # self.frame2.destroy()
            self.kb.destroy()

            self.frame1 = ttk.Frame(frame, width=frame.winfo_width, height=frame.winfo_height)
            self.frame1.pack(side="top", pady=30, padx=50)
            self.kb = vKeyboard(attach=self.entry,
                                 x=self.entry.winfo_rootx(),
                                 y=self.entry.winfo_rooty() + self.entry.winfo_reqheight(),
                                 keysize=self.keysize,
                                 parent=self.frame1,
                                 controller=self.controller,
                                 enterAction=self.enterAction)


class vKeyboard(ttk.Frame):
    # --- A frame for the keyboard(s) itself --- #
    def __init__(self, parent, attach, x, y, keysize, controller, enterAction):
        ttk.Frame.__init__(self, takefocus=0)

        self.attach = attach
        self.keysize = keysize
        self.parent = parent
        self.x = x
        self.y = y
        self.controller = controller
        self.enterAction = enterAction

    # --- Different sub-keyboards (e.g. alphabet, symbols..) --- #
        # --- Lowercase alphabet sub-keyboard --- #
        self.alpha_Frame = ttk.Frame(parent)
        self.alpha_Frame.grid(row=0, column=0, sticky="nsew")

        self.row1_alpha = ttk.Frame(self.alpha_Frame)
        self.row2_alpha = ttk.Frame(self.alpha_Frame)
        self.row3_alpha = ttk.Frame(self.alpha_Frame)
        self.row4_alpha = ttk.Frame(self.alpha_Frame)

        self.row1_alpha.grid(row=1)
        self.row2_alpha.grid(row=2)
        self.row3_alpha.grid(row=3)
        self.row4_alpha.grid(row=4)

        self.keyState = 1
        self.init_keys()

        self.alpha_Frame.tkraise()

        self.pack()

    def init_keys(self):
        self.alpha = {
            'row1': ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'Bksp'],
            'row2': ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            'row3': ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            'row4': ['[ space ]']
        }

        self.keyStyle = self.alpha
        self.row1 = self.row1_alpha
        self.row2 = self.row2_alpha
        self.row3 = self.row3_alpha
        self.row4 = self.row4_alpha

        for row in self.keyStyle.keys():  # iterate over dictionary of rows
            if row == 'row1':  # TO-DO: re-write this method
                i = 1  # for readability and functionality
                for k in self.keyStyle[row]:
                    if k == 'Bksp':
                        ttk.Button(self.row1,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 2,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    else:
                        ttk.Button(self.row1,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    i += 1
            elif row == 'row2':
                i = 2
                for k in self.keyStyle[row]:
                    ttk.Button(self.row2,
                               style="vKeyboard.TButton",
                               text=k,
                               width=self.keysize,
                               command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    i += 1
            elif row == 'row3':
                i = 2
                for k in self.keyStyle[row]:
                    if k == 'ENTER':
                        ttk.Button(self.row3,
                                   style="vKeyboardSpecial.TButton",
                                   text=k,
                                   width=self.keysize * 2,
                                   command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    else:
                        ttk.Button(self.row3,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    i += 1
            else:
                i = 3
                for k in self.keyStyle[row]:
                    if k == '[ space ]':
                        ttk.Button(self.row4,
                                   style="vKeyboard.TButton",
                                   text='     ',
                                   width=self.keysize * 6,
                                   command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    i += 1

    def _attach_key_press(self, k):
        if k == 'Bksp':
            self.remaining = self.attach.get()[:-1]
            self.attach.delete(0, tk.END)
            self.attach.insert(0, self.remaining)
        elif k == 'ENTER':
            Global.name = self.attach.get()
            # switch_page('home')
            # Global.name =                                     # Define, what's supposed to happen..
            #self.controller.enter_cb(self.enterAction)
        elif k == 'BACK':
            self.controller.showFrame("StartPage")  # Or any other page...
        elif k == '[ space ]':
            self.attach.insert(tk.END, ' ')
        else:
            self.attach.insert(tk.END, k)


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root, width=400, height=400)
    # app = GUI(root)
    root.mainloop()
