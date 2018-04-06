import pyttsx3
import threading

global name
global screen
global func_id
global vid
global monitor_thread
global is_available
global path
global close_to

func_id = None


def init():
    global engine, is_available
    engine = pyttsx3.init()
    is_available = True


class Points:
    '''Class to store points listed in the settings file'''
    x, y, w, h, range = 0, 0, 0, 0, 0     # static variables
    prev = 5     # corresponds to all set


'''def goodbye_world():
    print ("Stopping Feed")
    cancel()
    button.configure(text = "Start Feed", command=hello_world)


def hello_world():
    print ("Starting Feed")
    button.configure(text = "Stop Feed", command=goodbye_world)
    print_sleep()


def cancel():
    global func_id
    if func_id is not None:
        print(func_id)
        root.after_cancel(func_id)
        func_id = None


def print_sleep():
    global func_id
    foo = random.randint(4000,7500)
    print ("Sleeping", foo)
    func_id = root.after(foo,print_sleep)
    print(func_id)

root = Tk()
global func_id
func_id = None
button = Button(root, text="Start Feed", command=hello_world)
button.pack()
root.mainloop()'''


