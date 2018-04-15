import Global
import tkinter as tk
from PIL import Image, ImageTk
from cv2 import destroyAllWindows
from graph import plot
# import linecache

# func_id = Global.func_id


def switch_page(target):
    s = Global.screen
    func_id = Global.func_id
    if func_id is not None:
        s.parent.after_cancel(func_id)
        Global.func_id = None
        print(func_id)

    s.frames[s.current_frame].grid_forget()
    s.prev = s.current_frame

    # if s.prev == "exercise":
    for element in s.win.winfo_children():
        element.grid_forget()

    s.current_frame = target
    s.frames[target].grid(row=3, column=0)


def get_about():
    # close the run_gif function
    # global func_id
    s = Global.screen

    '''s.frames[s.current_frame].grid_forget()

    s.current_frame = "setting"
    s.frames[s.current_frame].grid(row=3, column=0)'''

    # s.label1.grid_forget()
    # about_frame = tk.Frame(s.win, width=width, height=height-100)
    # s.about_frame.grid(row=3, column=0)
    switch_page("about")
    lab = tk.Label(s.frames['about'])
    lab.grid(row=3, column=0)
    img = Image.open('resources/about.gif')
    img = img.resize((s.parent.winfo_width(),s.parent.winfo_height()))
    imgs = ImageTk.PhotoImage(image=img, master=lab)
    lab.imgtk = imgs
    lab.configure(image=imgs)


def change_sett():
    switch_page('config')
    Global.screen.get_config()


def get_settings():
    s = Global.screen
    switch_page('setting')
    frame = s.frames['setting']     # get the settings frame
    lab = tk.Label(frame, text='You are '+Global.name)
    lab.grid(row=0, column=0, pady=10)
    lab2 = tk.Label(frame)
    img = Image.open('resources/neutral.gif')
    img.resize((50, 50))
    imgs = ImageTk.PhotoImage(image=img, master=lab2)
    lab2.imgtk = imgs
    lab2.configure(image=imgs)
    lab2.grid(row=1, column=0)
    change_pic = tk.Button(frame, text='Update picture')
    change_pic.grid(row=2, column=0, pady=10)
    # entry = tk.Entry(frame)
    # entry.insert(0,Global.name)
    # entry.grid(row=3, column=1)
    lab1 = tk.Label(frame, text='Update settings')
    lab1.grid(row=3, column=0)
    button = tk.Button(frame, text='change', command=change_sett)
    button.grid(row=3, column=1)

    # save_button = tk.Button(frame, text='save changes')
    # save_button.grid(row=5, column=0)
    # user_name = tk.Entry()


def get_home():
    s = Global.screen
    switch_page('home')
    s.label1.grid(row=3, column=0)
    s.frame.grid(row=3, column=0)
    s.run_gif()


def cancel():
    s = Global.screen
    func_id = Global.func_id
    if func_id is not None:
        s.parent.after_cancel(func_id)
        Global.func_id = None
        print(func_id)
    s.parent.destroy()
    Global.vid.release()
    destroyAllWindows()
    Global.shutdown = True
    # Global.vid.stop()


def get_eyes():
    global bu
    s = Global.screen
    switch_page('exercise')

    eyes = ['eye rolling', 'focus shift', '20 20', 'blinking', 'palming', 'massage', 'figure8']
    bu = tk.Button(s.frames['exercise'], text=eyes[0], command=lambda:read_exer(0+1))
    bu.grid(row=0, column=0)

'''
    name = tk.Label(frame, text='eye rolling')
    name.grid(row=0, column=0)
    text = tk.Label(frame,
                    text='Keep your head still and moving only your eyes, look all the way to the left and then move your eyes slowly and smoothly in a clockwise. After doing it clockwise for 30 seconds to 1 minute, you can do it anti-clockwise.')
    text.grid(row=1, column=0)
    lab = tk.Label(s.frames['exercise'])
    lab.grid(row=0, column=1)
    img = Image.open('exercises/eye_rolling.gif')
    imgs = ImageTk.PhotoImage(image=img, master=lab)
    lab.imgtk = imgs
    lab.configure(image=imgs)
    lab.place(x='0', y='0')
'''


def read_exer(id1):
    switch_page('exercise')
    s = Global.screen

    file = open('exercises/eyes.txt')

    for line in file:
        fig_num = int(line[0])   # the figure relevant to exercise
        print(line)
        if fig_num == id1:
            index = line.find(":")
            exer_name = line[2:index]
            text = line[index:]
            print('yes')
            tk.Label(s.frames['exercise'], text=exer_name).grid(row=0,column=0)
            tk.Label(s.frames['exercise'], text=text).grid(row=1,column=0)
            lab = tk.Label(s.frames['exercise'])
            lab.grid(row=3, column=0)
            img = Image.open('exercises/'+str(fig_num)+'.gif')
            imgs = ImageTk.PhotoImage(image=img, master=lab)
            lab.imgtk = imgs
            lab.configure(image=imgs)
            lab.grid(row=2, column=0)


def add(flag):
    val = int(Global.screen.usage.get())
    if val < 30 and flag == 1:
        # if flag is +1 and val<30 minutes then value is incremented
        val = val + 5
    if val > 5 and flag == -1:
        val = val - 5

    Global.screen.usage.configure(state='normal')
    Global.screen.usage.delete(0, 'end')
    Global.screen.usage.insert(0, val)
    Global.screen.usage.configure(state='disabled')


def get_stats():
    switch_page('stats')
    frame = Global.screen.frames['stats']
    plot(frame)
