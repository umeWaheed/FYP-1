# from graphics import Image as Im
from FaceDetection import gather_samples
from Face import resize
from graphics import *
import tkinter as tk
# from threading import Timer
# import pyttsx3
import Global
import MainFace1
import threading
# from subprocess import Popen
from PIL import Image, ImageTk
from Face import resize
from FacialLandmark import rect_to_bb
# import numpy as np
import cv2
import dlib
from tkinter import Scale
from Analyse import load_settings
from Keyboard import StartPage
import Frames
# import VideoStream  # for pi camera

# Global.vid = VideoStream.VideoStream(usePiCamera=True).start()
Global.vid = cv2.VideoCapture(0)  # for webcam
# global func_id,
global req_frame
# func_id = None
width = 800
height = 400

def prints():
    print('here')
    s.frame.grid_forget()


def takeInput():
    global page1
    s.ok.grid_forget()
    Frames.switch_page("input")
    frame = s.frames['input']
    # s.frames[s.current_frame].grid_forget()
    # s.current_frame = 'input'
    but = tk.Button(frame, text='lets be friends', command=get_name)
    but.pack(side='bottom')
    page1 = StartPage(frame)
    # s.frames[s.current_frame].grid(row=3, column=0)


def get_name():
    Global.name = page1.entry.get()
    print(Global.name)
    Frames.switch_page('home')
    gather()


class Screen(tk.Frame):
    def __init__(self):
        super(Screen, self).__init__()
        self.blinking = True
        '''self.win = GraphWin('New window', 500, 300)
        self.win.setBackground(color_rgb(255, 255, 255))'''
        self.win = tk.Tk()
        self.win.wm_title('Fit Assist')
        # self.win.state('zoomed')
        self.win.attributes('-fullscreen', True)
        self.win.config(background='white') # , width=width, height=height)
        # width = self.win.winfo_width()
        # height = self.win.winfo_height()

        '''add menu in the screen'''
        self.menu = tk.Menu(self.win)
        self.menu.add_command(label='Home', command=Frames.get_home)
        self.menu.add_command(label='Stats', command=prints)

        self.exermenu = tk.Menu(self.menu)
        self.eyemenu = tk.Menu(self.exermenu)

        self.eyemenu.add_command(label='Eye rolling', command=lambda: Frames.read_exer(1))
        self.eyemenu.add_command(label='Focus shifting', command=lambda:Frames.read_exer(2))
        self.eyemenu.add_command(label='Blinking', command=lambda: Frames.read_exer(3))
        self.eyemenu.add_command(label='The 20-20-20 rule', command=lambda: Frames.read_exer(4))
        self.eyemenu.add_command(label='Palming', command=lambda: Frames.read_exer(5))
        self.eyemenu.add_command(label='Eye massage', command=lambda: Frames.read_exer(6))
        self.eyemenu.add_command(label='Figure 8', command=lambda: Frames.read_exer(7))

        self.exermenu.add_command(label='neck', command=prints)
        self.exermenu.add_cascade(label='eyes', menu=self.eyemenu)
        self.menu.add_cascade(label='Exercises', menu=self.exermenu)

        self.menu.add_command(label='Settings', command=Frames.get_settings)
        self.menu.add_command(label='About', command=Frames.get_about)
        self.menu.add_command(label='Exit', command=Frames.cancel)
        self.win.config(menu=self.menu)

        '''frame holds the images to be displayed'''
        self.frames = {}
        self.current_frame = "home"
        self.prev=""
        self.frames['input'] = self.input = tk.Frame(self.win, width=width, height=height-100)
        self.frames['home'] = self.frame = tk.Frame(self.win, width=width, height=height-100)     # home frame
        self.frames['config'] = self.config = tk.Frame(self.win, width= width, height=height-100)    # configuration frame
        self.frames['about'] = self.about_frame = tk.Frame(self.win, width=width, height=height - 100)  # about frame
        self.frames['setting'] = self.set_frame = tk.Frame(self.win, width=width, height=height-100)     # settings frame
        self.frames['exercise'] = tk.Frame(self.win, width=width, height=height-100)     # exercise frame
        self.frames[self.current_frame].grid(row=3, column=0)

        self.label1 = tk.Label(self.frames["home"])
        self.lmain = None
        self.slider = Scale(self.frames["config"], from_=20, to=50, orient='horizontal', tickinterval=5, length=200)
        self.label1.grid(row=3, column=0)

        self.gifBackgroundImages = list()
        self.actualGifBackgroundImage = 0
        self.ok = tk.Button(self.win, text='click me to become friends!', command=takeInput)

    def run_gif(self):
        # global func_id
        # CHECK IF LIST IS EMPTY
        if not Global.is_available: # if user is not available go sad
            self.sad()
        else:
            if len(self.gifBackgroundImages) == 0:
                # CREATE FILES IN LIST
                for foldername in os.listdir('resources/cute'):
                    self.gifBackgroundImages.append(foldername)
                    # ALPHABETICAL ORDER
                self.gifBackgroundImages.sort(key=lambda x: int(x.split('.')[0].split('-')[1]))
                print(self.gifBackgroundImages)

            if self.actualGifBackgroundImage == len(self.gifBackgroundImages):
                self.actualGifBackgroundImage = 0

            img = Image.open('resources/cute/' + self.gifBackgroundImages[self.actualGifBackgroundImage])
            img = img.resize((self.win.winfo_width(), self.win.winfo_height()))
            imgs = ImageTk.PhotoImage(image=img, master=self.label1)
            self.label1.imgtk = imgs
            self.label1.configure(image=imgs)
            # self.label1.place(x='0', y='0')
            '''self.background["file"] = 'resources/gif/' + self.gifBackgroundImages[self.actualGifBackgroundImage]
            self.label1["image"] = self.background'''
            self.actualGifBackgroundImage += 1

            # MILISECONDS/ PER FRAME
        Global.func_id = self.after(100, lambda: self.run_gif())

    def sad(self):
        img = Image.open('resources/sad.gif')
        # img = img.resize((self.win.winfo_width(), self.win.winfo_height()))
        imgs = ImageTk.PhotoImage(image=img, master=self.label1)
        self.label1.imgtk = imgs
        self.label1.configure(image=imgs)
        # self.label1.place(x='0', y='0')

    def show_frame(self):
        global req_frame
        ret, frame = Global.vid.read()
        if not ret:
            print('empty')
        # frame = Global.vid.read()
        frame = resize(frame,width=400)
        frame = cv2.flip(frame, 1)  # flip the stream to match real world
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img, master=self.lmain)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)  # the label calls show_frame after every 10 sec
        req_frame = frame  # get the last frame from the video for calibration

    def get_config(self):
        frame = s.frames["config"]
        label = tk.Label(frame, text="Sit according to your preferred posture. Click on button when you are done",
                         fg='red', font='Verdana 14 bold')
        label.grid(row=0, column=0, pady=5)

        bu = tk.Button(frame, text='Calibrate', command=calibrate)
        # when called run face_detection on the last frame
        bu.grid(row=1, column=0, pady=2)

        # Graphics window
        imageFrame = tk.Frame(frame, width=400, height=400)
        imageFrame.grid(row=2, column=0, padx=20, pady=20)
        self.lmain = tk.Label(imageFrame)
        # s.lmain.configure(text='here')
        self.lmain.grid(row=2, column=0)

        self.slider.grid(row=3, column=0)
        self.show_frame()


