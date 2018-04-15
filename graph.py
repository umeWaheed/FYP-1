import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Global
from datetime import datetime
import numpy as np
import tkinter as tk


def to_sec(string1, string2):
    # h, m, s = string.split(':')
    s1 = datetime.strptime(string1, "%H:%M:%S")     # start time
    s2 = datetime.strptime(string2, "%H:%M:%S")     # end time
    if s1.hour > s2.hour:
        diff = s2.hour+24 - s1.hour        # add 24 to end hour
        return diff*3600+(s2.minute-s1.minute)*60+(s2.second-s1.second)*1.0
    else:
        return (s2-s1).total_seconds()


def draw():
    filename = 'activity/Project_log.txt'

    file = open(filename, "r")
    names = ()
    values = []
    dict = {}

    for line in file:
        #  data = file.read()
        arr = line.split()
        # names = names + (arr[0],)
        # names.append (arr[0])
        # get the hr, minutes and seconds from string
        key = arr[0]
        sec = to_sec(arr[1], arr[2])
        # values.append(sec)
        if arr[0] not in dict:
            dict[key] = sec      # name of application : duration
        else:
            dict[key] = dict.get(key)+sec
        # i = i+1

    for key in dict:
        names = names + (key,)
        values.append(dict[key])

    print(dict)
    print("I am here")
    print(names)
    print(values)

    fig, ax = plt.subplots()
    ax.set_ylabel("Programs")
    y_pos = np.arange(len(names))
    plt.barh(y_pos, values, align='center', alpha=0.5)
    plt.yticks(y_pos, names)
    plt.xlabel('Usage in seconds')
    plt.title('Activity monitoring')
    plt.show()


# draw()


def plot(frame):
    Global.init()
    filename = 'activity/Project_log.txt'

    file = open(filename, "r")
    names = ()
    values = []
    dict = {}
    # i = 0

    for line in file:
        #  data = file.read()
        arr = line.split()
        # names = names + (arr[0],)
        # names.append (arr[0])
        # get the hr, minutes and seconds from string
        key = arr[0]
        sec = to_sec(arr[1], arr[2])
        # values.append(sec)
        if arr[0] not in dict:
            dict[key] = sec      # name of application : duration
        else:
            dict[key] = dict.get(key)+sec
        # i = i+1

    for key in dict:
        names = names + (key,)
        values.append(dict[key])

    print(dict)
    print("I am here")
    print(names)
    print(values)

    # plt.figure(1, figsize=(500, 3))

    label = tk.Label(frame, text="Graph Page!")
    label.pack(pady=10, padx=10)

    button1 = tk.Button(frame, text="Back to Home")
    button1.pack()

    f = Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)

    # fig, ax = plt.subplots()
    # ax.set_ylabel("Programs")
    y_pos = np.arange(len(names))
    plt.barh(y_pos, values, align='center', alpha=0.5)
    plt.yticks(y_pos, names)
    plt.xlabel('Usage in seconds')
    plt.title('Activity monitoring')
    # plt.show()

    a.barh(names, values)
    canvas = FigureCanvasTkAgg(f, frame)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas, frame)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)


'''
def embed(frame):
    label = tk.Label(frame, text="Graph Page!")
    label.pack(pady=10, padx=10)

    button1 = tk.Button(frame, text="Back to Home")
    button1.pack()

    f = Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

    canvas = FigureCanvasTkAgg(f, self)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas, self)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)'''

'''objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(names))
performance = [8, 18, 6, 4, 2, 1]

plt.bar(y_pos, values, align='center')
plt.xticks(y_pos, names)
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()
'''
'''men_means, men_std = (20, 35, 30, 35, 27), (2, 2, 2, 2, 2)
women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)

ind = np.arange(len(men_means))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, names, width, yerr=men_std,
                color='SkyBlue', label='app')
# rects2 = ax.bar(ind + width/2, women_means, width, yerr=women_std,
#                color='IndianRed', label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
ax.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


autolabel(rects1, "left")
autolabel(rects2, "right")

plt.show()'''