def calibrate():
    global req_frame
    req_frame = resize(req_frame, width=400)
    detector = dlib.get_frontal_face_detector()
    gray = cv2.cvtColor(req_frame, cv2.COLOR_BGR2GRAY)
    rect = detector(gray, 0)
    (x, y, w, h) = rect_to_bb(rect[0])
    cv2.rectangle(req_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(x, y, w, h)
    write_settings(x,y,w,h,s.slider.get())
    if s.prev == 'setting':
        Frames.switch_page('setting')
    else:
        Frames.switch_page('home')
        s.run_gif()
    cv2.imshow('face', req_frame)
    cv2.waitKey(100)


def write_settings(x, y, w, h, sensit):
    dir_path = 'user_info/'+name+'_'+str(total)+'.txt'
    Global.path = 'user_info/'+name+'_'+str(total)
    fout = open(dir_path, 'w')   # open file in write mode, for new user
    line = str(x)+" "+str(y)+" "+str(w)+" "+str(h)+" "+str(sensit)   # input to file has to be string
    fout.write(line)
    fout.close()
    load_settings(dir_path)     # load the newly written settings


def run(lbl):
    global s, name, total
    # engine = pyttsx3.init()
    Global.monitor_thread = threading.Thread(target=MainFace1.monitor)

    if lbl != 0:
        Global.engine.say("welcome "+f.subjects[lbl])
        Global.engine.setProperty('rate', 120)
        Global.engine.runAndWait()
        Global.name = f.subjects[lbl]
        name = Global.name
        total = lbl
        Global.path = 'user_info/'+name+'_'+str(total)
        Global.monitor_thread.setDaemon(True)  # as it is infinite loop so it prevents to run after program exits
        Global.monitor_thread.start()
        s = Screen()
        Global.screen = s
        s.run_gif()
        # s.blink()
        s.mainloop()
        '''while True:
            s.blink()
            time.sleep(1)'''
    else:   # unknown user
        Global.engine.say("i do not know you")
        Global.engine.setProperty('rate', 120)
        Global.engine.runAndWait()
        s = Screen()
        Global.screen = s

        lbl = tk.Label(s.win, text='you resemble ', width=20)
        lbl.grid(row=0, column=0, sticky='e')
        '''text = ''
        for name in f.subjects:
            text += name'''
        var = tk.StringVar(s.win)
        var.set(f.subjects[Global.close_to])
        list = tk.OptionMenu(s.win, var, *f.subjects)
        list.grid(row=0, column=1, sticky='ew')
        # tk.Label(s.win, text=text).grid(row=1, column=0)
        s.ok.grid(row=2, column=0)
        print('you resemble ', f.subjects[Global.close_to])
        s.sad()
        s.mainloop()


def gather():
    global total, s, name
    name = Global.name
    '''s.label.grid_forget()
    s.ok.grid_forget()
    s.e.grid_forget()'''
    t3 = threading.Thread(target=gather_samples, args=(name, total))
    # the index for which samples are to  be gathered
    t3.start()
    Frames.switch_page('config')
    s.get_config()
    s.mainloop()

    '''while True:
        s.blink()
        time.sleep(1)'''


Global.init()
f = MainFace1.FaceVal()  # load settings
f.load_settings()
name = ""                           # the variable to hold new user
total = len(f.subjects)             # total number of users, ,i.e the next label for new user
label = MainFace1.FaceVal.label     # the predicted label
run(label)            # run main gui
